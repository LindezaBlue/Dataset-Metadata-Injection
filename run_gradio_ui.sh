#!/bin/bash
# run_gradio_ui.sh - Linux version of Dataset Metadata Injection launcher

echo "============================================================="
echo "   LoRA Metadata Injection - Gradio Web UI by: LindezaBlue"
echo "============================================================="
echo
echo "This script will:"
echo "- Create a virtual environment (venv) if it doesn't exist"
echo "- Install required dependencies (gradio, safetensors, torch CPU)"
echo "- Launch the Gradio web interface"
echo
echo "Folder: $(pwd)"
echo "Subfolders:"
echo "- Dataset to Repair  (for original dataset + LoRA)"
echo "- Updated LoRA       (new LoRA will be saved here)"
echo
echo "The web interface will open automatically in your browser at:"
echo "http://127.0.0.1:7860"
echo
read -p "Press Enter to continue..."

# Change directory to script location
cd "$(dirname "$0")" || exit 1

# Detect Python 3
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "ERROR: Python 3 is not installed."
    echo "Please install Python 3.11 or later."
    exit 1
fi
echo "Using Python: $($PYTHON --version)"

# Create venv if missing
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON -m venv venv || { echo "ERROR: venv creation failed."; exit 1; }
fi

# Activate venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Check dependencies
python -c "import gradio, safetensors, torch, packaging" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Dependencies missing. Installing now..."
    pip install packaging safetensors gradio
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
    if [ $? -ne 0 ]; then
        echo "ERROR: Dependency installation failed."
        exit 1
    fi
    echo "Dependencies installed successfully!"
else
    echo "All dependencies already installed."
fi

# Launch browser after 7 seconds
sleep 7 && xdg-open http://127.0.0.1:7860 &

# Start Gradio UI
echo "========================================"
echo "Starting Gradio Web UI..."
echo "Press Ctrl+C to stop the server"
echo "========================================"
python gradio_ui.py
if [ $? -ne 0 ]; then
    echo "Script encountered an error."
    exit 1
fi

echo
echo "Web UI closed."
echo "You can deactivate venv with: deactivate"
read -p "Press Enter to exit..."
