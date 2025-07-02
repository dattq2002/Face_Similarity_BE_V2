# Sử dụng Python 3.9 slim image làm base
FROM python:3.9-slim

# Thiết lập biến môi trường
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TF_CPP_MIN_LOG_LEVEL=2 \
    TF_ENABLE_ONEDNN_OPTS=0

# Cài đặt system dependencies cần thiết cho OpenCV và các thư viện khác
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libatlas-base-dev \
    gfortran \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Tạo thư mục làm việc
WORKDIR /app

# Copy requirements và cài đặt Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY face_similarity.py .

# Tạo thư mục temp cho việc xử lý file tạm
RUN mkdir -p temp

# Expose port
EXPOSE 5000

# Tạo user non-root để chạy ứng dụng (bảo mật tốt hơn)
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Command để chạy ứng dụng
CMD ["uvicorn", "face_similarity:app", "--host", "0.0.0.0", "--port", "5000"]