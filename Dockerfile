FROM python:3.9-slim

# Cài đặt các dependencies hệ thống cần thiết cho OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgthread-2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Tạo thư mục làm việc
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Cài đặt Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY face_similarity.py .

# Tạo thư mục temp
RUN mkdir -p temp

# Expose port
EXPOSE 5000

# Chạy ứng dụng
CMD ["python", "face_similarity.py"]