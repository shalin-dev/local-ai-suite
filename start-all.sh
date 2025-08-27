#!/bin/bash

# Local AI Application Suite - Startup Script
# Starts all AI applications in Docker containers

set -e

echo "🚀 Starting Local AI Application Suite..."
echo "========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if port is in use
check_port() {
    if nc -z localhost $1 2>/dev/null; then
        echo -e "${YELLOW}⚠️  Port $1 is already in use${NC}"
        return 1
    fi
    return 0
}

# Function to start an application
start_app() {
    APP_NAME=$1
    APP_DIR=$2
    APP_PORTS=$3
    
    echo -e "\n${GREEN}Starting $APP_NAME...${NC}"
    
    # Check ports
    for PORT in $APP_PORTS; do
        if ! check_port $PORT; then
            echo -e "${RED}❌ Cannot start $APP_NAME - port $PORT is in use${NC}"
            return 1
        fi
    done
    
    # Start the application
    if [ -d "$APP_DIR" ]; then
        cd "$APP_DIR"
        if [ -f "docker-compose.yml" ]; then
            docker-compose up -d
            echo -e "${GREEN}✅ $APP_NAME started successfully${NC}"
        else
            echo -e "${YELLOW}⚠️  No docker-compose.yml found for $APP_NAME${NC}"
        fi
        cd ..
    else
        echo -e "${RED}❌ Directory $APP_DIR not found${NC}"
    fi
}

# Start each application
echo -e "\n📱 Starting applications..."

# 1. Personal AI Assistant Dashboard
start_app "Personal AI Assistant Dashboard" \
    "personal-ai-assistant-dashboard" \
    "8000 3000 5432 6379"

# 2. AI Code Documentation Generator
start_app "AI Code Documentation Generator" \
    "ai-code-documentation-generator" \
    "8001 3001 6380 11435"

# 3. Local RAG System
start_app "Local RAG System" \
    "local-rag-system" \
    "8002 8003 3002 11436"

# 4. AI Image Classifier
start_app "AI Image Classifier" \
    "ai-image-classifier" \
    "8004 3003 5433 6381"

# Wait for services to be ready
echo -e "\n⏳ Waiting for services to be ready..."
sleep 10

# Check status
echo -e "\n📊 Checking application status..."
echo "========================================="

# Function to check if service is running
check_service() {
    SERVICE_NAME=$1
    SERVICE_URL=$2
    
    if curl -s "$SERVICE_URL" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ $SERVICE_NAME is running${NC}"
        return 0
    else
        echo -e "${RED}❌ $SERVICE_NAME is not responding${NC}"
        return 1
    fi
}

# Check each service
check_service "AI Assistant API" "http://localhost:8000/health"
check_service "AI Assistant UI" "http://localhost:3000"
check_service "Code Doc Generator" "http://localhost:8001/health"
check_service "RAG System" "http://localhost:8002/health"
check_service "Image Classifier" "http://localhost:8004/health"

# Display access URLs
echo -e "\n🌐 Access URLs:"
echo "========================================="
echo "AI Assistant Dashboard: http://localhost:3000"
echo "Code Documentation Generator: http://localhost:3001"
echo "Local RAG System: http://localhost:3002"
echo "AI Image Classifier: http://localhost:3003"
echo ""
echo "API Endpoints:"
echo "- AI Assistant: http://localhost:8000"
echo "- Code Docs: http://localhost:8001"
echo "- RAG System: http://localhost:8002"
echo "- Image Classifier: http://localhost:8004"

echo -e "\n${GREEN}🎉 All applications started successfully!${NC}"
echo "Use './stop-all.sh' to stop all services"