#!/usr/bin/env python3
"""
Quick test to verify browser auto-open works
"""

import time
import webbrowser
import threading

def test_browser_open():
    print("\n" + "="*60)
    print("  Testing Browser Auto-Open")
    print("="*60)
    print("\nThis will open your browser in 2 seconds...")
    print("URL: http://127.0.0.1:5000")
    print("\nNote: The web server must be running for the page to load.")
    print("="*60 + "\n")
    
    time.sleep(2)
    print("Opening browser now...")
    webbrowser.open('http://127.0.0.1:5000')
    print("✓ Browser opened!")
    print("\nIf your browser didn't open, you may need to:")
    print("  1. Check your default browser settings")
    print("  2. Manually open: http://127.0.0.1:5000")

if __name__ == "__main__":
    test_browser_open()
