from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime

app = FastAPI(
    title="AI Code Documentation Generator",
    description="Generate documentation for your codebase",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

jobs = {}

class ScanRequest(BaseModel):
    repo_url: Optional[str] = None
    local_path: Optional[str] = None
    doc_style: str = "markdown"

@app.get("/")
async def root():
    return HTMLResponse("""
    <html>
        <head>
            <title>Code Documentation Generator</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
                .container { background: rgba(255,255,255,0.95); color: #333; padding: 30px; border-radius: 10px; max-width: 800px; margin: 0 auto; }
                h1 { color: #667eea; }
                .status { background: #f0f0f0; padding: 10px; border-radius: 5px; margin: 10px 0; }
                button { background: #667eea; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
                button:hover { background: #764ba2; }
                input, select { width: 100%; padding: 8px; margin: 5px 0; border-radius: 5px; border: 1px solid #ddd; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 AI Code Documentation Generator</h1>
                <p>Generate comprehensive documentation for any codebase using AI</p>
                
                <h2>📝 Generate Documentation</h2>
                <div>
                    <input type="text" id="repo" placeholder="Enter GitHub repository URL or local path">
                    <select id="style">
                        <option value="markdown">Markdown</option>
                        <option value="html">HTML</option>
                        <option value="rst">ReStructuredText</option>
                    </select>
                    <button onclick="generateDocs()">Generate Documentation</button>
                </div>
                
                <div id="status" class="status" style="display: none;">
                    <h3>Job Status</h3>
                    <div id="statusContent"></div>
                </div>
                
                <h2>✨ Features</h2>
                <ul>
                    <li>Multi-language support (Python, JS, TS, Java, C++, Go, Rust)</li>
                    <li>Git repository integration</li>
                    <li>Multiple output formats</li>
                    <li>Smart code parsing with tree-sitter</li>
                    <li>Batch processing for large codebases</li>
                </ul>
                
                <h2>📊 Recent Jobs</h2>
                <div id="jobs"></div>
            </div>
            
            <script>
                function generateDocs() {
                    const repo = document.getElementById('repo').value;
                    const style = document.getElementById('style').value;
                    
                    fetch('/api/scan', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({repo_url: repo, doc_style: style})
                    })
                    .then(res => res.json())
                    .then(data => {
                        document.getElementById('status').style.display = 'block';
                        document.getElementById('statusContent').innerHTML = 
                            `Job ID: ${data.job_id}<br>Status: ${data.status}`;
                        updateJobs();
                    });
                }
                
                function updateJobs() {
                    fetch('/api/jobs')
                        .then(res => res.json())
                        .then(data => {
                            const html = data.map(job => 
                                `<div class="status">
                                    <strong>${job.job_id}</strong><br>
                                    Status: ${job.status}<br>
                                    Created: ${job.created_at}
                                </div>`
                            ).join('');
                            document.getElementById('jobs').innerHTML = html;
                        });
                }
                
                updateJobs();
                setInterval(updateJobs, 5000);
            </script>
        </body>
    </html>
    """)

@app.post("/api/scan")
async def scan_codebase(request: ScanRequest):
    job_id = str(uuid.uuid4())[:8]
    job = {
        "job_id": job_id,
        "status": "scanning",
        "created_at": datetime.now().isoformat(),
        "request": request.dict()
    }
    jobs[job_id] = job
    
    # Simulate processing
    job["status"] = "completed"
    job["result"] = f"Documentation generated for {request.repo_url or request.local_path}"
    
    return {"job_id": job_id, "status": "started"}

@app.get("/api/jobs")
async def get_jobs():
    return list(jobs.values())

@app.get("/api/status/{job_id}")
async def get_job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8091)