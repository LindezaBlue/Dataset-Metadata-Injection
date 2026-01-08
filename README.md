# Dataset Metadata Injection Tool

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC--BY--NC--SA%204.0-orange.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![Platform: Linux](https://img.shields.io/badge/platform-Linux-brightgreen.svg)](https://www.kernel.org/)

A lightweight Python tool for adding Kohya/A1111-compatible tag frequency metadata to LoRA (Low-Rank Adaptation) safetensors files. This tool fixes missing tag metadata in LoRA files trained with AI-Toolkit or similar programs, ensuring proper display in A1111/Forge/ForgeNeo.

![Tag Metadata Example](https://private-user-images.githubusercontent.com/141217866/531762017-334f5a71-5664-42bf-925b-108605d02fe5.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Njc4OTI3MDUsIm5iZiI6MTc2Nzg5MjQwNSwicGF0aCI6Ii8xNDEyMTc4NjYvNTMxNzYyMDE3LTMzNGY1YTcxLTU2NjQtNDJiZi05MjViLTEwODYwNWQwMmZlNS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwMTA4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDEwOFQxNzEzMjVaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT00ZjI4NGYzNTdiMzI0ZDhmOTAyZTg2ODZlN2UyZTlmZGRiNDc0NGFjOTllZjNmMzc4NTAzMmJkNzQ5NDQyYjQzJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.nyeREqV3xFyw4nQZkmqKXalNkBtDKnz3X_Mxe9sqB3A)

---

## 🌟 Features

- **Automatic Tag Frequency Calculation** — Scans caption files and counts tag occurrences across your dataset
- **Kohya/A1111 Compatible** — Adds standard metadata fields (`ss_tag_frequency`, `ss_dataset_dirs`, etc.)
- **Non-Destructive Processing** — Creates new files with metadata while preserving originals
- **Smart Dependency Management** — Auto-installs required packages in isolated virtual environment
- **Portable & User-Friendly** — Works from any folder with clear error messages

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** — [Download here](https://www.python.org/downloads/)
- **Windows OS** — Batch file automation (Linux support planned)
- **.safetensors LoRA file** — Your trained model
- **Training dataset** — Images with corresponding `.txt` caption files

### Installation

1. Clone or download this repository:
   ```bash
   git clone https://github.com/LindezaBlue/Dataset-Metadata-Injection.git
   cd Dataset-Metadata-Injection
   ```

2. No additional setup required! The batch files handle dependency installation automatically.

---

## 📖 Usage Guide

### Gradio Web Interface

The easiest way to use this tool is through the visual web interface.

### Step 1: Prepare Your Files

1. Place you dataset subfolder inside `Dataset to Repair/`  
   Example: `Dataset to Repair/my_character/`  
   - Place all your training images (`.png`, `.jpg`, `.jpeg`) in this folder
   - Ensure each image has a matching `.txt` caption file with comma-separated tags  
     Example: `image1.png` → `image1.txt` containing `1girl, blue hair, smiling, outdoors`

2. Place your original LoRA file (`.safetensors` format) directly in the `Dataset to Repair/` folder, **not inside the model subfolder!**

### Step 2: Launch the Gradio Interface

1. Double-click `Run Gradio UI.bat`  
   The batch file will automatically:  
   - Detect your Python installation  
   - Create a virtual environment *(first run only)*
   - Install required dependencies *(gradio, safetensors, torch CPU-only, etc.—first run only)*  
   - Launch the web interface in your default browser at **http://127.0.0.1:7860**

### Step 3: Use the Web Interface

The interface guides you step-by-step:

1. **Select your files**  
   - Choose your **Dataset Subfolder Name** from the dropdown
   - Choose your **LoRA Filename** from the dropdown  
   - Click **Refresh File Lists** if your files don't appear yet

2. **Scan the dataset**  
   - Click **Scan Dataset**  
   - The tool will automatically read all `.txt` caption files and count tag frequencies  
   - Results appear in the **Tag Frequencies** box

3. **Inject the metadata**  
   - Click **Inject Metadata & Save**  
   - A new LoRA file with embedded metadata will be created  
   - Find it in the `Updated LoRA/` folder (filename ends with `_with_tags.safetensors`)

5. When you're done, just close the browser tab, and Terminal/CLI to exit the program.

![Gradio Interface](https://private-user-images.githubusercontent.com/141217866/533147921-b6fc282b-9b60-4678-9efe-7a1b5f093eb8.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Njc4OTI3MDUsIm5iZiI6MTc2Nzg5MjQwNSwicGF0aCI6Ii8xNDEyMTc4NjYvNTMzMTQ3OTIxLWI2ZmMyODJiLTliNjAtNDY3OC05ZWZlLTdhMWI1ZjA5M2ViOC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwMTA4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDEwOFQxNzEzMjVaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT01ODEzM2FlNDJiYWQyNDgxNGQ3MTg2ZDQ3YmQwMzE2OGVjNmE5OTljZWM3ODYzOTNkMTQ4OGI5YTQ0N2M3YzhmJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.1s54RbRuNyf7W8wlNEpRVULJZohx7aoReJn4QGA_lXg)

### Linux Users

A launch script `run_gradio_ui.sh` is provided for Linux systems.  
It mirrors the Windows batch file, creating a virtual environment, installing dependencies, and launching the Gradio UI.  

⚠️ **Linux users, please test this script and report any issues**, especially with automatic browser opening or dependency installation.
*(I currently am not able to test if this works on Linux systems so feedback is appreciated, Thank you!)*


---

## 📂 Project Structure

```
Dataset-Metadata-Injection/
├── Run Gradio UI.bat           # Launch web interface
├── gradio_ui.py               # Gradio interface code
├── Metadata_Injection.py      # Core injection logic
├── requirements.txt           # Python dependencies
├── Dataset to Repair/         # Input folder for your files
│   └── [your_dataset]/
│   └── [your_model]/
└── Updated LoRA/              # Output folder
```

---

## 🔧 Technical Details

### Metadata Fields Added

This tool injects the following Kohya SS / A1111-compatible fields:

| Field | Description |
|-------|-------------|
| `ss_tag_frequency` | JSON object mapping tags to occurrence counts |
| `ss_dataset_dirs` | Dataset folder names and image counts |
| `ss_resolution` | Training resolution (default: `1024,1024`) |
| `ss_num_train_images` | Total number of training images |

### Dependencies

All dependencies are auto-installed in an isolated virtual environment:

- **safetensors** — Safe model file loading/saving
- **torch** (CPU-only) — Minimal PyTorch for tensor operations
- **gradio** — Web-based UI framework
- **packaging** — Version management utilities

### System Requirements

- **Python:** 3.11 or later (auto-detected from `%LOCALAPPDATA%\Programs\Python`)
- **Disk Space:** ~500MB for virtual environment
- **Platform:** Windows *(Linux support in development)*

---

## ❓ Troubleshooting

### "Missing Dataset Folder/Safetensor Model"

**Problem:** Files not found in expected locations

**Solutions:**
- Verify your dataset folder exists in `Dataset to Repair/`
- Ensure `.safetensors` file is in `Dataset to Repair/`, not in a subfolder

### "Python not found"

**Problem:** Python installation not detected

**Solutions:**
- Install Python 3.11+ from [python.org](https://www.python.org/downloads/)
- Use "Install for current user" option during installation
- Script auto-searches `%LOCALAPPDATA%\Programs\Python\`

### Virtual Environment Issues

**Solution:** Delete the `venv/` folder and re-run the batch file to recreate it cleanly

### Caption File Format

Ensure your `.txt` files use comma-separated tags:
```
# Correct
1girl, blue hair, smiling, outdoors, school uniform

# Incorrect (will not parse properly)
1girl blue hair smiling outdoors school uniform
```

---

## 🛣️ Roadmap

- [x] ~~Implement referenced .json config file for easier editing~~
- [x] ~~Create Gradio web interface for simplified user experience~~
- [ ] Add batch processing for multiple LoRAs
- [ ] Support for Linux platforms *(In-Progress, Needs Testers)*
- [ ] Tag frequency visualization charts
- [ ] Export/import metadata presets
- [ ] Any suggestions from the community 

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report bugs** via [GitHub Issues](https://github.com/LindezaBlue/Dataset-Metadata-Injection/issues)
2. **Submit pull requests** for new features or fixes
3. **Share feedback** and suggestions for improvement
4. **Star this repo** if you find it useful!

---

## 📄 License

This project is licensed under the  
**Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**.  
See the [LICENSE file](https://github.com/LindezaBlue/Dataset-Metadata-Injection/tree/main?tab=License-1-ov-file) for full details.

You are free to **use, modify, and share** this project, **but only for non-commercial purposes**, and you must **give proper credit** to the original author.  

### If you remix or build upon this work, you must distribute your contributions under the **same license**!

---

## 💖 Support & Credits

**Created by:** [LindezaBlue](https://github.com/LindezaBlue)

Special thanks to the AI art community for feedback and testing!

If you find this tool helpful:
- ⭐ **Star this repository**
- 🐛 **Report issues** to help improve the tool
- 📢 **Share** with others who might benefit

---

## 📝 Notes

- This tool modifies **metadata only**, not model weights
- Designed for AI-Toolkit trained LoRAs missing standard metadata
- Compatible with Automatic1111, Forge, and ForgeNeo interfaces
- Non-destructive processing ensures your originals remain intact

---

**Questions?** Open an [issue](https://github.com/LindezaBlue/Dataset-Metadata-Injection/issues) or check existing discussions!
