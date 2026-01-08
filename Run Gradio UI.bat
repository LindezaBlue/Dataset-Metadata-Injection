@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Dataset Metadata Injection - Gradio UI
echo ========================================
echo.

REM Find the latest Python installation
set "PYTHON_BASE=%LOCALAPPDATA%\Programs\Python"
set "PYTHON_EXE="

if exist "%PYTHON_BASE%" (
    for /f "delims=" %%i in ('dir /b /ad /o-n "%PYTHON_BASE%\Python3*" 2^>nul') do (
        if exist "%PYTHON_BASE%\%%i\python.exe" (
            set "PYTHON_EXE=%PYTHON_BASE%\%%i\python.exe"
            goto :found_python
        )
    )
)

:found_python
if not defined PYTHON_EXE (
    echo ERROR: Python not found in %PYTHON_BASE%
    echo Please install Python 3.11 or later from https://www.python.org/
    echo Make sure to select "Install for current user"
    pause
    exit /b 1
)

echo Found Python: %PYTHON_EXE%
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    "%PYTHON_EXE%" -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo Checking dependencies...
python -m pip install --upgrade pip > nul 2>&1
pip install gradio safetensors torch packaging --upgrade

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Starting Gradio Web UI...
echo ========================================
echo The interface will open in your browser at:
echo http://127.0.0.1:7860
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Run the Gradio app
python gradio_ui.py

pause