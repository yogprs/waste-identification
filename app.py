from flask import Flask, request, jsonify, render_template
from detection import detect_trash
from flask_socketio import SocketIO, emit
import base64
import os
import numpy as np
import cv2

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

UPLOAD_FOLDER = "image-scan"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/scan')
def scan():
    return render_template('scan.html')

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    return jsonify({"message": "Upload berhasil"})

@app.route("/camera")
def camera():
    return render_template("camera.html")

# @app.route('/set_camera', methods=['POST'])
# def change_camera():
#     global camera_index
#     camera_index = int(request.form.get('camera_index'))
#     set_camera(camera_index)
#     return "OK"

@app.route("/live")
def live():
    return render_template("livescan.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json.get('image', None)

        if not data:
            return jsonify({"error": "No image"}), 400

        if "," not in data:
            return jsonify({"error": "Format salah"}), 400

        encoded = data.split(',')[1]

        if not encoded:
            return jsonify({"error": "Base64 kosong"}), 400

        img = base64.b64decode(encoded)

        if len(img) == 0:
            return jsonify({"error": "Decode gagal"}), 400
        
        print("Image length:", len(img))

        np_arr = np.frombuffer(img, np.uint8)

        if np_arr.size == 0:
            return jsonify({"error": "Numpy kosong"}), 400

        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({"error": "Frame None"}), 400

        result = detect_trash(frame)
        print(result[1])
        return jsonify({
            "status": "Success",
            # "data": {
            #     "image": result[0],
            #     "text": result[1]
            # }
        })
        # return jsonify({"status": "ok"})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500
    
@socketio.on('image')
def handle_image(data):
    try:
        if isinstance(data, dict):
            image_data = data.get('image', None)
        else:
            image_data = data

        if not image_data:
            return

        if "," in image_data:
            encoded = image_data.split(',')[1]
        else:
            encoded = image_data

        img_bytes = base64.b64decode(encoded)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if frame is not None:
            result_frame, label = detect_trash(frame)
            
            # Encode frame back to base64
            _, buffer = cv2.imencode('.jpg', result_frame)
            base64_result = base64.b64encode(buffer).decode('utf-8')
            output_image = "data:image/jpeg;base64," + base64_result

            emit('response_back', {'image': output_image})

    except Exception as e:
        print("Socket error:", str(e))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3000, debug=True)