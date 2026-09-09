# Phase 1: Deep-Live-Cam Browser Stream

## TL;DR

Phase 1 makes Deep-Live-Cam's **live face-swapped output** viewable in a web browser.

**Start it:**
```powershell
python run.py
# Click "Live" button
# Open http://127.0.0.1:5000 in browser
```

## What It Does

```
Deep-Live-Cam Face Swap → Browser
```

Your browser displays the **ACTUAL processed output** from Deep-Live-Cam.

## What It Doesn't Do

❌ No WebRTC yet  
❌ No video calls yet  
❌ No host/client yet  
❌ No OBS  
❌ No virtual camera  

Phase 1 = Browser displays Deep-Live-Cam output. That's it.

## Installation

### 1. Install Flask

```powershell
pip install flask
```

### 2. Verify Setup

```powershell
python verify_phase1.py
```

Should show:
```
✓ ALL CHECKS PASSED
```

## Usage

### Method 1: Use Batch File (Windows)

```powershell
start_browser_stream.bat
```

### Method 2: Manual Start

```powershell
# Start Deep-Live-Cam
python run.py

# In the window:
# 1. Select SOURCE face
# 2. Click "Live"
# 3. Select camera

# Browser will open AUTOMATICALLY!
# If it doesn't, manually open: http://127.0.0.1:5000
```

### Browser Auto-Opens

When you click "Live", the browser automatically opens to http://127.0.0.1:5000 after 1.5 seconds (giving Flask time to start).

**If browser doesn't open automatically:**
- Run: `open_browser.bat`
- Or manually navigate to: http://127.0.0.1:5000

## What You'll See

### Deep-Live-Cam Window
- Works exactly as before
- All original controls present
- Original preview window works

### Browser (http://127.0.0.1:5000)
- Shows **SAME** output as Deep-Live-Cam preview
- Updates in real-time
- No delay

## Verification Test

**To verify browser shows ACTUAL swapped output:**

1. Use a distinctive face as SOURCE (e.g., celebrity)
2. Start Live mode
3. Compare:
   - Qt preview = swapped face ✓
   - Browser = swapped face ✓
   - Both should show SAME face

If browser shows YOUR face instead of SOURCE face → something is wrong.

## How It Works

Deep-Live-Cam already produces live face-swapped frames. Phase 1 just taps into those frames and sends them to Flask, which streams to your browser.

**Code changed:** ~35 lines in `modules/ui.py`  
**Core face-swapping:** Completely untouched  

## Files

### New Files
- `web_stream_server.py` - Flask server
- `PHASE1_*.md` - Documentation
- `verify_phase1.py` - Verification
- `start_browser_stream.bat` - Quick start

### Modified Files
- `modules/ui.py` - Minimal changes to tap processed frames
- `requirements.txt` - Added Flask

### Untouched Files (Critical)
- `modules/core.py` - Face-swapping engine
- `modules/processors/frame/face_swapper.py` - Swap logic
- `modules/face_analyser.py` - Detection
- All model files

## Architecture

```
TARGET (webcam)
    ↓
Face Detection (Deep-Live-Cam)
    ↓
Face Swapping (Deep-Live-Cam)
    ↓
Enhancement (Deep-Live-Cam)
    ↓
Processed Frame
    ↓
    ├─→ Qt Preview (original)
    └─→ Web Queue → Flask → Browser (new)
```

## Troubleshooting

### "Connection refused" in browser
- Wait for console message: "BROWSER STREAM ENABLED"
- Check Flask started
- Try http://localhost:5000

### Black/frozen browser display
- Verify Qt preview is working
- Confirm SOURCE face selected
- Wait 10-30 seconds for startup

### Browser shows YOUR face (not swapped)
Phase 1 is NOT working. Check:
- Is face swapping working in Qt preview?
- Did you select a SOURCE face?
- Any console errors?

## Documentation

- `PHASE1_INSTRUCTIONS.md` - Detailed guide
- `PHASE1_SUMMARY.md` - Technical summary
- `PHASE1_README.md` - This file

## Success Criteria

Phase 1 complete when:

✅ Browser shows live face-swapped output  
✅ Output matches Qt preview  
✅ Updates as target moves  
✅ Original Deep-Live-Cam still works  

## Next Phase

Phase 1 provides foundation for:
- Phase 2: WebRTC integration
- Phase 3: Video calls
- Phase 4: CallShield features

But Phase 1 first: Get Deep-Live-Cam output in browser. ✓

## URLs

**Browser Stream:** http://127.0.0.1:5000  
**Change port:** Edit `modules/ui.py` line ~1307

## Support

Run verification:
```powershell
python verify_phase1.py
```

Should show all ✓ checks passed.

## License

Same as Deep-Live-Cam. Phase 1 is an extension, not a replacement.

---

**Phase 1 Status:** ✅ Complete and working
