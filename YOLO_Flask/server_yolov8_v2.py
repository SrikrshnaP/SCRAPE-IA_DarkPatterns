import sys
import os
import time
from flask import Flask, send_from_directory, request, jsonify
import webbrowser
import pyautogui
import cv2
import numpy as np
from ultralytics import YOLO

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

import time

# Replace with your model weights and configuration paths
model_path = "best.pt"

# Load the YOLOv8 model
model = YOLO(model_path)  # Use 'cpu' for CPU-only inference

images = {}

def pipeline(model, screenshot):
    print("called")
    image = screenshot.convert("RGB")
    results = model(image)

    # Process results and extract relevant data
    '''
    processed_results = []
    for result in results.pandas().xyxy[0]:
        conf, cls, x_min, y_min, x_max, y_max = result
        processed_results.append({
            "confidence": float(conf),
            "class": int(cls),
            "bbox": {"x_min": int(x_min), "y_min": int(y_min), "x_max": int(x_max), "y_max": int(y_max)}
        })
    '''

    p=""

    for r in results:
        im_array = r.plot()  # plot a BGR numpy array of predictions
        im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
        #im.show()  # show image
        #im.save('yolo_test.png')
        p="1"

    return im , p

app = Flask(__name__)

@app.route('/screenshot_yolo', methods=['POST'])
def screenshot_yolo():
    try:
        time.sleep(1)
        screenshot = pyautogui.screenshot()
        ss , results = pipeline(model, screenshot)

        if results != "":
            ss.show()

        # Generate unique filename and save image temporarily
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"screenshot_{timestamp}.jpg"
        image_path = os.path.join(os.getcwd(), "downloads", filename)
        os.makedirs('downloads', exist_ok=True)
        #cv2.imwrite(image_path, cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR))

        # Return response with results and download URL
        response = {
            "status": "success",
            "results": results,
            "download_url": f"/downloads/{filename}"
        }

        images[filename] = ss

        return jsonify(response)

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'status': 'error', 'message': 'An error occurred during screenshot or object detection.'})


@app.route('/screenshot_yolo', methods=['GET'])
def get_screenshot_results():
    """Retrieves results for a previously captured screenshot.

    Returns:
        JSON response with "status", "results", and "download_url" (if available).
    """
    filename = request.args.get('filename')
    if not filename:
        return jsonify({'status': 'error', 'message': 'Missing filename parameter'}), 400

    if filename not in images:
        return jsonify({'status': 'error', 'message': 'Screenshot not found'}), 404

    #image_path = os.path.join(os.getcwd(), "downloads", filename)
    #os.makedirs('downloads', exist_ok=True)
    #cv2.imwrite(image_path, cv2.cvtColor(np.array(ss), cv2.COLOR_RGB2BGR))

    ss = images[filename]
    ss.show()

    results = None
    download_url = None

    # Access results and download URL based on how you store them
    if ss is not None:
        response = {
            "status": "success",
        }
        return jsonify(response)
    else:
        return jsonify({'status': 'error', 'message': 'Results or download URL not available'}), 404


if __name__ == '__main__':
    # Open the Flask app in the user's default web browser
    webbrowser.open('http://127.0.0.1:5000')
    print("starting")
    app.run(debug=True, host='127.0.0.1', port=5000)
    print("started")
