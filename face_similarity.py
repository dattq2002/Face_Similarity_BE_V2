from flask import Flask, request, jsonify
from flask_cors import CORS
from deepface import DeepFace
import uuid
import numpy as np
import cv2
import os
import traceback

app = Flask(__name__)
CORS(app)

# ✅ Hàm chuyển file ảnh từ request thành ảnh OpenCV (không lưu vào đĩa)
def read_image(file_storage):
    image_bytes = file_storage.read()
    np_arr = np.frombuffer(image_bytes, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

@app.route('/')
def index():
    return jsonify(message="Welcome to the Face Similarity API! Use POST /compare with img1 & img2.")

@app.route('/compare', methods=['POST'])
def compare():
    try:
        if 'img1' not in request.files or 'img2' not in request.files:
            return jsonify({'error': 'Missing files'}), 400

        img1_file = request.files['img1']
        img2_file = request.files['img2']

        # Tạo thư mục và tên file tạmAdd commentMore actions
        os.makedirs("temp", exist_ok=True)
        img1_path = f"temp/{uuid.uuid4()}.jpg"
        img2_path = f"temp/{uuid.uuid4()}.jpg"

        # Lưu file
        img1_file.save(img1_path)
        img2_file.save(img2_path)

        # Gọi DeepFace
        result = DeepFace.verify(img1_path, img2_path, enforce_detection=False, model_name="VGG-Face")
        distance = result.get("distance", None)
        similarity_percentage = None
        if distance is not None:
            similarity_percentage = round((1 - distance) * 100, 2)

        # Xoá file tạm
        os.remove(img1_path)
        os.remove(img2_path)

        result["similarity_percentage"] = similarity_percentage

        return jsonify(result)

    except Exception as e:
        # ✅ In lỗi chi tiết khi cần debug
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
