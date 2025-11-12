@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo Fluxgym Setup Script (Windows)
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.10 or higher from https://www.python.org/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Found Python %PYTHON_VERSION%
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH.
    echo Please install Git from https://git-scm.com/download/win
    pause
    exit /b 1
)
echo [OK] Found Git
echo.

REM Check if sd-scripts exists, clone if not
if not exist "sd-scripts" (
    echo sd-scripts directory not found. Cloning from GitHub...
    git clone -b sd3 https://github.com/kohya-ss/sd-scripts
    if errorlevel 1 (
        echo ERROR: Failed to clone sd-scripts repository
        pause
        exit /b 1
    )
    echo   [OK] sd-scripts cloned successfully
) else (
    echo [OK] Found sd-scripts directory
)
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist "env" (
    echo   Virtual environment already exists. Skipping creation.
) else (
    python -m venv env
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo   [OK] Virtual environment created
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call env\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo   [OK] Virtual environment activated
echo.

REM Upgrade pip, setuptools, and wheel
echo Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo WARNING: Failed to upgrade pip tools, continuing anyway...
)
echo   [OK] pip tools upgraded
echo.

REM Install sd-scripts dependencies
echo Installing sd-scripts dependencies...
cd sd-scripts
pip install --prefer-binary -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install sd-scripts dependencies
    cd ..
    pause
    exit /b 1
)
cd ..
echo   [OK] sd-scripts dependencies installed
echo.

REM Install fluxgym dependencies
echo Installing fluxgym dependencies...
pip install --prefer-binary -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install fluxgym dependencies
    pause
    exit /b 1
)
echo   [OK] fluxgym dependencies installed
echo.

REM Ask about GPU type
echo ==========================================
echo PyTorch Installation
echo ==========================================
echo.
echo Select your GPU type:
echo   1) Standard install - CUDA 12.1 (Recommended for all GPUs)
echo   2) RTX 50-series optimized - CUDA 12.8 (Experimental)
echo.
echo NOTE: CUDA 12.1 works for ALL GPUs including RTX 50-series.
echo       Only choose option 2 if you specifically need CUDA 12.8.
echo.
set /p gpu_choice="Enter choice [1 or 2]: "

echo.
if "%gpu_choice%"=="1" (
    echo Installing PyTorch with CUDA 12.1...
    pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    if errorlevel 1 (
        echo ERROR: Failed to install PyTorch
        pause
        exit /b 1
    )
    echo   [OK] PyTorch (CUDA 12.1) installed
) else if "%gpu_choice%"=="2" (
    echo.
    echo ==========================================
    echo OPTION 2 SELECTED - CUDA 12.8
    echo ==========================================
    echo.
    echo Installing PyTorch with CUDA 12.8 (nightly build for RTX 50-series)...
    echo Command: pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu128
    echo.
    echo Starting installation... Please wait...
    echo.

    pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu128

    echo.
    echo.
    echo Checking installation result...

    if errorlevel 1 (
        echo.
        echo ==========================================
        echo ERROR: PyTorch Installation Failed
        echo ==========================================
        echo.
        echo The CUDA 12.8 installation did not complete successfully.
        echo.
        echo RECOMMENDATION: Press any key to close this window, then run
        echo setup.bat again and choose option 1 instead.
        echo.
        echo CUDA 12.1 works perfectly with ALL GPUs including RTX 50-series.
        echo You do not need CUDA 12.8 for RTX 50-series cards.
        echo.
        pause
        exit /b 1
    )

    echo.
    echo [OK] PyTorch (CUDA 12.8) installed successfully
    echo.
    echo Updating bitsandbytes for RTX 50-series support...

    pip install -U bitsandbytes

    if errorlevel 1 (
        echo.
        echo WARNING: Failed to update bitsandbytes
        echo This might cause issues, but you can continue.
        echo.
    ) else (
        echo [OK] bitsandbytes updated
    )
    echo.
) else (
    echo Invalid choice. Defaulting to CUDA 12.1...
    pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    if errorlevel 1 (
        echo ERROR: Failed to install PyTorch
        pause
        exit /b 1
    )
    echo   [OK] PyTorch (CUDA 12.1) installed
)

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo To start Fluxgym:
echo   1. Activate the virtual environment: env\Scripts\activate
echo   2. Run the application: python app.py
echo.
echo The application will be available at http://localhost:7860
echo.
pause
