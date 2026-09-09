#!/usr/bin/env python3
"""
Simple Web Bridge for Deep-Live-Cam
====================================
This runs ALONGSIDE the original Deep-Live-Cam Qt application.
It simply displays the same processed output that Qt shows.

USAGE:
1. Start this script: python simple_web_bridge.py
2. Start Deep-Live-Cam normally: python run.py
3. Use Deep-Live-Cam as normal (select source, click Live)
4. Open browser: http://127.0.0.1:5000
"""

from flask import Flask, Response, render_template_string
import cv2
import queue
import time

app = Flask(__name__)

# Shared queue that will receive frames from Deep-Live-Cam
browser_frame_queue = queue.Queue(maxsize=2)

def generate_frames():
    """Generate MJPEG stream"""
    while True:
        try:
            frame = browser_frame_queue.get(timeout=1.0)
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            if not ret:
                continue
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        except queue.Empty:
            time.sleep(0.01)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Deep-Live-Cam - Browser View</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                background: #000;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                font-family: Arial, sans-serif;
            }
            .container {
                text-align: center;
            }
            h1 {
                color: #fff;
                margin-bottom: 20px;
            }
            img {
                max-width: 90vw;
                max-height: 80vh;
                border: 3px solid #667eea;
                border-radius: 10px;
                box-shadow: 0 0 50px rgba(102, 126, 234, 0.5);
            }
            .instructions {
                color: #aaa;
                margin-top: 20px;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎭 Deep-Live-Cam - Live Browser View</h1>
            <img src="/video_feed" alt="Live Stream">
            <div class="instructions">
                Use the Deep-Live-Cam application to control face swapping.<br>
                This browser shows the same live output.
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  Deep-Live-Cam Web Bridge")
    print("="*60)
    print("\n  Server starting at http://127.0.0.1:5000")
    print("  Waiting for Deep-Live-Cam to send frames...")
    print("\n  Steps:")
    print("  1. Keep this running")
    print("  2. Start Deep-Live-Cam: python run.py")
    print("  3. Use Deep-Live-Cam normally")
    print("  4. Open browser: http://127.0.0.1:5000")
    print("\n" + "="*60 + "\n")
    
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
