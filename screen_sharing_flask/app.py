# screen_sharing_flask/app.py
from flask import Flask, render_template, request, Response
import base64
from io import BytesIO
from PIL import Image
import time

app = Flask(__name__)
frame_data = None  # Global variable to store the latest frame

@app.route('/stream', methods=['POST'])
def stream():
    global frame_data
    data = request.json['data']
    frame_data = data  # Update the latest frame data
    return '', 204

@app.route('/viewer')
def viewer():
    return render_template('viewer.html')

def generate_frames():
    global frame_data
    while True:
        if frame_data:
            # Decode base64 image to binary
            img_data = base64.b64decode(frame_data)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img_data + b'\r\n')
        time.sleep(0.03)  # Adjust frame rate for smoother streaming

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

