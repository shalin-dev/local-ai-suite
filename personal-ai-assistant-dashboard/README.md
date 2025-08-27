# Personal AI Assistant Dashboard

A unified interface for multiple local AI models with chat, image generation, and code assistance capabilities.

## 🚀 Currently Running

### Backend API
- **URL**: http://localhost:8090
- **Status**: ✅ Running
- **Framework**: FastAPI

### Frontend Application  
- **URL**: http://localhost:5173
- **Status**: ✅ Running
- **Framework**: React + TypeScript + Vite

## 📋 Features

- **Multi-Model Chat**: Support for Llama, Mistral, CodeLlama and more
- **Conversation History**: Persistent storage of all conversations
- **Image Generation**: Integration with Stable Diffusion (when enabled)
- **Code Assistance**: AI-powered code review, optimization, and explanations
- **Real-time WebSocket**: Live streaming responses
- **Modern UI**: Clean, responsive interface with dark/light modes

## 🔧 API Endpoints

### Test the API:
```bash
# Get available models
curl http://localhost:8090/api/models

# Send a chat message
curl -X POST http://localhost:8090/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "model": "llama3.2"}'

# Get conversations
curl http://localhost:8090/api/conversations

# Health check
curl http://localhost:8090/health
```

## 🎨 Access the UI

Open your browser and navigate to:
- **http://localhost:5173**

## 🐳 Docker Deployment

For production deployment with all features:
```bash
# Build and start all services
docker-compose up -d

# Install Ollama models
make install

# Check status
make status
```

## 📦 Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy, Ollama
- **Frontend**: React, TypeScript, Vite, Axios
- **Database**: PostgreSQL (Docker), SQLite (local)
- **Cache**: Redis
- **AI Models**: Ollama (local), OpenAI API (optional)
- **Container**: Docker & Docker Compose

## 🌟 Quick Demo

The application is currently running in demo mode. The backend provides mock responses to demonstrate the API functionality. In production, it connects to actual LLM services like Ollama or OpenAI.

---
Built with ❤️ for the open-source community