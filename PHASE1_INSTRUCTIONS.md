# Phase 1: Deep-Live-Cam Browser Stream

## What This Does

Phase 1 makes Deep-Live-Cam's **ACTUAL live face-swapped output** available in a web browser without modifying its core functionality.

## Architecture

```
TARGET (webcam)
    ↓
Deep-Live-Cam Face Swap Engine
    ↓
Processed Frames
    ↓
    ├─→ Qt Preview Window (original)
    └─→ Web Stream Queue → Flask Server → Browser
```

## What Was Changed

### 1. Added Web Stream Server (`web_stream_server.py`)
- Minimal Flask server
- Receives processed frames via shared queue
- Streams as MJPEG to browser
- **Does NOT modify face-swapping logic**

### 2. Modified `modules/ui.py` (minimal changes)
- Added import for web stream queue
- Modified `_ProcessingWorker` to push processed frames to web queue
- Added web server startup when webcam preview opens
- **No changes to face-swapping pipeline**

### 3. Added Flask dependency
- Added `flask>=3.0.0` to `requirements.txt`

## How to Use

### 1. Install Flask (if not already installed)

```powershell
# Activate your venv if you have one
venv\Scripts\activate

# Install Flask
pip install flask
```

### 2. Start Deep-Live-Cam

```powershell
python run.py
```

### 3. Use Deep-Live-Cam Normally

1. Select a **SOURCE** face image (the face to apply)
2. Click **"Live"** button
3. Select your webcam/camera
4. Wait for the preview to appear (10-30 seconds)

### 4. Browser Opens Automatically

When you click "Live", the browser **automatically opens** to http://127.0.0.1:5000 after 1.5 seconds.

You'll see console output:

```
============================================================
  BROWSER STREAM ENABLED
============================================================
[Web Stream] Starting server at http://127.0.0.1:5000
  Opening browser at http://127.0.0.1:5000
  to view the live face-swapped output
============================================================
```

**If browser doesn't open automatically:**
- Run `open_browser.bat` 
- Or manually navigate to: **http://127.0.0.1:5000**

## What You'll See

### In Deep-Live-Cam Window:
- Original TARGET/SOURCE controls
- "Live" button
- Live preview window (Qt) - **works as before**

### In Browser (http://127.0.0.1:5000):
- **ACTUAL live face-swapped output**
- Same processed frames shown in Qt preview
- Real-time stream as target moves

## Verification

The browser receives the **ACTUAL processed output** because:

1. `_ProcessingWorker.run()` in `ui.py` line ~1090-1190:
   - Captures raw frames from webcam
   - Runs face detection
   - Runs face swapping via `fp.swap_face()`
   - Runs face enhancement
   - Produces `temp_frame` (processed output)

2. Line ~1192-1220:
   - Pushes `temp_frame` to Qt preview queue (original)
   - **ALSO pushes same `temp_frame` to web queue** (new)

3. `web_stream_server.py`:
   - Receives frames from web queue
   - Encodes as JPEG
   - Streams to browser via MJPEG

## Key Files

| File | Purpose | Changed? |
|------|---------|----------|
| `modules/core.py` | Face-swapping engine | ❌ No |
| `modules/processors/frame/face_swapper.py` | Face swap logic | ❌ No |
| `modules/face_analyser.py` | Face detection | ❌ No |
| `modules/ui.py` | UI and preview | ✅ Yes (minimal) |
| `web_stream_server.py` | Browser stream server | ✅ New |

## What's NOT Included (Phase 2+)

- ❌ WebRTC
- ❌ Peer-to-peer connection
- ❌ Host/Client mode
- ❌ Video call functionality
- ❌ CallShield features
- ❌ Virtual camera
- ❌ OBS integration

Phase 1 only makes the existing output available in browser.

## Troubleshooting

### Browser shows black screen
- Check that Deep-Live-Cam "Live" preview is working
- Verify you selected a SOURCE face image
- Wait 10-30 seconds for processing to start

### "Connection refused" in browser
- Check console for "BROWSER STREAM ENABLED" message
- Verify Flask started: look for "[Web Stream] Starting server"
- Try closing and reopening browser

### Frames not updating
- Verify Qt preview window shows live updates
- Check that face swapping is working in Qt preview
- Refresh browser page

## Success Criteria

Phase 1 is complete when:

✅ Deep-Live-Cam starts normally  
✅ You select TARGET (webcam) using original controls  
✅ You select SOURCE face using original controls  
✅ You click "Live" button  
✅ Qt preview window shows live face-swapped output  
✅ Browser at http://127.0.0.1:5000 shows **SAME** live output  
✅ Browser output updates as target moves  
✅ No OBS or virtual camera required  
✅ Original Deep-Live-Cam functionality intact  

## Technical Details

### Frame Flow

```python
# In _ProcessingWorker.run() - modules/ui.py

# 1. Get raw frame from webcam
frame = self._cq.get(timeout=0.05)
temp_frame = frame

# 2. Apply face swapping (ORIGINAL Deep-Live-Cam logic)
for fp in frame_processors:
    if fp.NAME == "DLC.FACE-SWAPPER":
        temp_frame = fp.swap_face(source_image, target_face, temp_frame)

# 3. Send to Qt preview (ORIGINAL)
self._pq.put_nowait(temp_frame)

# 4. Send to web stream (NEW - Phase 1 addition)
web_stream_queue.put_nowait(temp_frame.copy())
```

### Web Server

```python
# web_stream_server.py

# Minimal Flask server
# - Receives processed frames from queue
# - Encodes as JPEG
# - Streams via multipart/x-mixed-replace (MJPEG)
# - No modification to Deep-Live-Cam logic
```

## Port Configuration

Default: `http://127.0.0.1:5000`

To change port, edit `modules/ui.py` line ~1307:

```python
start_web_stream_thread(host='127.0.0.1', port=5000)  # Change port here
```
