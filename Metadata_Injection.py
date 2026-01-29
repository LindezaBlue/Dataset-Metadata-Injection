import gradio as gr
import json
from pathlib import Path
from collections import Counter
from safetensors import safe_open
from safetensors.torch import save_file

class MetadataInjector:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.dataset_dir = self.base_dir / "Model to Repair"
        self.output_dir = self.base_dir / "Updated LoRA"
        self.dataset_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
    def scan_dataset(self, subfolder_name):
        # Check if it's an absolute path or a subfolder name
        if Path(subfolder_name).is_absolute():
            dataset_path = Path(subfolder_name)
        else:
            dataset_path = self.dataset_dir / subfolder_name
        
        if not dataset_path.exists():
            return None, f"[ERROR] Dataset folder not found: {dataset_path}"
        
        tag_counter = Counter()
        image_count = 0
        
        for txt_file in dataset_path.glob("*.txt"):
            try:
                with open(txt_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    tags = [tag.strip() for tag in content.split(',') if tag.strip()]
                    tag_counter.update(tags)
                    image_count += 1
            except Exception as e:
                continue
        
        if image_count == 0:
            return None, f"[ERROR] No caption files found in {dataset_path}"
        
        return dict(tag_counter), f"[OK] Found {image_count} images with {len(tag_counter)} unique tags"
    
    def inject_metadata(self, lora_filename, subfolder_name, tag_frequencies):
        lora_path = self.dataset_dir / lora_filename
        
        if not lora_path.exists():
            return None, f"[ERROR] LoRA file not found: {lora_path}"
        
        try:
            tensors = {}
            metadata = {}
            
            with safe_open(lora_path, framework="pt", device="cpu") as f:
                metadata = f.metadata() or {}
                for key in f.keys():
                    tensors[key] = f.get_tensor(key)
            
            dataset_dirs = {
                "1_" + subfolder_name: {
                    "n_repeats": 1,
                    "img_count": sum(tag_frequencies.values())
                }
            }
            
            tag_freq = {
                "1_" + subfolder_name: tag_frequencies
            }
            
            metadata["ss_tag_frequency"] = json.dumps(tag_freq)
            metadata["ss_dataset_dirs"] = json.dumps(dataset_dirs)
            metadata["ss_resolution"] = "1024,1024"
            metadata["ss_num_train_images"] = str(dataset_dirs["1_" + subfolder_name]["img_count"])
            
            output_filename = lora_path.stem + "_with_tags.safetensors"
            output_path = self.output_dir / output_filename
            
            save_file(tensors, str(output_path), metadata=metadata)
            
            return str(output_path), f"[OK] Successfully created: {output_filename}"
            
        except Exception as e:
            return None, f"[ERROR] Error: {str(e)}"

def live_validate(tags_text, frequency):
    freq = 1
    if frequency is not None:
        try:
            freq = int(frequency)
        except ValueError:
            pass
    
    preview = {}
    status = "<span style='color: #888;'>Enter comma-separated tags to see a live preview</span>"
    interactive = gr.update(interactive=False)
    
    if tags_text and tags_text.strip():
        cleaned = tags_text.replace('\n', ',').strip()
        parts = [p.strip() for p in cleaned.split(',') if p.strip()]
        
        if parts:
            if len(parts) == 1 and ' ' in parts[0]:
                status = "<span style='color: #ff9900;'>🔸 Hint: Use commas to separate tags (e.g., blue hair, red eyes)</span>"
            else:
                unique = list(dict.fromkeys(parts))
                dups = len(parts) - len(unique)
                dup_note = f"<br><small>{dups} duplicate(s) removed</small>" if dups > 0 else ""
                preview = {tag: freq for tag in unique}
                count = len(unique)
                status = f"<span style='color: green;'>🟢 Ready — {count} unique tag{'s' if count != 1 else ''}{dup_note}</span>"
                interactive = gr.update(interactive=True)
        else:
            status = "<span style='color: orange;'>⚠️ No tags detected yet</span>"
    
    return preview, status, interactive, preview

def create_ui():
    injector = MetadataInjector()
    
    with gr.Blocks(title="Dataset Metadata Injection Tool") as demo:
        current_tags = gr.State({})
        
        gr.Markdown("""
        # 🏷️ Dataset Metadata Injection Tool
        Add Kohya/A1111-compatible tag frequency metadata to your LoRA files
        """)
        
        with gr.Row():
            # LEFT COLUMN - Steps 1, 2, 3
            with gr.Column(scale=1):
                gr.Markdown("### 🔍 Step 1: Configure Paths")
                
                # LoRA filename only
                lora_input = gr.Dropdown(
                    label="LoRA Filename",
                    choices=[f.name for f in injector.dataset_dir.glob("*.safetensors")],
                    value=None,
                    allow_custom_value=True,
                    info="Select your original LoRA file in 'Model to Repair'"
                )
                
                manual_mode = gr.Checkbox(
                    label="Manual trigger word mode (no dataset required)",
                    value=False,
                    info="Use this if you don't have the training dataset"
                )
                
                subfolder_input = gr.Dropdown(
                    label="Dataset Subfolder Name",
                    choices=[d.name for d in injector.dataset_dir.iterdir() if d.is_dir()],
                    value=None,
                    allow_custom_value=True,
                    info="Select a subfolder or enter a custom path to your dataset",
                    visible=True
                )
                
                manual_tags_input = gr.Textbox(
                    label="Trigger Words (comma-separated)",
                    placeholder="my_character, blue_hair, school_uniform, smiling",
                    lines=2,
                    visible=False,
                    info="Enter your trigger words separated by commas"
                )
                
                tag_frequency_input = gr.Number(
                    label="Tag Frequency (applies to all tags)",
                    value=1,
                    minimum=1,
                    step=1,
                    visible=False,
                    info="How many times each tag appears in your training"
                )
                
                # Button row: Scan and Select Folder
                with gr.Row():
                    scan_btn = gr.Button("🔍 Scan Dataset / Parse Tags", variant="primary", size="lg", visible=True, scale=3)
                    select_folder_btn = gr.Button("📁 Select Dataset Folder", size="lg", visible=True, scale=1)
                
                gr.Markdown("### 🚀 Step 3: Inject Metadata")
                
                inject_btn = gr.Button("💾 Inject Metadata & Save", variant="primary", size="lg", interactive=False)
                
                output_status = gr.Textbox(label="Output Status", interactive=False, lines=4)
                output_path = gr.Textbox(label="Output File Location", interactive=False, lines=4)
                
            # RIGHT COLUMN - Step 2 Review Tags + Instructions
            with gr.Column(scale=1):
                gr.Markdown("### 🏷️ Step 2: Review Tags")
                
                tag_display = gr.JSON(
                    label="Tag Frequencies",
                    value={}
                )
                
                manual_preview = gr.JSON(
                    label="Tag Frequencies (Live Preview)",
                    value={},
                    visible=False
                )
                
                review_status = gr.Markdown("")
                
                gr.Markdown(
                    "*Review the tag frequencies that will be injected into your LoRA*"
                )
                
                # Dynamic Instructions
                instructions_display = gr.Markdown("""
                ### 📋 Instructions:
                
                **Normal Mode (with dataset):**
                1. Place your LoRA file (.safetensors) in the `Model to Repair` folder
                2. Select your LoRA filename from the dropdown
                3. Select a dataset subfolder from the dropdown, OR enter a custom full path to your dataset folder
                4. Click "Scan Dataset / Parse Tags" to detect tags
                5. Review the tag frequencies
                6. Click "Inject Metadata & Save" to create your updated LoRA
                
                **File Locations:**
                - **Input:** Place LoRA files in `Model to Repair/`
                - **Output:** Updated files saved to `Updated LoRA/`
                
                **Note:** You can use subfolders inside 'Model to Repair' for datasets or provide any custom folder path on your system.
                """)
        
        # Event handlers
        def toggle_manual_mode(is_manual):
            if is_manual:
                instructions_text = """
                ### 📋 Instructions:
                
                **Manual Mode (without dataset):**
                1. Place your LoRA file (.safetensors) in the `Model to Repair` folder
                2. Select your LoRA filename from the dropdown
                3. Check "Manual trigger word mode"
                4. Enter your trigger words (comma-separated)
                5. Set the tag frequency (default: 1)
                6. Watch the live preview and status update as you type
                7. When the status is green and tags are ready, click "Inject Metadata & Save"
                
                **File Locations:**
                - **Input:** Place LoRA files in `Model to Repair/`
                - **Output:** Updated files saved to `Updated LoRA/`
                """
            else:
                instructions_text = """
                ### 📋 Instructions:
                
                **Normal Mode (with dataset):**
                1. Place your LoRA file (.safetensors) in the `Model to Repair` folder
                2. Select your LoRA filename from the dropdown
                3. Select a dataset subfolder from the dropdown, OR enter a custom full path to your dataset folder
                4. Click "Scan Dataset / Parse Tags" to detect tags
                5. Review the tag frequencies
                6. Click "Inject Metadata & Save" to create your updated LoRA
                
                **File Locations:**
                - **Input:** Place LoRA files in `Model to Repair/`
                - **Output:** Updated files saved to `Updated LoRA/`
                
                **Note:** You can use subfolders inside 'Model to Repair' for datasets or provide any custom folder path on your system.
                """
            
            return {
                subfolder_input: gr.update(visible=not is_manual),
                manual_tags_input: gr.update(visible=is_manual),
                tag_frequency_input: gr.update(visible=is_manual),
                scan_btn: gr.update(visible=not is_manual),
                select_folder_btn: gr.update(visible=not is_manual),
                tag_display: gr.update(visible=not is_manual, value={}),
                manual_preview: gr.update(visible=is_manual, value={}),
                review_status: gr.update(value=""),
                inject_btn: gr.update(interactive=False),
                current_tags: {},
                instructions_display: gr.update(value=instructions_text)
            }
        
        def select_dataset_folder():
            """Open folder browser dialog"""
            try:
                import tkinter as tk
                from tkinter import filedialog
                
                root = tk.Tk()
                root.withdraw()
                root.wm_attributes('-topmost', 1)
                
                folder_path = filedialog.askdirectory(
                    title="Select Dataset Folder",
                    initialdir=str(injector.dataset_dir)
                )
                
                root.destroy()
                
                if folder_path:
                    return gr.update(value=folder_path)
                else:
                    return gr.update()
            except Exception as e:
                # Fallback if tkinter not available
                return gr.update()
        
        def scan_dataset_handler(is_manual, subfolder, lora_file):
            if not lora_file:
                status = "⚠️ [WARNING] Please select a LoRA file"
                return {}, status, gr.update(interactive=False), {}
            
            if is_manual:
                status = "<span style='color: orange;'>In manual mode, use the live preview — no scan needed</span>"
                return {}, status, gr.update(interactive=False), {}
            
            if not subfolder:
                status = "⚠️ [WARNING] Please select a dataset subfolder"
                return {}, status, gr.update(interactive=False), {}
            
            tags, status = injector.scan_dataset(subfolder)
            success = tags is not None
            
            if success:
                status = f"<span style='color: green;'>{status}</span>"
                interactive = gr.update(interactive=True)
            else:
                status = f"<span style='color: red;'>{status}</span>"
                interactive = gr.update(interactive=False)
            
            return tags or {}, status, interactive, tags or {}
        
        def inject_handler(is_manual, lora_file, subfolder, tags):
            if not tags:
                return "[WARNING] No tags to inject — please scan or enter tags first", ""
            
            if not lora_file:
                return "[WARNING] Missing LoRA file", ""
            
            folder_name = "manual_tags" if is_manual else subfolder
            
            if not is_manual and not subfolder:
                return "[WARNING] Missing dataset subfolder", ""
            
            output_path_result, status = injector.inject_metadata(lora_file, folder_name, tags)
            return status, output_path_result or ""
        
        # Connect event handlers
        manual_mode.change(
            fn=toggle_manual_mode,
            inputs=[manual_mode],
            outputs=[subfolder_input, manual_tags_input, tag_frequency_input, scan_btn,
                     select_folder_btn, tag_display, manual_preview, review_status, inject_btn, current_tags, instructions_display]
        )
        
        manual_tags_input.change(
            fn=live_validate,
            inputs=[manual_tags_input, tag_frequency_input],
            outputs=[manual_preview, review_status, inject_btn, current_tags]
        )
        
        tag_frequency_input.change(
            fn=live_validate,
            inputs=[manual_tags_input, tag_frequency_input],
            outputs=[manual_preview, review_status, inject_btn, current_tags]
        )
        
        select_folder_btn.click(
            fn=select_dataset_folder,
            outputs=[subfolder_input]
        )
        
        scan_btn.click(
            fn=scan_dataset_handler,
            inputs=[manual_mode, subfolder_input, lora_input],
            outputs=[tag_display, review_status, inject_btn, current_tags]
        )
        
        inject_btn.click(
            fn=inject_handler,
            inputs=[manual_mode, lora_input, subfolder_input, current_tags],
            outputs=[output_status, output_path]
        )
    
    return demo

if __name__ == "__main__":
    demo = create_ui()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True,
        theme=gr.themes.Soft()
    )
