FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir flask flask-cors deepface

EXPOSE 5000

CMD ["python", "face_similarity.py"]