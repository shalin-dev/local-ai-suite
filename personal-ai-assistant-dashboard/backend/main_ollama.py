from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime
import logging
import httpx
import json

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

# Ollama configuration
OLLAMA_HOST = "http://localhost:11434"

class ChatRequest(BaseModel):
    message: str
    model: str = Field(default="llama3.2:1b")
    session_id: Optional[str] = None
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2048, ge=1, le=32768)
    system_prompt: Optional[str] = None

@app.get("/")
async def root():
    return {
        "message": "Personal AI Assistant Dashboard API",
        "version": "1.0.0",
        "status": "running",
        "ollama": "connected"
    }

@app.get("/api/models")
async def get_available_models():
    try:
        # Get models from Ollama
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{OLLAMA_HOST}/api/tags")
            if response.status_code == 200:
                ollama_models = response.json()
                model_names = [model["name"] for model in ollama_models.get("models", [])]
                return {
                    "chat": model_names,
                    "available": model_names,
                    "default": "llama3.2:1b"
                }
    except Exception as e:
        logger.error(f"Failed to get models from Ollama: {e}")
    
    # Return your known models as fallback
    return {
        "chat": ["llama3.2:1b", "deepseek-coder:6.7b-instruct-q4_0"],
        "available": ["llama3.2:1b", "deepseek-coder:6.7b-instruct-q4_0"],
        "default": "llama3.2:1b"
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
        
        # Call Ollama API
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                ollama_payload = {
                    "model": request.model,
                    "prompt": request.message,
                    "temperature": request.temperature,
                    "options": {
                        "num_predict": request.max_tokens
                    },
                    "stream": False
                }
                
                if request.system_prompt:
                    ollama_payload["system"] = request.system_prompt
                
                logger.info(f"Sending request to Ollama: {ollama_payload['model']}")
                response = await client.post(
                    f"{OLLAMA_HOST}/api/generate",
                    json=ollama_payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    ai_response = result.get("response", "No response from model")
                else:
                    logger.error(f"Ollama returned status {response.status_code}")
                    ai_response = f"Error: Ollama returned status {response.status_code}"
                    
        except httpx.ConnectError:
            logger.warning("Could not connect to Ollama, using demo response")
            ai_response = f"Demo response (Ollama not connected): I understand you said '{request.message}'. In production, this would be a real AI response from {request.model}."
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            ai_response = f"Error connecting to Ollama: {str(e)}"
        
        conversations[request.session_id].append({
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return {
            "session_id": request.session_id,
            "response": ai_response,
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
    # Check Ollama connection
    ollama_status = "disconnected"
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(f"{OLLAMA_HOST}/api/tags")
            if response.status_code == 200:
                ollama_status = "connected"
    except:
        pass
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "conversation_count": len(conversations),
        "ollama": ollama_status
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8094)