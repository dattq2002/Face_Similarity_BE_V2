from flask import Flask, request, jsonify
from flask_cors import CORS
from deepface import DeepFace
import shutil
import os
import uuid

app = Flask(__name__)
CORS(app)  # Cho phép CORS tất cả domain

model = None

# @app.before_first_request
# def load_model_once():
#     global model
#     model = DeepFace.build_model("VGG-Face")  # Hoặc "Facenet", "ArcFace" tùy chọn
#     print("✅ Model đã load xong")

@app.route('/')
def index():
    return jsonify(message="Welcome to the Face Similarity API! Use /compare endpoint to compare two images.")

@app.route('/compare', methods=['POST'])
def compare():
    try:
        if 'img1' not in request.files or 'img2' not in request.files:
            return jsonify({'error': 'Missing files'}), 400

        img1_file = request.files['img1']
        img2_file = request.files['img2']

        # Tạo thư mục và tên file tạm
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
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
