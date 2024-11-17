# screen_sharing_flask/screen_capture.py
import mss
import numpy as np
import cv2
import base64
import time
import requests

SERVER_URL = 'http://localhost:5000/stream'  # Flask server URL

def capture_and_send():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Capture the primary monitor
        
        while True:
            # Capture the screen
            img = sct.grab(monitor)

            # Convert to a format compatible with OpenCV
            img_np = np.array(img)
            frame = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)

            # Encode as JPEG and convert to base64
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')

            # Send to server
            requests.post(SERVER_URL, json={'data': jpg_as_text})

            # A short delay to control frame rate (adjust as needed for performance)
            time.sleep(0.03)  # About 30 frames per second

if __name__ == '__main__':
    capture_and_send()
