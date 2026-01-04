# Dataset Metadata Injection Tool

A lightweight Python tool that adds Kohya/A1111-compatible tag frequency metadata to LoRA (Low-Rank Adaptation) model files. This tool scans your training dataset and embeds tag statistics directly into your `.safetensors` LoRA files, making them compatible with automatic tag completion and other metadata-dependent features in AI image generation tools.

## Features

- ✅ **Automatic Tag Frequency Calculation** - Scans all caption `.txt` files in your dataset and counts tag occurrences
- ✅ **Kohya/A1111 Compatible** - Adds `ss_tag_frequency`, `ss_dataset_dirs`, and other standard metadata fields
- ✅ **Portable** - Works from any folder location with automatic Python detection
- ✅ **User-Friendly** - Simple batch file interface with clear error messages
- ✅ **Non-Destructive** - Creates a new LoRA file with metadata while preserving your original
- ✅ **Smart Dependency Management** - Automatically installs required packages only when needed

## Requirements

- **Python 3.11 or later** (automatically detected from `%LOCALAPPDATA%\Programs\Python`)
- **Windows OS** (batch file automation)
- **Original LoRA file** in `.safetensors` format
- **Training dataset** with images and corresponding `.txt` caption files

## Installation

1. **Download or clone this repository:**
   ```bash
   git clone https://github.com/LindezaBlue/Dataset-Metadata-Injection.git
   cd Dataset-Metadata-Injection
   ```

2. **Ensure Python 3.11+ is installed** on your system. Download from [python.org](https://www.python.org/downloads/) if needed.

3. **No additional setup required!** The batch file handles everything automatically.

## Folder Structure

```
Dataset-Metadata-Injection/
├── Run Injection.bat           # Main execution script
├── Metadata_Injection.py       # Core Python script
├── Dataset to Repair/          # Place your files here
│   ├── dataset_name/           # Your dataset folder (rename as needed)
│   │   ├── image1.png
│   │   ├── image1.txt
│   │   ├── image2.jpg
│   │   └── image2.txt
│   └── model_name.safetensors  # Your original LoRA file
└── Updated LoRA/               # Output folder (created automatically)
    └── model_name_with_tags.safetensors
```

## Usage

### Step 1: Prepare Your Files

1. **Create your dataset folder** inside `Dataset to Repair/`:
   - Example: `Dataset to Repair/my_character/`
   - Place all training images (`.png`, `.jpg`, `.jpeg`) in this folder
   - Ensure each image has a matching `.txt` file with comma-separated tags
     - Example: `image1.png` → `image1.txt` containing `1girl, blue hair, smiling, outdoors`

2. **Place your original LoRA** (`.safetensors` file) directly in `Dataset to Repair/`

### Step 2: Configure the Script

Open `Metadata_Injection.py` in a text editor and update these two lines:

```python
# Name of your dataset subfolder inside "Dataset to Repair"
dataset_subfolder = "my_character"  # <--- Change to your folder name

# Exact filename of your original trained LoRA in "Dataset to Repair"
original_lora_filename = "my_lora.safetensors"  # <--- Change to your LoRA filename
```

### Step 3: Run the Tool

1. Double-click `Run Injection.bat`
2. The script will:
   - Automatically find your Python installation
   - Create a virtual environment (first run only)
   - Install dependencies (first run only)
   - Scan your dataset and count tag frequencies
   - Generate a new LoRA file with embedded metadata

3. Find your updated LoRA in the `Updated LoRA/` folder with `_with_tags` appended to the filename

## Example Output

```
Running Metadata_Injection.py...
Success! New LoRA with tag frequency saved to:
E:\Dataset-Metadata-Injection\Updated LoRA\my_lora_with_tags.safetensors
Dataset scanned: E:\Dataset-Metadata-Injection\Dataset to Repair\my_character (25 images)
Top 10 tags added: {'1girl': 25, 'blue hair': 20, 'smiling': 18, 'outdoors': 15, ...}
```

## Troubleshooting

### "Missing Dataset Folder/Safetensor Model" Error

- **Cause**: The dataset folder or LoRA file wasn't found
- **Solution**: 
  1. Check that your dataset folder exists inside `Dataset to Repair/`
  2. Verify the folder name in `Metadata_Injection.py` matches exactly (case-sensitive)
  3. Ensure your `.safetensors` file is in `Dataset to Repair/` (not in a subfolder)

### "Python not found" Error

- **Cause**: Python isn't installed or isn't in the expected location
- **Solution**: 
  1. Install Python 3.11+ from [python.org](https://www.python.org/downloads/)
  2. During installation, choose "Install for current user" (not system-wide)
  3. The script searches `%LOCALAPPDATA%\Programs\Python\` automatically

### Virtual Environment Issues

- **Solution**: Delete the `venv/` folder and run the batch file again to recreate it

## Metadata Added

This tool adds the following metadata fields to your LoRA:

- `ss_tag_frequency` - JSON object containing tag counts per dataset
- `ss_dataset_dirs` - JSON object with dataset folder names and image counts
- `ss_resolution` - Training resolution (default: `1024,1024`)
- `ss_num_train_images` - Total number of training images

## Technical Details

- **Dependencies**: `safetensors`, `torch` (CPU), `packaging`
- **Python Version**: 3.11+ (automatically detected)
- **Framework**: PyTorch (CPU-only for minimal overhead)
- **Metadata Format**: Kohya SS / Automatic1111 WebUI compatible

## Contributing

Contributions are welcome! Feel free to:
- Report bugs via [Issues](https://github.com/LindezaBlue/Dataset-Metadata-Injection/issues)
- Submit pull requests for improvements
- Suggest new features

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

You are free to use, modify, and distribute this software, provided you credit the original author (LindezaBlue).

## Credits

**Created by**: [LindezaBlue](https://github.com/LindezaBlue)

Special thanks to the AI art community for feedback and testing!

## Support

If you find this tool helpful, consider:
- ⭐ Starring this repository
- 🐛 Reporting issues to help improve the tool
- 📢 Sharing with others who might benefit

---

**Note**: This tool is designed for AI-Toolkit trained LoRAs that may be missing metadata. It does not modify the model weights themselves, only the metadata container.
