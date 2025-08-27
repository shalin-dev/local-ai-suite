from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Personal AI Assistant Dashboard",
    description="Unified interface for multiple local AI models",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo
conversations = {}

class ChatRequest(BaseModel):
    message: str
    model: str = Field(default="llama3.2")
    session_id: Optional[str] = None
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2048, ge=1, le=32768)
    system_prompt: Optional[str] = None

@app.get("/")
async def root():
    return {
        "message": "Personal AI Assistant Dashboard API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/models")
async def get_available_models():
    return {
        "chat": ["llama3.2", "llama3.1", "mistral", "codellama"],
        "image": ["stable-diffusion-2.1"],
        "code": ["codellama"]
    }

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        if not request.session_id:
            request.session_id = str(uuid.uuid4())
        
        # Store message in memory
        if request.session_id not in conversations:
            conversations[request.session_id] = []
        
        conversations[request.session_id].append({
            "role": "user",
            "content": request.message,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Demo response (in production, this would call the actual LLM)
        response = f"This is a demo response to: '{request.message}'. In production, this would connect to Ollama or other LLM services."
        
        conversations[request.session_id].append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return {
            "session_id": request.session_id,
            "response": response,
            "model": request.model,
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/conversations")
async def get_conversations(limit: int = 10, offset: int = 0):
    conv_list = []
    for session_id, messages in list(conversations.items())[offset:offset+limit]:
        conv_list.append({
            "session_id": session_id,
            "message_count": len(messages),
            "last_message": messages[-1]["content"] if messages else None,
            "created_at": messages[0]["timestamp"] if messages else None
        })
    return conv_list

@app.get("/api/conversations/{session_id}")
async def get_conversation(session_id: str):
    if session_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {
        "session_id": session_id,
        "messages": conversations[session_id]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "conversation_count": len(conversations)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8090)