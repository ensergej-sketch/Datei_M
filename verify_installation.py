#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Datei_M Installation Verification Script
Checks if all requirements are met to run the application
"""

import sys
import os

def check_python_version():
    """Check if Python version is sufficient"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python version {version.major}.{version.minor}.{version.micro} is too old")
        print("  Required: Python 3.8 or higher")
        return False

def check_tkinter():
    """Check if tkinter is available"""
    try:
        import tkinter
        print("✓ tkinter is installed")
        return True
    except ImportError:
        print("✗ tkinter is not installed")
        print("  Install it with:")
        print("    - Ubuntu/Debian: sudo apt-get install python3-tk")
        print("    - Fedora: sudo dnf install python3-tkinter")
        print("    - Windows/macOS: Reinstall Python with tcl/tk support")
        return False

def check_modules():
    """Check if all project modules are present"""
    required_files = [
        'main.py',
        'modules/__init__.py',
        'modules/dateien_manager.py',
        'modules/dokumente_manager.py',
        'modules/regex_editor.py',
        'modules/kategorie_manager.py'
    ]
    
    all_present = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} not found")
            all_present = False
    
    return all_present

def main():
    """Main verification function"""
    print("=" * 60)
    print("Datei_M Installation Verification")
    print("=" * 60)
    print()
    
    print("Checking Python version...")
    python_ok = check_python_version()
    print()
    
    print("Checking tkinter...")
    tkinter_ok = check_tkinter()
    print()
    
    print("Checking project files...")
    files_ok = check_modules()
    print()
    
    print("=" * 60)
    if python_ok and tkinter_ok and files_ok:
        print("✓ All checks passed!")
        print("  You can start the application with: python main.py")
        return 0
    else:
        print("✗ Some checks failed")
        print("  Please resolve the issues above before running the application")
        return 1

if __name__ == "__main__":
    sys.exit(main())
