#!/usr/bin/env python3
"""
Web UI Server for Deep-Live-Cam
================================
Complete browser-based interface for Deep-Live-Cam.
All controls and video output available in the browser.
"""

from flask import Flask, render_template, Response, request, jsonify
import cv2
import queue
import threading
import time
import os
import base64
import numpy as np
from pathlib import Path

# Import Deep-Live-Cam modules
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import modules.globals
from modules.face_analyser import get_one_face, detect_one_face_fast, detect_many_faces_fast, ensure_landmarks
from modules.video_capture import VideoCapturer
from modules.processors.frame.core import get_frame_processors_modules
from modules.core import suggest_execution_providers, limit_resources
from modules import imread_unicode

app = Flask(__name__)
app.config['SECRET_KEY'] = 'deep-live-cam-web-ui'

# Global state
state = {
    'source_path': None,
    'source_image': None,
    'camera_active': False,
    'camera_index': 0,
    'frame_processors': [],
    'capture_worker': None,
    'processing_worker': None,
    'stop_event': None,
    'processed_queue': None,
    'many_faces': False,
    'live_mirror': False,
    'show_fps': True,
}

class WebCaptureWorker(threading.Thread):
    """Captures frames from webcam"""
    def __init__(self, cap, capture_queue, stop_event):
        super().__init__(daemon=True)
        self.cap = cap
        self.capture_queue = capture_queue
        self.stop_event = stop_event

    def run(self):
        # Initialize COM for this thread (required for pygrabber on Windows)
        import platform
        if platform.system() == "Windows":
            import pythoncom
            pythoncom.CoInitialize()
        
        try:
            while not self.stop_event.is_set():
                ret, frame = self.cap.read()
                if ret and frame is not None:
                    try:
                        self.capture_queue.put_nowait(frame)
                    except queue.Full:
                        try:
                            self.capture_queue.get_nowait()
                        except queue.Empty:
                            pass
                        try:
                            self.capture_queue.put_nowait(frame)
                        except queue.Full:
                            pass
                time.sleep(0.001)
        finally:
            # Uninitialize COM when thread exits
            if platform.system() == "Windows":
                pythoncom.CoUninitialize()

