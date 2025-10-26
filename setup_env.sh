#!/bin/bash

# Setup script for Hands-On Machine Learning project
# This script creates a virtual environment and installs dependencies

echo "Hands-On Machine Learning - Environment Setup"
echo "=============================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Error: python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created successfully!"
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo ""
echo "=============================================="
echo "Setup complete! Your environment is ready."
echo ""
echo "To activate the virtual environment later, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run the data fetching script:"
echo "  python end-to-end/get/get_data.py"
echo "=============================================="
