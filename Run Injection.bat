@echo off
setlocal EnableDelayedExpansion

echo =============================================================
echo    LoRA Tag Frequency Metadata Adder by: LindezaBlue
echo =============================================================
echo.
echo This batch file will:
echo - Create a virtual environment (venv) if it doesn't exist
echo - Install required dependencies (safetensors + torch CPU version)
echo - Run the metadata injection script
echo.
echo Folder: %~dp0
echo Subfolders:
echo - Dataset to Repair  (for original dataset + LoRA)
echo - Updated LoRA       (new LoRA will be saved here)
echo.
echo IMPORTANT:
echo - Place your dataset folder (e.g., "dataset_name") inside "Dataset to Repair"
echo - Place your original .safetensors LoRA inside "Dataset to Repair"
echo - Edit Metadata_Injection.py to set exact dataset folder name and LoRA filename!
echo.
pause

:: Set working directory to where the batch file is located
cd /d "%~dp0"

:: Search for Python installations
set PYTHON_PATH=
set "PYTHON_SEARCH_PATH=%LOCALAPPDATA%\Programs\Python"

echo Searching for Python installation...
echo.

:: Check for Python 3.11.9 first
if exist "%PYTHON_SEARCH_PATH%\Python311\python.exe" (
    set "PYTHON_PATH=%PYTHON_SEARCH_PATH%\Python311\python.exe"
    echo Found Python 3.11: !PYTHON_PATH!
    goto :python_found
)

:: If not found, search for any Python 3.x version (highest version first)
for /f "tokens=*" %%i in ('dir /b /ad /o-n "%PYTHON_SEARCH_PATH%\Python3*" 2^>nul') do (
    if exist "%PYTHON_SEARCH_PATH%\%%i\python.exe" (
        set "PYTHON_PATH=%PYTHON_SEARCH_PATH%\%%i\python.exe"
        echo Found Python: !PYTHON_PATH!
        goto :python_found
    )
)

:: If still not found, show error
echo ERROR: No Python installation found in %PYTHON_SEARCH_PATH%
echo Please install Python 3.11 or later from python.org
echo Make sure to install for current user (not system-wide)
pause
exit /b 1

:python_found
echo.

:: Create venv if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    "!PYTHON_PATH!" -m venv venv
    if errorlevel 1 (
        echo ERROR: venv creation failed.
        pause
        exit /b 1
    )
)

:: Activate venv
call venv\Scripts\activate

:: Verify we're using the correct Python
echo.
echo Verifying Python version in venv...
python --version
where python
echo.

:: Check if dependencies are installed
echo Checking dependencies...
python -c "import safetensors, torch, packaging" 2>nul
if errorlevel 1 (
    echo Dependencies missing. Installing now...
    echo.
    
    :: Upgrade pip and install dependencies
    python -m pip install --upgrade pip
    python -m pip install packaging
    python -m pip install safetensors
    python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
    
    if errorlevel 1 (
        echo ERROR: Dependency installation failed.
        pause
        exit /b 1
    )
    echo.
    echo Dependencies installed successfully!
) else (
    echo All dependencies already installed.
)
echo.

:: Run the script
echo.
echo Running Metadata_Injection.py...
python Metadata_Injection.py

:: Check if the script failed
if errorlevel 1 (
    echo.
    echo Script encountered an error.
    pause
    exit /b 1
)

echo.
echo Done!
echo - New LoRA file saved to "Updated LoRA" folder
echo - You can deactivate venv with: deactivate
echo.
pause