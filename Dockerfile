FROM python:3.9-slim

# Cài đặt các thư viện cần thiết
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Tạo thư mục làm việc
WORKDIR /face_similarity_BE_V2

# Cài thư viện Python
RUN pip install --no-cache-dir flask flask-cors deepface opencv-python-headless tf-keras gunicorn

# Copy source code vào container
COPY . /face_similarity_BE_V2

# Expose cổng để ứng dụng lắng nghe
EXPOSE 5000

# Dùng Gunicorn để chạy Flask app trong production
# Giả sử trong file face_similarity.py có: app = Flask(__name__)
CMD ["gunicorn", "-w", "1", "-t", "300", "-b", "0.0.0.0:5000", "face_similarity:app"]

