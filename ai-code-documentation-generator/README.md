# AI-Powered Code Documentation Generator

Automatically generate comprehensive documentation for your codebase using local LLMs. Scans repositories, analyzes code structure, and creates beautiful documentation in multiple formats.

## 🚀 Features

- **Multi-Language Support**: Python, JavaScript, TypeScript, Java, C++, Go, Rust, and more
- **Git Integration**: Clone and analyze any public repository
- **Smart Parsing**: Uses tree-sitter for accurate code parsing
- **Multiple Output Formats**: Markdown, HTML, RST, JSON
- **Batch Processing**: Document entire codebases efficiently
- **Customizable Templates**: Use your own documentation templates
- **Metrics & Analysis**: Code complexity, test coverage insights
- **Local LLM Integration**: Works with Ollama for privacy

## 🐳 Docker Setup

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f doc-generator
```

## 📦 Installation (Local)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the service
python -m src.main
```

## 🔧 API Endpoints

### Generate Documentation
```bash
curl -X POST http://localhost:8001/api/scan \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/user/repo.git",
    "doc_style": "markdown",
    "llm_model": "llama3.2"
  }'
```

### Check Job Status
```bash
curl http://localhost:8001/api/status/{job_id}
```

### Download Documentation
```bash
curl -O http://localhost:8001/api/download/{job_id}
```

## 🎯 Use Cases

1. **Open Source Projects**: Generate docs for any GitHub repository
2. **Legacy Code**: Document undocumented legacy codebases
3. **API Documentation**: Auto-generate API docs from code
4. **Code Reviews**: Create comprehensive code analysis reports
5. **Team Onboarding**: Help new developers understand codebases

## 🛠 Configuration

Edit `config.yaml` to customize:

```yaml
scanner:
  exclude_patterns: ["test*", "*.test.js"]
  max_file_size: 1048576  # 1MB

parser:
  languages: ["python", "javascript", "typescript"]
  
generator:
  default_model: "llama3.2"
  include_examples: true
  include_metrics: true
```

## 📊 Architecture

```
┌─────────────┐     ┌──────────┐     ┌───────────┐
│   Scanner   │────▶│  Parser  │────▶│ Generator │
└─────────────┘     └──────────┘     └───────────┘
       │                  │                  │
       ▼                  ▼                  ▼
   [Git Repos]      [Tree-sitter]      [Ollama LLM]
```

## 🔍 Supported Languages

- **Full Support**: Python, JavaScript, TypeScript, Java, C++, Go, Rust
- **Basic Support**: C#, PHP, Ruby, Swift, Kotlin, Scala, R
- **Config Files**: YAML, JSON, TOML, XML

## 🌐 Web UI

Access the web interface at http://localhost:3001 for:
- Visual repository browser
- Real-time documentation generation
- Export in multiple formats
- Documentation preview

## 📈 Performance

- Processes ~1000 files/minute
- Supports repositories up to 100MB
- Concurrent file processing
- Caching for repeated analyses

## 🔐 Privacy

- Runs completely offline
- No data leaves your machine
- Works with local LLMs only
- Secure containerized environment

---
Built with ❤️ for developers who hate writing documentation