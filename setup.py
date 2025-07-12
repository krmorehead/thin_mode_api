#!/usr/bin/env python3
"""
Setup script for the Flask LLM API
"""

import os
import shutil
import subprocess
import sys
import time

def create_env_file():
    """Create .env file from example.env if it doesn't exist"""
    if not os.path.exists('.env'):
        if os.path.exists('example.env'):
            shutil.copy('example.env', '.env')
            print("✓ Created .env file from example.env")
        else:
            print("✗ example.env not found")
            return False
    else:
        print("✓ .env file already exists")
    return True

def install_basic_packages():
    """Install basic packages first"""
    basic_packages = [
        'flask==2.3.3',
        'python-dotenv==1.0.0',
        'requests==2.31.0'
    ]
    
    print("Installing basic packages...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        for package in basic_packages:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        print("✓ Basic packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install basic packages: {e}")
        return False

def install_ml_packages():
    """Install ML packages with fallback options"""
    print("Installing ML packages...")
    
    # Try to install torch first
    try:
        print("Installing PyTorch...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'torch==2.0.1', '--index-url', 'https://download.pytorch.org/whl/cpu'])
        print("✓ PyTorch installed successfully")
    except subprocess.CalledProcessError:
        print("Trying alternative PyTorch installation...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'torch', '--index-url', 'https://download.pytorch.org/whl/cpu'])
            print("✓ PyTorch installed successfully (alternative method)")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install PyTorch: {e}")
            return False
    
    # Try to install transformers
    try:
        print("Installing transformers...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'transformers==4.30.2'])
        print("✓ Transformers installed successfully")
    except subprocess.CalledProcessError:
        print("Trying alternative transformers installation...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'transformers'])
            print("✓ Transformers installed successfully (alternative method)")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install transformers: {e}")
            return False
    
    # Try to install remaining packages
    remaining_packages = [
        'accelerate==0.20.3',
        'protobuf==3.20.3'
    ]
    
    for package in remaining_packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to install {package}: {e}")
            print("Continuing with other packages...")
    
    print("✓ ML packages installation completed")
    return True

def install_dependencies():
    """Install Python dependencies with fallback methods"""
    if not os.path.exists('requirements.txt'):
        print("✗ requirements.txt not found")
        return False

    print("Installing dependencies in phases...")
    
    # Phase 1: Basic packages
    if not install_basic_packages():
        return False
    
    # Phase 2: ML packages
    if not install_ml_packages():
        print("Warning: Some ML packages failed to install")
        print("Trying to install all requirements at once as fallback...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("✓ Dependencies installed successfully via fallback method")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install dependencies: {e}")
            return False
    
    return True

def test_basic_imports():
    """Test if basic imports work"""
    try:
        print("Testing basic imports...")
        import flask
        import dotenv
        import requests
        print("✓ Basic imports successful")
        return True
    except ImportError as e:
        print(f"✗ Basic imports failed: {e}")
        return False

def test_ml_imports():
    """Test if ML imports work"""
    try:
        print("Testing ML imports...")
        import torch
        import transformers
        print("✓ ML imports successful")
        return True
    except ImportError as e:
        print(f"Warning: ML imports failed: {e}")
        print("The basic Flask app will still work, but ML features may be limited")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected")
    return True

def check_virtual_environment():
    """Check if we're in a virtual environment"""
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    if in_venv:
        print("✓ Virtual environment detected")
    else:
        print("Warning: Not in a virtual environment. Consider using one to avoid conflicts.")
    return True

def main():
    print("Setting up Flask LLM API...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check virtual environment
    check_virtual_environment()
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n" + "=" * 50)
        print("Installation encountered issues!")
        print("Try running these commands manually:")
        print("  pip install --upgrade pip")
        print("  pip install flask python-dotenv requests")
        print("  pip install torch --index-url https://download.pytorch.org/whl/cpu")
        print("  pip install transformers")
        sys.exit(1)
    
    # Test imports
    test_basic_imports()
    test_ml_imports()
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("\nTo start the server:")
    print("  python app.py")
    print("\nTo test the API:")
    print("  python test_api.py")
    print("\nTo customize the model, edit the .env file")
    
    print("\nIf you encounter any issues, try:")
    print("  pip install --upgrade pip")
    print("  pip install -r requirements.txt")

if __name__ == "__main__":
    main() 