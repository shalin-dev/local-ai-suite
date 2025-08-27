#!/bin/bash

# Local AI Application Suite - Stop Script
# Stops all AI applications

echo "🛑 Stopping Local AI Application Suite..."
echo "========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to stop an application
stop_app() {
    APP_NAME=$1
    APP_DIR=$2
    
    echo -e "\n${YELLOW}Stopping $APP_NAME...${NC}"
    
    if [ -d "$APP_DIR" ]; then
        cd "$APP_DIR"
        if [ -f "docker-compose.yml" ]; then
            docker-compose down
            echo -e "${GREEN}✅ $APP_NAME stopped${NC}"
        fi
        cd ..
    fi
}

# Stop each application
stop_app "Personal AI Assistant Dashboard" "personal-ai-assistant-dashboard"
stop_app "AI Code Documentation Generator" "ai-code-documentation-generator"
stop_app "Local RAG System" "local-rag-system"
stop_app "AI Image Classifier" "ai-image-classifier"

echo -e "\n${GREEN}✅ All applications stopped successfully!${NC}"