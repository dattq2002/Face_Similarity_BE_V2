FROM python:3.9-slim

WORKDIR /face_similarity_be_v2

# Cài system dependencies cho OpenCV và DeepFace
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgthread-2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements và cài packages
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy app code
COPY face_similarity.py .
COPY . .

# Tạo temp folder
RUN mkdir -p temp

# Set Flask environment
ENV FLASK_APP=face_similarity.py
ENV FLASK_ENV=production

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]