class WebProcessingWorker(threading.Thread):
    """Processes frames with face swapping"""
    def __init__(self, capture_queue, processed_queue, stop_event, camera_fps):
        super().__init__(daemon=True)
        self.capture_queue = capture_queue
        self.processed_queue = processed_queue
        self.stop_event = stop_event
        self.camera_fps = camera_fps

    def run(self):
        # Initialize COM for this thread (required on Windows)
        import platform
        if platform.system() == "Windows":
            import pythoncom
            pythoncom.CoInitialize()
        
        try:
            from modules.gpu_processing import gpu_flip
            
            frame_processors = get_frame_processors_modules(modules.globals.frame_processors)
            prev_time = time.time()
            frame_count = 0
            fps = 0.0
            det_count = 0
            cached_target_face = None
            cached_many_faces = None
            det_interval = max(1, round(self.camera_fps * 0.08))

            while not self.stop_event.is_set():
                try:
                    frame = self.capture_queue.get(timeout=0.05)
                except queue.Empty:
                    continue

                temp_frame = frame
                if state.get('live_mirror', False):
                    temp_frame = gpu_flip(temp_frame, 1)

                if not modules.globals.map_faces:
                    source_image = state.get('source_image')
                    
                    det_count += 1
                    if det_count % det_interval == 0:
                        if state.get('many_faces', False):
                            cached_target_face = None
                            cached_many_faces = detect_many_faces_fast(temp_frame)
                        else:
                            cached_target_face = detect_one_face_fast(temp_frame)
                            cached_many_faces = None

                    cached_faces = None
                    if cached_many_faces:
                        cached_faces = cached_many_faces
                    elif cached_target_face is not None:
                        cached_faces = [cached_target_face]

                    for fp in frame_processors:
                        if fp.NAME == "DLC.FACE-SWAPPER":
                            swapped_bboxes = []
                            if state.get('many_faces', False) and cached_many_faces:
                                result = temp_frame.copy()
                                for t_face in cached_many_faces:
                                    result = fp.swap_face(source_image, t_face, result)
                                    if hasattr(t_face, "bbox") and t_face.bbox is not None:
                                        swapped_bboxes.append(t_face.bbox.astype(int))
                                temp_frame = result
                            elif cached_target_face is not None:
                                temp_frame = fp.swap_face(source_image, cached_target_face, temp_frame)
                                if hasattr(cached_target_face, "bbox") and cached_target_face.bbox is not None:
                                    swapped_bboxes.append(cached_target_face.bbox.astype(int))
                            temp_frame = fp.apply_post_processing(temp_frame, swapped_bboxes)
                        elif fp.NAME == "DLC.FACE-ENHANCER":
                            if modules.globals.fp_ui.get("face_enhancer", False):
                                temp_frame = fp.process_frame(None, temp_frame, detected_faces=cached_faces)

                current_time = time.time()
                frame_count += 1
                if current_time - prev_time >= 0.5:
                    fps = frame_count / (current_time - prev_time)
                    frame_count = 0
                    prev_time = current_time

                if state.get('show_fps', True):
                    cv2.putText(temp_frame, f"FPS: {fps:.1f}", (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                try:
                    self.processed_queue.put_nowait(temp_frame)
                except queue.Full:
                    try:
                        self.processed_queue.get_nowait()
                    except queue.Empty:
                        pass
                    try:
                        self.processed_queue.put_nowait(temp_frame)
                    except queue.Full:
                        pass
        finally:
            # Uninitialize COM when thread exits
            if platform.system() == "Windows":
                pythoncom.CoUninitialize()

def generate_frames():
    """Generate MJPEG stream from processed frames"""
    while True:
        if state['processed_queue'] is None:
            time.sleep(0.1)
            continue
        
        try:
            frame = state['processed_queue'].get(timeout=1.0)
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            if not ret:
                continue
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        except queue.Empty:
            continue

@app.route('/')
def index():
    """Main web UI"""
    return render_template('full_ui.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/upload_source', methods=['POST'])
def upload_source():
    """Upload source face image"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save to temp location
    temp_dir = Path('temp_uploads')
    temp_dir.mkdir(exist_ok=True)
    filepath = temp_dir / file.filename
    file.save(str(filepath))
    
    # Load source face
    try:
        source_face = get_one_face(imread_unicode(str(filepath)))
        if source_face is None:
            return jsonify({'error': 'No face detected in image'}), 400
        
        state['source_path'] = str(filepath)
        state['source_image'] = source_face
        modules.globals.source_path = str(filepath)
        
        return jsonify({'success': True, 'message': 'Source face loaded'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/start_camera', methods=['POST'])
def start_camera():
    """Start camera and processing"""
    # Initialize COM for this thread (required for pygrabber on Windows)
    import platform
    if platform.system() == "Windows":
        import pythoncom
        pythoncom.CoInitialize()
    
    try:
        print("\n[DEBUG] start_camera endpoint called")
        data = request.json
        camera_index = data.get('camera_index', 0)
        options = data.get('options', {})
        print(f"[DEBUG] Camera index: {camera_index}")
        print(f"[DEBUG] Options: {options}")
        
        if state['camera_active']:
            print("[DEBUG] Camera already active")
            return jsonify({'error': 'Camera already active'}), 400
        
        if state['source_image'] is None:
            print("[DEBUG] No source image")
            return jsonify({'error': 'Please upload a source face first'}), 400
        
        print("[DEBUG] Initializing modules...")
        # Initialize modules with all options
        modules.globals.frame_processors = ['face_swapper']
        modules.globals.execution_providers = suggest_execution_providers()
        modules.globals.execution_threads = 4
        modules.globals.map_faces = False
        modules.globals.many_faces = options.get('many_faces', False)
        modules.globals.live_mirror = options.get('live_mirror', False)
        modules.globals.show_fps = options.get('show_fps', True)
        modules.globals.poisson_blend = options.get('poisson_blend', False)
        modules.globals.color_correction = options.get('color_correction', False)
        
        # Face enhancer options
        enhancer = options.get('enhancer', 'none')
        modules.globals.fp_ui = {
            'face_enhancer': enhancer == 'gfpgan',
            'face_enhancer_gpen512': enhancer == 'gpen512',
            'face_enhancer_gpen256': enhancer == 'gpen256'
        }
        
        # Store refinement options in state
        state['transparency'] = options.get('transparency', 1.0)
        state['sharpness'] = options.get('sharpness', 0.0)
        state['mouth_mask'] = options.get('mouth_mask', 0.0)
        state['many_faces'] = options.get('many_faces', False)
        state['live_mirror'] = options.get('live_mirror', False)
        state['show_fps'] = options.get('show_fps', True)
        
        print("[DEBUG] Initializing frame processors...")
        # Initialize frame processors
        for fp in get_frame_processors_modules(modules.globals.frame_processors):
            print(f"[DEBUG] Pre-starting {fp.NAME}...")
            if not fp.pre_start():
                print(f"[DEBUG] Failed to start {fp.NAME}")
                return jsonify({'error': f'Failed to start {fp.NAME}'}), 500
        
        print(f"[DEBUG] Starting camera {camera_index}...")
        # Start camera (COM must be initialized before this)
        cap = VideoCapturer(camera_index)
        if not cap.start(640, 480, 30):
            print("[DEBUG] Failed to start camera")
            return jsonify({'error': 'Failed to start camera'}), 500
        
        print(f"[DEBUG] Camera started: {cap.actual_width}x{cap.actual_height}@{cap.actual_fps}fps")
        
        # Create queues and workers
        capture_queue = queue.Queue(maxsize=2)
        processed_queue = queue.Queue(maxsize=2)
        stop_event = threading.Event()
        
        print("[DEBUG] Creating workers...")
        capture_worker = WebCaptureWorker(cap, capture_queue, stop_event)
        processing_worker = WebProcessingWorker(capture_queue, processed_queue, stop_event, cap.actual_fps)
        
        print("[DEBUG] Starting workers...")
        capture_worker.start()
        processing_worker.start()
        
        # Update state
        state['camera_active'] = True
        state['camera_index'] = camera_index
        state['capture_worker'] = capture_worker
        state['processing_worker'] = processing_worker
        state['stop_event'] = stop_event
        state['processed_queue'] = processed_queue
        state['cap'] = cap
        
        print("[DEBUG] Camera started successfully!")
        return jsonify({'success': True, 'message': 'Camera started'})
    except Exception as e:
        print(f"[DEBUG] Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        # Uninitialize COM when request completes
        if platform.system() == "Windows":
            pythoncom.CoUninitialize()

@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    """Stop camera and processing"""
    if not state['camera_active']:
        return jsonify({'error': 'Camera not active'}), 400
    
    try:
        state['stop_event'].set()
        state['cap'].release()
        state['camera_active'] = False
        state['processed_queue'] = None
        
        return jsonify({'success': True, 'message': 'Camera stopped'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/toggle_many_faces', methods=['POST'])
def toggle_many_faces():
    """Toggle many faces mode"""
    data = request.json
    state['many_faces'] = data.get('enabled', False)
    modules.globals.many_faces = state['many_faces']
    return jsonify({'success': True})

@app.route('/toggle_mirror', methods=['POST'])
def toggle_mirror():
    """Toggle mirror mode"""
    data = request.json
    state['live_mirror'] = data.get('enabled', False)
    return jsonify({'success': True})

@app.route('/status')
def status():
    """Get current status"""
    return jsonify({
        'camera_active': state['camera_active'],
        'source_loaded': state['source_image'] is not None,
        'many_faces': state.get('many_faces', False),
        'live_mirror': state.get('live_mirror', False),
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  Deep-Live-Cam Web UI Server")
    print("="*60)
    print("\n  Starting server at http://127.0.0.1:5000")
    print("  Open your browser to access the interface")
    print("\n" + "="*60 + "\n")
    
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
