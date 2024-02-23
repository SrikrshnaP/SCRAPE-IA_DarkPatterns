import sys
import os
import time
from flask import Flask, send_from_directory, request, jsonify
import webbrowser
import pyautogui
import cv2
import numpy as np
#from pytorch_yolo import Model_Yolo  # Assuming PyTorch YOLO implementation

import time
import datetime
import pyautogui
from PIL import Image
import cv2
import numpy
from ultralytics import YOLO

# Replace with your model weights and configuration paths
model_path = "best.pt"

# Load the YOLOv8 model
model = YOLO(model_path)  # Use 'cpu' for CPU-only inference

def pipeline(model,i):
    screenshot = pyautogui.screenshot()
    image = screenshot.convert("RGB")
    
    results = model(image)
    # print(output)

    for r in results:
        im_array = r.plot()  # plot a BGR numpy array of predictions
        im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
        im.show()  # show image
        im.save('yolo_test.png')

app = Flask(__name__)

@app.route('/screenshot_yolo', methods=['POST'])
def screenshot_yolo():
    try:
        print("trying")
        pipeline(model,0)
        print("happened")
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'status': 'error', 'message': 'An error occurred during screenshot or object detection.'})

if __name__ == '__main__':
    # Open the Flask app in the user's default web browser
    webbrowser.open('http://127.0.0.1:5000')
    print("starting")
    app.run(debug=True, host='127.0.0.1', port=5000)
    print("started")
