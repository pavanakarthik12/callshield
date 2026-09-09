# Phase 1 Quick Start Guide

## 3 Steps to Get Deep-Live-Cam Output in Browser

### Step 1: Start Deep-Live-Cam

**Double-click:** `start_browser_stream.bat`

**Or run:**
```powershell
python run.py
```

### Step 2: Configure Face Swap

In the Deep-Live-Cam window:

1. **Click "Select a face"** → Choose a SOURCE face image
2. **Click "Live"** button
3. **Select your camera** from the dropdown

Wait 10-30 seconds for the preview window to appear.

### Step 3: View in Browser

**Browser opens automatically!**

If it doesn't:
- Double-click: `open_browser.bat`
- Or go to: http://127.0.0.1:5000

## That's It!

You should now see:

✅ **Qt Preview Window** - Shows live face-swapped output  
✅ **Browser Window** - Shows SAME live face-swapped output  

Both update in real-time as you move.

---

## Troubleshooting

### Browser didn't open automatically?

Run: `open_browser.bat`

### Browser shows "Connection refused"?

Wait a few seconds for the server to start, then refresh.

### Browser shows black screen?

- Make sure Qt preview is working first
- Verify you selected a SOURCE face
- Wait 30 seconds for processing to start

### Want to verify setup?

Run:
```powershell
python verify_phase1.py
```

Should show: `✓ ALL CHECKS PASSED`

---

## What You're Seeing

The browser displays the **ACTUAL live face-swapped output** from Deep-Live-Cam.

**Not** your original face.  
**Not** a recording.  
**The real processed stream.**

---

## Files You Can Run

| File | What It Does |
|------|--------------|
| `start_browser_stream.bat` | Start Deep-Live-Cam |
| `open_browser.bat` | Open browser (if already running) |
| `verify_phase1.py` | Verify installation |
| `test_browser_open.py` | Test browser auto-open |

---

## Need More Info?

- **Quick reference:** `PHASE1_README.md`
- **Detailed guide:** `PHASE1_INSTRUCTIONS.md`
- **Technical details:** `PHASE1_SUMMARY.md`

---

**Phase 1 Status:** ✅ Complete

Browser automatically opens when you click "Live"!
