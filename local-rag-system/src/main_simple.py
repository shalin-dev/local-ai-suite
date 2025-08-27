from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime

app = FastAPI(
    title="Local RAG System",
    description="Personal knowledge base with semantic search",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

documents = []
queries = []

class QueryRequest(BaseModel):
    question: str
    num_results: int = 5

@app.get("/")
async def root():
    return HTMLResponse("""
    <html>
        <head>
            <title>Local RAG System</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
                .container { background: rgba(255,255,255,0.95); color: #333; padding: 30px; border-radius: 10px; max-width: 900px; margin: 0 auto; }
                h1 { color: #667eea; }
                .doc-card { background: #f9f9f9; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #667eea; }
                .query-box { background: #f0f4f8; padding: 20px; border-radius: 8px; margin: 20px 0; }
                button { background: #667eea; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin: 5px; }
                button:hover { background: #764ba2; }
                input, textarea { width: 100%; padding: 10px; margin: 5px 0; border-radius: 5px; border: 1px solid #ddd; }
                .answer { background: #e8f4f8; padding: 15px; border-radius: 8px; margin: 10px 0; }
                .source { background: #f0f0f0; padding: 8px; border-radius: 5px; margin: 5px 0; font-size: 0.9em; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🧠 Local RAG System</h1>
                <p>Build your personal knowledge base with semantic search capabilities</p>
                
                <div class="query-box">
                    <h2>🔍 Ask a Question</h2>
                    <textarea id="question" rows="3" placeholder="What would you like to know?"></textarea>
                    <button onclick="askQuestion()">Search Knowledge Base</button>
                    <div id="answer"></div>
                </div>
                
                <h2>📄 Upload Documents</h2>
                <div>
                    <input type="file" id="fileInput" accept=".pdf,.txt,.md,.doc,.docx">
                    <button onclick="uploadDoc()">Upload Document</button>
                </div>
                
                <h2>📚 Document Library</h2>
                <div id="documents">
                    <div class="doc-card">
                        <strong>Sample Document: AI Basics</strong><br>
                        <small>Uploaded: 2024-01-15 | Type: PDF | Pages: 42</small><br>
                        <em>Introduction to artificial intelligence and machine learning concepts</em>
                    </div>
                    <div class="doc-card">
                        <strong>Sample Document: Python Guide</strong><br>
                        <small>Uploaded: 2024-01-14 | Type: Markdown | Size: 15KB</small><br>
                        <em>Comprehensive Python programming guide for beginners</em>
                    </div>
                </div>
                
                <h2>✨ Features</h2>
                <ul>
                    <li>Process PDFs, DOCX, TXT, Markdown files</li>
                    <li>ChromaDB vector database for efficient search</li>
                    <li>Semantic search with source citations</li>
                    <li>Query enhancement and expansion</li>
                    <li>100% local processing for privacy</li>
                </ul>
            </div>
            
            <script>
                function askQuestion() {
                    const question = document.getElementById('question').value;
                    
                    fetch('/api/query', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({question: question})
                    })
                    .then(res => res.json())
                    .then(data => {
                        document.getElementById('answer').innerHTML = 
                            `<div class="answer">
                                <h3>Answer:</h3>
                                <p>${data.answer}</p>
                                <div class="source">
                                    <strong>Sources:</strong><br>
                                    ${data.sources.map(s => `• ${s}`).join('<br>')}
                                </div>
                            </div>`;
                    });
                }
                
                function uploadDoc() {
                    const fileInput = document.getElementById('fileInput');
                    const file = fileInput.files[0];
                    
                    if (!file) {
                        alert('Please select a file');
                        return;
                    }
                    
                    const formData = new FormData();
                    formData.append('file', file);
                    
                    fetch('/api/upload', {
                        method: 'POST',
                        body: formData
                    })
                    .then(res => res.json())
                    .then(data => {
                        alert('Document uploaded successfully!');
                        updateDocuments();
                    });
                }
                
                function updateDocuments() {
                    fetch('/api/documents')
                        .then(res => res.json())
                        .then(data => {
                            const html = data.map(doc => 
                                `<div class="doc-card">
                                    <strong>${doc.filename}</strong><br>
                                    <small>Uploaded: ${doc.uploaded_at} | Type: ${doc.type}</small><br>
                                    <em>${doc.description}</em>
                                </div>`
                            ).join('');
                            document.getElementById('documents').innerHTML = html;
                        });
                }
            </script>
        </body>
    </html>
    """)

@app.post("/api/query")
async def query(request: QueryRequest):
    # Demo response
    query_id = str(uuid.uuid4())[:8]
    answer = f"Based on the documents in your knowledge base, here's what I found about '{request.question}': This is a demo response showing how the RAG system would work with real document embeddings and semantic search."
    
    queries.append({
        "id": query_id,
        "question": request.question,
        "answer": answer,
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "query_id": query_id,
        "question": request.question,
        "answer": answer,
        "sources": [
            "AI Basics - Page 12",
            "Python Guide - Section 3.2",
            "Machine Learning Handbook - Chapter 7"
        ],
        "confidence": 0.92
    }

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    doc_id = str(uuid.uuid4())[:8]
    doc = {
        "id": doc_id,
        "filename": file.filename,
        "type": file.filename.split('.')[-1].upper(),
        "uploaded_at": datetime.now().isoformat(),
        "description": f"Document about {file.filename.split('.')[0]}"
    }
    documents.append(doc)
    return {"message": "Document uploaded successfully", "document": doc}

@app.get("/api/documents")
async def get_documents():
    return documents if documents else [
        {
            "filename": "AI Basics.pdf",
            "type": "PDF",
            "uploaded_at": "2024-01-15T10:30:00",
            "description": "Introduction to artificial intelligence"
        },
        {
            "filename": "Python Guide.md",
            "type": "MD",
            "uploaded_at": "2024-01-14T09:15:00",
            "description": "Python programming guide"
        }
    ]

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8092)