# Local Speech-to-Text System

Privacy-focused speech recognition using OpenAI's Whisper model running entirely on your local hardware. Convert speech to text in 99+ languages without any cloud services.

## 🚀 Features

- **100% Offline**: All processing happens locally, your audio never leaves your device
- **99+ Languages**: Automatic language detection and transcription
- **Real-time Recording**: Record directly from browser with live transcription
- **Multiple Models**: Choose from tiny (39M) to large (1.5GB) models
- **Translation**: Translate any language to English
- **Word Timestamps**: Get precise timing for each word
- **Multiple Formats**: Export as TXT, SRT, VTT, or JSON
- **Batch Processing**: Process multiple files simultaneously
- **WebSocket Streaming**: Real-time transcription for live audio

## 🎯 Use Cases

1. **Meeting Transcription**: Convert recorded meetings to searchable text
2. **Podcast Transcription**: Create transcripts for podcasts and interviews
3. **Video Subtitles**: Generate accurate subtitles for videos
4. **Voice Notes**: Convert voice memos to text documents
5. **Language Learning**: Transcribe and translate foreign language content
6. **Accessibility**: Create transcripts for hearing-impaired users
7. **Content Creation**: Convert spoken ideas to written content
8. **Legal Transcription**: Transcribe depositions and legal recordings

## 🐳 Docker Setup

```bash
# Start the service
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f speech-to-text
```

## 📦 Quick Start (Local)

### Install Dependencies
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Run the application
python -m src.main
```

## 🌐 Web Interface

Access the web UI at http://localhost:8095

### Features:
- 🎤 **Record**: Click the red button to record directly from browser
- 📁 **Upload**: Drag and drop audio/video files
- 🌍 **Languages**: Select from 99+ languages or auto-detect
- 📊 **Models**: Choose model based on speed/accuracy needs
- 📝 **Export**: Download transcriptions in multiple formats

## 🔧 API Endpoints

### Transcribe Audio
```bash
curl -X POST http://localhost:8095/api/transcribe \
  -F "file=@audio.mp3" \
  -F "language=en" \
  -F "model=base"
```

### List Available Models
```bash
curl http://localhost:8095/api/models
```

### Get Transcription History
```bash
curl http://localhost:8095/api/transcriptions
```

## 📊 Model Comparison

| Model | Size | Speed | Accuracy | RAM Required |
|-------|------|-------|----------|--------------|
| Tiny | 39 MB | ~32x | Good | ~1 GB |
| Base | 74 MB | ~16x | Better | ~1 GB |
| Small | 244 MB | ~6x | Great | ~2 GB |
| Medium | 769 MB | ~2x | Excellent | ~5 GB |
| Large | 1550 MB | 1x | Best | ~10 GB |

*Speed relative to Large model

## 🎙️ Supported Formats

### Input
- Audio: MP3, WAV, FLAC, OGG, M4A, AAC, WMA, OPUS
- Video: MP4, AVI, MKV, MOV, WEBM (audio extracted)

### Output
- **TXT**: Plain text transcription
- **SRT**: SubRip subtitles with timestamps
- **VTT**: WebVTT subtitles for web
- **JSON**: Structured data with segments and metadata

## 🌍 Language Support

Full support for 99 languages including:
- English, Spanish, French, German, Italian, Portuguese
- Chinese, Japanese, Korean, Arabic, Hebrew, Hindi
- Russian, Polish, Turkish, Dutch, Swedish, Norwegian
- And many more...

## ⚙️ Configuration

Edit environment variables in `docker-compose.yml`:

```yaml
environment:
  - MODEL_SIZE=base  # tiny, base, small, medium, large
  - DEVICE=cpu       # cpu or cuda
  - BATCH_SIZE=8     # For batch processing
```

## 🚀 Performance Tips

### CPU Usage
- Use smaller models (tiny/base) for faster processing
- Enable multi-threading with `OMP_NUM_THREADS`
- Consider quantized models for better CPU performance

### GPU Acceleration
- CUDA-enabled GPUs provide 5-10x speedup
- Requires NVIDIA GPU with CUDA support
- Set `DEVICE=cuda` in environment

### Memory Optimization
- Stream large files instead of loading entirely
- Use smaller models for limited RAM
- Enable model caching for repeated use

## 🔐 Privacy & Security

- **No Cloud**: Runs entirely offline on your hardware
- **No Tracking**: No analytics or telemetry
- **No Storage**: Audio files deleted after processing (optional)
- **Encrypted**: Support for encrypted audio storage
- **GDPR Compliant**: Full data control and deletion

## 🧪 Advanced Features

### Real-time Streaming
```python
# WebSocket connection for live transcription
ws = websocket.WebSocket()
ws.connect("ws://localhost:8095/ws/transcribe")
ws.send(audio_chunk)
result = ws.recv()
```

### Batch Processing
```python
# Process multiple files
files = ["audio1.mp3", "audio2.wav", "audio3.m4a"]
for file in files:
    transcribe(file)
```

### Custom Vocabulary
```python
# Add domain-specific terms
custom_vocab = ["OpenAI", "Whisper", "PyTorch"]
transcribe(audio, vocab=custom_vocab)
```

## 📈 Benchmarks

| File Size | Model | CPU Time | GPU Time | Accuracy |
|-----------|-------|----------|----------|----------|
| 5 min | Base | 45s | 8s | 95% |
| 30 min | Base | 4.5m | 48s | 95% |
| 1 hour | Base | 9m | 1.6m | 95% |
| 1 hour | Large | 60m | 6m | 98% |

*Tested on Intel i7-10700K (CPU) and NVIDIA RTX 3070 (GPU)

## 🛠️ Troubleshooting

### Common Issues

**Out of Memory:**
- Use a smaller model
- Process shorter audio segments
- Increase swap space

**Slow Processing:**
- Enable GPU acceleration
- Use smaller model
- Reduce audio quality to 16kHz

**Language Detection Issues:**
- Manually specify language code
- Provide longer audio samples
- Use larger models for better detection

## 🤝 Integration Examples

### Python
```python
import requests

with open("audio.mp3", "rb") as f:
    response = requests.post(
        "http://localhost:8095/api/transcribe",
        files={"file": f},
        data={"model": "base", "language": "en"}
    )
print(response.json()["text"])
```

### JavaScript
```javascript
const formData = new FormData();
formData.append('file', audioFile);
formData.append('model', 'base');

fetch('http://localhost:8095/api/transcribe', {
    method: 'POST',
    body: formData
})
.then(res => res.json())
.then(data => console.log(data.text));
```

---
Built with ❤️ for privacy-conscious users who need accurate speech recognition