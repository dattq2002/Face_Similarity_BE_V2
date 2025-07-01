#!/bin/bash

# Script deploy Face Similarity API

echo "🚀 Starting deployment..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Docker if not exists
if ! command -v docker &> /dev/null; then
    echo "🐳 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
fi

# Install Docker Compose if not exists
if ! command -v docker-compose &> /dev/null; then
    echo "🐙 Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Create project directory
PROJECT_DIR="/opt/face-similarity-api"
echo "📁 Creating project directory: $PROJECT_DIR"
sudo mkdir -p $PROJECT_DIR
sudo chown $USER:$USER $PROJECT_DIR

# Copy files to project directory (assume files are in current directory)
echo "📋 Copying project files..."
cp face_similarity.py $PROJECT_DIR/
cp Dockerfile $PROJECT_DIR/
cp requirements.txt $PROJECT_DIR/
cp docker-compose.yml $PROJECT_DIR/
cp nginx.conf $PROJECT_DIR/

# Create necessary directories
mkdir -p $PROJECT_DIR/temp
mkdir -p $PROJECT_DIR/ssl
mkdir -p $PROJECT_DIR/logs

# Set permissions
chmod +x $PROJECT_DIR/deploy.sh

# Navigate to project directory
cd $PROJECT_DIR

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build and start containers
echo "🏗️ Building and starting containers..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Check if services are running
echo "🔍 Checking service status..."
docker-compose ps

# Test API
echo "🧪 Testing API..."
curl -f http://localhost/health || echo "⚠️ Health check failed"

# Show logs
echo "📋 Recent logs:"
docker-compose logs --tail=20

echo "✅ Deployment completed!"
echo "📡 API is available at:"
echo "   - Local: http://localhost/api/"
echo "   - Health check: http://localhost/health"
echo ""
echo "🔧 Useful commands:"
echo "   - View logs: docker-compose logs -f"
echo "   - Restart: docker-compose restart"
echo "   - Stop: docker-compose down"
echo "   - Update: docker-compose pull && docker-compose up -d"