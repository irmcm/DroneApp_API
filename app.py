from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import cv2
import numpy as np
import threading
import time

app = Flask(__name__)
CORS(app)

# In-memory drone state & harvest records
drone_state = {
    "battery": 100,
    "camera": "inactive"
}
harvest_records = []

# Video stream variables
current_frame = None
frame_lock = threading.Lock()

def generate_frames():
    """Generate video frames for streaming"""
    while True:
        with frame_lock:
            if current_frame is not None:
                # Encode frame to JPEG
                ret, buffer = cv2.imencode('.jpg', current_frame)
                if ret:
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.1)  # 10 FPS

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/video/upload', methods=['POST'])
def upload_video_frame():
    """Receive video frame from client"""
    global current_frame
    
    try:
        # Get the image data from request
        image_data = request.get_data()
        
        # Convert to numpy array
        nparr = np.frombuffer(image_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is not None:
            with frame_lock:
                current_frame = frame
            return jsonify({"message": "Frame uploaded successfully"}), 200
        else:
            return jsonify({"error": "Invalid image data"}), 400
            
    except Exception as e:
        return jsonify({"error": f"Error processing frame: {str(e)}"}), 500

@app.route('/api/start', methods=['POST'])
def start_drone():
    """
    Example "start" action — still POST for actions, not GET.
    """
    drone_state["camera"] = "active"
    return jsonify({"message": "Drone started"}), 200

@app.route('/api/status', methods=['GET'])
def get_status():
    """
    Returns your current drone_state.
    """
    return jsonify(drone_state), 200

@app.route('/api/harvest', methods=['POST'])
def post_harvest():
    """
    Receive a harvest record from your app.
    Expected JSON body:
      {
        "timestamp": 1749390192,
        "count":     42
      }
    """
    data = request.get_json() or {}
    # simple validation
    for field in ("timestamp", "count"):
        if field not in data:
            return jsonify({"error": f"Missing field '{field}'"}), 400

    # append to our in-memory list
    harvest_records.append({
        "timestamp": data["timestamp"],
        "count":     data["count"]
    })
    return jsonify({"message": "Harvest recorded"}), 201

@app.route('/api/harvests', methods=['GET'])
def get_harvests():
    """
    Return all harvest records.
    """
    return jsonify(harvest_records), 200

@app.route('/')
def index():
    return "Welcome to the Drone API Server!"

if __name__ == '__main__':
    # host='0.0.0.0' so other devices on your LAN can POST/GET
    app.run(debug=True, host='0.0.0.0', port=5001)