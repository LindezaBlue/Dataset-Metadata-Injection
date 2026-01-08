import gradio as gr
import json
import os
from pathlib import Path
from collections import Counter
from safetensors import safe_open
from safetensors.torch import save_file
import torch

class MetadataInjector:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.dataset_dir = self.base_dir / "Dataset to Repair"
        self.output_dir = self.base_dir / "Updated LoRA"
        self.output_dir.mkdir(exist_ok=True)
        
    def scan_dataset(self, subfolder_name):
        """Scan dataset folder and return tag frequencies"""
        dataset_path = self.dataset_dir / subfolder_name
        
        if not dataset_path.exists():
            return None, f"❌ Dataset folder not found: {dataset_path}"
        
        tag_counter = Counter()
        image_count = 0
        
        # Scan for caption files
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
            return None, f"❌ No caption files found in {dataset_path}"
        
        return dict(tag_counter), f"✅ Found {image_count} images with {len(tag_counter)} unique tags"
    
    def inject_metadata(self, lora_filename, subfolder_name, tag_frequencies):
        """Inject metadata into LoRA file"""
        lora_path = self.dataset_dir / lora_filename
        
        if not lora_path.exists():
            return None, f"❌ LoRA file not found: {lora_path}"
        
        try:
            # Load original LoRA
            tensors = {}
            metadata = {}
            
            with safe_open(lora_path, framework="pt", device="cpu") as f:
                metadata = f.metadata() or {}
                for key in f.keys():
                    tensors[key] = f.get_tensor(key)
            
            # Prepare metadata
            dataset_dirs = {
                "1_" + subfolder_name: {
                    "n_repeats": 1,
                    "img_count": sum(1 for _ in (self.dataset_dir / subfolder_name).glob("*.txt"))
                }
            }
            
            tag_freq = {
                "1_" + subfolder_name: tag_frequencies
            }
            
            # Update metadata
            metadata["ss_tag_frequency"] = json.dumps(tag_freq)
            metadata["ss_dataset_dirs"] = json.dumps(dataset_dirs)
            metadata["ss_resolution"] = "1024,1024"
            metadata["ss_num_train_images"] = str(dataset_dirs["1_" + subfolder_name]["img_count"])
            
            # Save new LoRA
            output_filename = lora_path.stem + "_with_tags.safetensors"
            output_path = self.output_dir / output_filename
            
            save_file(tensors, str(output_path), metadata=metadata)
            
            return str(output_path), f"✅ Successfully created: {output_filename}"
            
        except Exception as e:
            return None, f"❌ Error: {str(e)}"

def create_ui():
    injector = MetadataInjector()
    
    with gr.Blocks(title="Dataset Metadata Injection Tool") as demo:
        gr.Markdown("""
        # 🏷️ Dataset Metadata Injection Tool
        Add Kohya/A1111-compatible tag frequency metadata to your LoRA files
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 📁 Step 1: Configure Paths")
                
                # List available dataset folders
                dataset_folders = [d.name for d in (injector.dataset_dir).iterdir() if d.is_dir()]
                subfolder_input = gr.Dropdown(
                    label="Dataset Subfolder Name",
                    choices=dataset_folders,
                    value=dataset_folders[0] if dataset_folders else None,
                    allow_custom_value=True,
                    info="Select your dataset folder inside 'Dataset to Repair'"
                )
                
                # List available LoRA files
                lora_files = [f.name for f in (injector.dataset_dir).glob("*.safetensors")]
                lora_input = gr.Dropdown(
                    label="LoRA Filename",
                    choices=lora_files,
                    value=lora_files[0] if lora_files else None,
                    allow_custom_value=True,
                    info="Select your original LoRA file in 'Dataset to Repair'"
                )
                
                refresh_btn = gr.Button("🔄 Refresh File Lists", size="sm")
                scan_btn = gr.Button("🔍 Scan Dataset", variant="primary", size="lg")
                scan_status = gr.Textbox(label="Scan Status", interactive=False)
                
            with gr.Column(scale=1):
                gr.Markdown("### 🏷️ Step 2: Review Tags")
                
                tag_display = gr.JSON(
                    label="Tag Frequencies",
                    value={}
                )
                
                gr.Markdown(
                    "*This displays the tag frequency data detected from your dataset*"
                )
        
        gr.Markdown("### 🚀 Step 3: Inject Metadata")
        
        with gr.Row():
            inject_btn = gr.Button("💾 Inject Metadata & Save", variant="primary", size="lg")
            clear_btn = gr.Button("🔄 Clear All", size="lg")
        
        with gr.Row():
            output_status = gr.Textbox(label="Output Status", interactive=False)
            output_path = gr.Textbox(label="Output File Location", interactive=False)
        
        gr.Markdown("""
        ---
        ### 📋 Instructions:
        1. Enter your dataset subfolder name and LoRA filename
        2. Click "Scan Dataset" to detect tags
        3. Review and optionally edit the tag frequencies
        4. Click "Inject Metadata & Save" to create your updated LoRA
        
        **Output folder:** `Updated LoRA/`
        """)
        
        # Event handlers
        def refresh_files():
            """Refresh the list of available folders and files"""
            folders = [d.name for d in (injector.dataset_dir).iterdir() if d.is_dir()]
            files = [f.name for f in (injector.dataset_dir).glob("*.safetensors")]
            return (
                gr.Dropdown(choices=folders, value=folders[0] if folders else None),
                gr.Dropdown(choices=files, value=files[0] if files else None)
            )
        
        def scan_dataset_handler(subfolder, lora_file):
            if not subfolder or not lora_file:
                return {}, "⚠️ Please select both subfolder and LoRA file"
            
            tags, status = injector.scan_dataset(subfolder)
            if tags:
                return tags, status
            return {}, status
        
        def inject_handler(lora_file, subfolder, tags):
            if not tags:
                return "⚠️ Please scan dataset first", ""
            
            if not lora_file or not subfolder:
                return "⚠️ Missing configuration", ""
            
            output_path_result, status = injector.inject_metadata(lora_file, subfolder, tags)
            return status, output_path_result or ""
        
        def clear_all():
            folders = [d.name for d in (injector.dataset_dir).iterdir() if d.is_dir()]
            files = [f.name for f in (injector.dataset_dir).glob("*.safetensors")]
            return (
                folders[0] if folders else None,
                files[0] if files else None,
                {},
                "",
                "",
                ""
            )
        
        refresh_btn.click(
            fn=refresh_files,
            outputs=[subfolder_input, lora_input]
        )
        
        scan_btn.click(
            fn=scan_dataset_handler,
            inputs=[subfolder_input, lora_input],
            outputs=[tag_display, scan_status]
        )
        
        inject_btn.click(
            fn=inject_handler,
            inputs=[lora_input, subfolder_input, tag_display],
            outputs=[output_status, output_path]
        )
        
        clear_btn.click(
            fn=clear_all,
            outputs=[subfolder_input, lora_input, tag_display, scan_status, output_status, output_path]
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
