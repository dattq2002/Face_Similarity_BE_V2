FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY face_similarity.py .
RUN mkdir -p temp

EXPOSE 5000
CMD ["python", "face_similarity.py"]