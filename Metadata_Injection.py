import os
import json
from collections import Counter
from safetensors.torch import load_file, save_file
from safetensors import safe_open


# ------------------------------------------------------- #
#              === UPDATE THESE VALUES ===                #
# ------------------------------------------------------- #

# Name of your dataset subfolder inside "Dataset to Repair" (e.g., the flat folder with images + .txt)
dataset_subfolder = "my_character"  # <--- CHANGE THIS (e.g., "my_character")

# Exact filename of your original trained LoRA in "Dataset to Repair"
original_lora_filename = "my_lora.safetensors"  # <--- CHANGE THIS (e.g., "my_lora.safetensors")

# ------------------------------------------------------- #


# === NO NEED TO EDIT BELOW (uses relative paths) ===
base_dir = os.path.dirname(__file__)  # Script folder
dataset_dir = os.path.join(base_dir, "Dataset to Repair", dataset_subfolder)
lora_path = os.path.join(base_dir, "Dataset to Repair", original_lora_filename)
output_dir = os.path.join(base_dir, "Updated LoRA")

# Check if dataset folder exists
if not os.path.exists(dataset_dir):
    print("\n================================================")
    print("!!! Missing Dataset Folder/Safetensor Model  !!!")
    print("================================================")
    print(f"\nDataset folder not found: {dataset_dir}")
    print(f"Please create the folder and add your images + .txt files inside.")
    raise SystemExit(1)

# Check if LoRA file exists
if not os.path.exists(lora_path):
    print("\n================================================")
    print("!!! Missing Dataset Folder/Safetensor Model  !!!")
    print("================================================")
    print(f"\nLoRA file not found: {lora_path}")
    print(f"Please place your .safetensors file in 'Dataset to Repair' folder.")
    raise SystemExit(1)

# Create output folder if needed
os.makedirs(output_dir, exist_ok=True)

# Compute tag frequency
tags = Counter()
num_images = 0

# Check if dataset folder has any images
has_images = False
for filename in os.listdir(dataset_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        has_images = True
        break

if not has_images:
    print("\n================================================")
    print("!!! Missing Dataset Folder/Safetensor Model  !!!")
    print("================================================")
    print(f"\nNo images found in dataset folder: {dataset_dir}")
    print(f"Please add .png, .jpg, or .jpeg images to this folder.")
    raise SystemExit(1)

for filename in os.listdir(dataset_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        num_images += 1
        txt_path = os.path.join(dataset_dir, os.path.splitext(filename)[0] + ".txt")
        if os.path.exists(txt_path):
            with open(txt_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                caption_tags = [t.strip() for t in content.split(',') if t.strip()]
                for tag in caption_tags:
                    tags[tag] += 1

tag_freq_dict = {dataset_subfolder: {tag: count for tag, count in tags.items()}}

# Load existing LoRA (removed duplicate check since we already checked above)
# Load the state dict and metadata separately using safe_open
state_dict = load_file(lora_path)

# Get existing metadata
metadata = {}
with safe_open(lora_path, framework="pt") as f:
    metadata = f.metadata() or {}

# Add Kohya/A1111 compatible keys
metadata['ss_tag_frequency'] = json.dumps(tag_freq_dict)
metadata['ss_dataset_dirs'] = json.dumps({dataset_subfolder: {"n_images": num_images}})
metadata['ss_resolution'] = "1024,1024"  # Adjust if your training used different
metadata['ss_num_train_images'] = str(num_images)

# Save new LoRA to "Updated LoRA" folder
new_filename = os.path.basename(original_lora_filename).replace(".safetensors", "_with_tags.safetensors")
new_path = os.path.join(output_dir, new_filename)
save_file(state_dict, new_path, metadata=metadata)

print(f"Success! New LoRA with tag frequency saved to:\n{new_path}")
print(f"Dataset scanned: {dataset_dir} ({num_images} images)")
print("Top 10 tags added:", dict(list(tags.most_common(10))))