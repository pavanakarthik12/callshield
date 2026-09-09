#!/usr/bin/env python3
"""
Web Stream Server for Deep-Live-Cam
====================================
This module creates a minimal Flask server that streams the processed 
face-swapped output from Deep-Live-Cam to a browser.

CRITICAL: This does NOT replace or modify Deep-Live-Cam's core functionality.
It only taps into the existing processed frame stream and makes it available via HTTP.
"""

import queue
import threading
import cv2
from flask import Flask, Response, render_template_string
import time

app = Flask(__name__)

# Shared queue for web streaming
# This will receive the SAME processed frames that go to the Qt preview
web_stream_queue = queue.Queue(maxsize=2)

def generate_frames():
    """Generator function that yields JPEG frames for MJPEG streaming"""
    while True:
        try:
            # Get processed frame from queue
            frame = web_stream_queue.get(timeout=1.0)
            
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            if not ret:
                continue
            
            # Yield frame in multipart format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        except queue.Empty:
            # No frame available, wait a bit
            time.sleep(0.01)
            continue

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Returns MJPEG stream."""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    """Main page with video stream display"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Deep-Live-Cam - Browser Stream</title>
        <style>
            body {
                margin: 0;
                padding: 20px;
                background-color: #1a1a1a;
                font-family: Arial, sans-serif;
                color: #ffffff;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            h1 {
                margin-bottom: 10px;
            }
            .info {
                margin-bottom: 20px;
                color: #888;
                text-align: center;
            }
            .video-container {
                border: 2px solid #333;
                border-radius: 8px;
                overflow: hidden;
                background-color: #000;
                max-width: 90vw;
                max-height: 80vh;
            }
            img {
                display: block;
                max-width: 100%;
                height: auto;
            }
            .status {
                margin-top: 20px;
                padding: 10px 20px;
                background-color: #2a2a2a;
                border-radius: 4px;
            }
        </style>
    </head>
    <body>
        <h1>Deep-Live-Cam - Live Browser Output</h1>
        <div class="info">
            This is the ACTUAL processed face-swapped output from Deep-Live-Cam<br>
            Use the main Deep-Live-Cam window to select TARGET and SOURCE
        </div>
        <div class="video-container">
            <img src="{{ url_for('video_feed') }}" alt="Live Stream">
        </div>
        <div class="status">
            <strong>Status:</strong> Streaming live processed frames
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

def start_web_server(host='127.0.0.1', port=5000):
    """Start the Flask web server in a separate thread"""
    print(f"\n[Web Stream] Starting server at http://{host}:{port}")
    print(f"[Web Stream] Open your browser to view the live stream")
    app.run(host=host, port=port, debug=False, threaded=True, use_reloader=False)

def start_web_stream_thread(host='127.0.0.1', port=5000):
    """Start web server in background thread"""
    thread = threading.Thread(target=start_web_server, args=(host, port), daemon=True)
    thread.start()
    return thread
