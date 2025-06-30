FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1

WORKDIR /face_similarity_BE_V2

RUN pip install --no-cache-dir flask flask-cors deepface opencv-python-headless tf-keras

COPY . /face_similarity_BE_V2

EXPOSE 5000

CMD ["python", "face_similarity.py"]
