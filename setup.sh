#!/bin/bash
set -e

echo "=========================================="
echo "Fluxgym Setup Script (Linux/Mac)"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $PYTHON_VERSION"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "ERROR: Git is not installed. Please install Git first."
    exit 1
fi
echo "✓ Found Git"
echo ""

# Check if sd-scripts exists, clone if not
if [ ! -d "sd-scripts" ]; then
    echo "sd-scripts directory not found. Cloning from GitHub..."
    git clone -b sd3 https://github.com/kohya-ss/sd-scripts
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to clone sd-scripts repository"
        exit 1
    fi
    echo "  ✓ sd-scripts cloned successfully"
else
    echo "✓ Found sd-scripts directory"
fi
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "env" ]; then
    echo "  Virtual environment already exists. Skipping creation."
else
    python3 -m venv env
    echo "  ✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source env/bin/activate
echo "  ✓ Virtual environment activated"
echo ""

# Upgrade pip, setuptools, and wheel
echo "Upgrading pip, setuptools, and wheel..."
python3 -m pip install --upgrade pip setuptools wheel
echo "  ✓ pip tools upgraded"
echo ""

# Install sd-scripts dependencies
echo "Installing sd-scripts dependencies..."
cd sd-scripts
pip install --prefer-binary -r requirements.txt
cd ..
echo "  ✓ sd-scripts dependencies installed"
echo ""

# Install fluxgym dependencies
echo "Installing fluxgym dependencies..."
pip install --prefer-binary -r requirements.txt
echo "  ✓ fluxgym dependencies installed"
echo ""

# Ask about GPU type
echo "=========================================="
echo "PyTorch Installation"
echo "=========================================="
echo ""
echo "Select your GPU type:"
echo "  1) Standard NVIDIA GPU (RTX 30-series, 40-series, etc.) - CUDA 12.1"
echo "  2) NVIDIA RTX 50-series (5090, etc.) - CUDA 12.8"
echo ""
read -p "Enter choice [1 or 2]: " gpu_choice

echo ""
case $gpu_choice in
    1)
        echo "Installing PyTorch with CUDA 12.1..."
        pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121
        echo "  ✓ PyTorch (CUDA 12.1) installed"
        ;;
    2)
        echo "Installing PyTorch with CUDA 12.8..."
        pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu128
        echo "  ✓ PyTorch (CUDA 12.8) installed"
        echo ""
        echo "Updating bitsandbytes for RTX 50-series support..."
        pip install -U bitsandbytes
        echo "  ✓ bitsandbytes updated"
        ;;
    *)
        echo "Invalid choice. Defaulting to CUDA 12.1..."
        pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121
        echo "  ✓ PyTorch (CUDA 12.1) installed"
        ;;
esac

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To start Fluxgym:"
echo "  1. Activate the virtual environment: source env/bin/activate"
echo "  2. Run the application: python app.py"
echo ""
echo "The application will be available at http://localhost:7860"
echo ""
