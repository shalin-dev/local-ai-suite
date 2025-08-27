# Local AI Application Suite

A collection of powerful, privacy-focused AI applications that run entirely on your local machine. Each application is containerized for easy deployment and complete isolation.

## 🚀 Applications

### 1. [Personal AI Assistant Dashboard](./personal-ai-assistant-dashboard)
**Status:** ✅ Running (http://localhost:5173)

Unified interface for multiple local AI models with chat, image generation, and code assistance.

**Key Features:**
- Multi-model chat interface (Llama, Mistral, CodeLlama)
- Image generation with Stable Diffusion
- Code assistance and review
- Conversation history
- WebSocket streaming

**Ports:**
- Frontend: `3000` (Production) / `5173` (Development)
- Backend: `8090`

---

### 2. [AI-Powered Code Documentation Generator](./ai-code-documentation-generator)
**Status:** 🐳 Docker Ready

Automatically generate comprehensive documentation for any codebase using local LLMs.

**Key Features:**
- Multi-language support (Python, JS, TS, Java, C++, Go, Rust)
- Git repository integration
- Multiple output formats (Markdown, HTML, RST)
- Tree-sitter parsing for accuracy
- Batch processing

**Ports:**
- API: `8001`
- Web UI: `3001`

---

### 3. [Local RAG System](./local-rag-system)
**Status:** 🐳 Docker Ready

Build a personal knowledge base from your documents with semantic search capabilities.

**Key Features:**
- Process PDFs, DOCX, TXT, and more
- ChromaDB vector storage
- Semantic search with citations
- Query enhancement
- Collection management

**Ports:**
- Backend: `8002`
- ChromaDB: `8003`
- Web UI: `3002`

---

### 4. [AI Image Classifier for Photos](./ai-image-classifier)
**Status:** 🐳 Docker Ready

Automatically organize and tag your photo library using local vision models.

**Key Features:**
- Auto-tagging with 1000+ categories
- Face recognition and grouping
- Scene detection
- Duplicate finder
- Natural language search
- Smart album generation

**Ports:**
- Backend: `8004`
- Web UI: `3003`
- Database: `5433`

## 🛠 Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Python, FastAPI, Celery |
| Frontend | React, TypeScript, Vite |
| AI Models | Ollama, Transformers, YOLO |
| Databases | PostgreSQL, ChromaDB, Redis |
| Container | Docker, Docker Compose |
| Embedding | Sentence Transformers, CLIP |

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- 16GB+ RAM recommended
- 50GB+ free disk space
- NVIDIA GPU (optional, for faster processing)

### Start All Applications

```bash
# Clone the repository
git clone <your-repo-url>
cd git-projects

# Start all services
./start-all.sh

# Or start individual apps
cd personal-ai-assistant-dashboard && docker-compose up -d
cd ai-code-documentation-generator && docker-compose up -d
cd local-rag-system && docker-compose up -d
cd ai-image-classifier && docker-compose up -d
```

## 📊 Resource Usage

| Application | RAM | CPU | GPU | Storage |
|------------|-----|-----|-----|---------|
| AI Assistant | 2GB | 2 cores | Optional | 5GB |
| Code Doc Gen | 1GB | 2 cores | No | 2GB |
| RAG System | 4GB | 2 cores | Optional | 10GB+ |
| Image Classifier | 4GB | 2 cores | Recommended | 20GB+ |

## 🔐 Privacy & Security

- **100% Local**: All processing happens on your machine
- **No Cloud Dependencies**: Works completely offline
- **Data Ownership**: Your data never leaves your system
- **Containerized**: Each app runs in isolation
- **Open Source**: Fully auditable code

## 📈 Performance Optimization

### CPU-Only Setup
```yaml
# Optimized for CPU
THREADS: 8
BATCH_SIZE: 1
USE_GPU: false
```

### GPU-Accelerated Setup
```yaml
# Optimized for NVIDIA GPU
CUDA_VISIBLE_DEVICES: 0
BATCH_SIZE: 32
USE_GPU: true
```


## 🤝 Contributing

Contributions are welcome! Each application is designed to be modular and extensible.

### Development Setup
```bash
# Install development dependencies
make dev-setup

# Run tests
make test

# Build all containers
make build-all
```

## 📝 License

MIT License - Use freely for personal and commercial projects.

## 🆘 Troubleshooting

### Common Issues

**Port Conflicts:**
```bash
# Check ports in use
netstat -tulpn | grep LISTEN

# Change ports in docker-compose.yml
```

**Memory Issues:**
```bash
# Increase Docker memory
# Docker Desktop > Settings > Resources > Memory: 8GB+
```

**GPU Not Detected:**
```bash
# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
```

## 📚 Documentation

- [API Documentation](./docs/api.md)
- [Deployment Guide](./docs/deployment.md)
- [Security Best Practices](./docs/security.md)
- [Performance Tuning](./docs/performance.md)

## 🌟 Star History

If you find these applications useful, please consider giving the repository a star ⭐

---

**Built with ❤️ for the open-source community**

*Empowering developers with local, private AI solutions*