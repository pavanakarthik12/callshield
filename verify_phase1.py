#!/usr/bin/env python3
"""
Phase 1 Verification Script
============================
This script verifies that Phase 1 setup is correct.
"""

import sys
import os

def check_file_exists(filepath, description):
    """Check if a file exists"""
    exists = os.path.isfile(filepath)
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {filepath}")
    return exists

def check_module_import(module_name):
    """Check if a module can be imported"""
    try:
        __import__(module_name)
        print(f"✓ {module_name} is installed")
        return True
    except ImportError:
        print(f"✗ {module_name} is NOT installed")
        return False

def main():
    print("\n" + "="*60)
    print("  PHASE 1 VERIFICATION")
    print("="*60 + "\n")
    
    all_good = True
    
    # Check core Deep-Live-Cam files
    print("Checking Deep-Live-Cam core files...")
    all_good &= check_file_exists("run.py", "Main entry point")
    all_good &= check_file_exists("modules/core.py", "Core module")
    all_good &= check_file_exists("modules/ui.py", "UI module")
    all_good &= check_file_exists("modules/processors/frame/face_swapper.py", "Face swapper")
    
    print("\nChecking Phase 1 additions...")
    all_good &= check_file_exists("web_stream_server.py", "Web stream server")
    all_good &= check_file_exists("PHASE1_INSTRUCTIONS.md", "Instructions")
    
    print("\nChecking Python dependencies...")
    all_good &= check_module_import("flask")
    all_good &= check_module_import("cv2")
    all_good &= check_module_import("numpy")
    all_good &= check_module_import("PySide6")
    
    print("\nChecking web_stream_server module...")
    try:
        from web_stream_server import web_stream_queue, start_web_stream_thread
        print("✓ web_stream_server imports successfully")
        print("✓ web_stream_queue is available")
        print("✓ start_web_stream_thread is available")
    except ImportError as e:
        print(f"✗ Failed to import web_stream_server: {e}")
        all_good = False
    
    print("\n" + "="*60)
    if all_good:
        print("  ✓ ALL CHECKS PASSED")
        print("="*60)
        print("\nPhase 1 setup is complete!\n")
        print("To start:")
        print("1. Run: python run.py")
        print("2. Click 'Live' button in Deep-Live-Cam")
        print("3. Open browser: http://127.0.0.1:5000")
        print("\nSee PHASE1_INSTRUCTIONS.md for detailed usage.\n")
        return 0
    else:
        print("  ✗ SOME CHECKS FAILED")
        print("="*60)
        print("\nPlease fix the issues above before proceeding.")
        print("\nIf Flask is missing, install it:")
        print("  pip install flask\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
