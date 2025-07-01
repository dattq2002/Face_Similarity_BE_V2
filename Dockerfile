cat > Dockerfile << 'EOF'
FROM ubuntu:20.04

# Tránh interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Cài Python và pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY face_similarity.py .
RUN mkdir -p temp

EXPOSE 5000
CMD ["python3", "face_similarity.py"]
EOF