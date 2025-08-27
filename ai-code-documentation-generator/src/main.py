import asyncio
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
import logging
from datetime import datetime

from .scanner import CodeScanner
from .parser import CodeParser
from .doc_generator import DocumentationGenerator
from .templates import TemplateManager
from .utils import setup_logging, load_config

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI-Powered Code Documentation Generator",
    description="Automatically generate documentation for your codebase using local LLMs",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

config = load_config()
scanner = CodeScanner(config)
parser = CodeParser(config)
doc_generator = DocumentationGenerator(config)
template_manager = TemplateManager(config)

class ScanRequest(BaseModel):
    repo_url: Optional[str] = None
    local_path: Optional[str] = None
    file_patterns: List[str] = Field(default=["*.py", "*.js", "*.ts", "*.java", "*.cpp", "*.go", "*.rs"])
    exclude_patterns: List[str] = Field(default=["node_modules", "__pycache__", ".git", "dist", "build"])
    doc_style: str = Field(default="markdown", description="markdown, html, rst, or json")
    include_examples: bool = True
    include_tests: bool = True
    include_metrics: bool = True
    llm_model: str = Field(default="llama3.2")

class DocumentationJob(BaseModel):
    job_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    progress: float
    message: str
    result_path: Optional[str] = None
    error: Optional[str] = None

jobs_db: Dict[str, DocumentationJob] = {}

@app.get("/")
async def root():
    return {
        "message": "AI Code Documentation Generator API",
        "version": "1.0.0",
        "endpoints": {
            "scan": "/api/scan",
            "generate": "/api/generate",
            "status": "/api/status/{job_id}",
            "download": "/api/download/{job_id}",
            "templates": "/api/templates"
        }
    }

@app.post("/api/scan")
async def scan_codebase(request: ScanRequest, background_tasks: BackgroundTasks):
    job_id = str(datetime.now().timestamp())
    
    job = DocumentationJob(
        job_id=job_id,
        status="scanning",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        progress=0.0,
        message="Starting codebase scan..."
    )
    
    jobs_db[job_id] = job
    
    background_tasks.add_task(
        process_documentation,
        job_id=job_id,
        request=request
    )
    
    return {"job_id": job_id, "status": "started"}

async def process_documentation(job_id: str, request: ScanRequest):
    job = jobs_db[job_id]
    
    try:
        job.status = "scanning"
        job.progress = 10.0
        job.message = "Scanning codebase..."
        job.updated_at = datetime.now()
        
        if request.repo_url:
            code_path = await scanner.clone_repository(request.repo_url)
        else:
            code_path = Path(request.local_path or ".")
        
        files = await scanner.scan_directory(
            code_path,
            file_patterns=request.file_patterns,
            exclude_patterns=request.exclude_patterns
        )
        
        job.progress = 30.0
        job.message = f"Found {len(files)} files to document"
        job.status = "parsing"
        job.updated_at = datetime.now()
        
        parsed_data = []
        for i, file_path in enumerate(files):
            parsed = await parser.parse_file(file_path)
            if parsed:
                parsed_data.append(parsed)
            
            job.progress = 30 + (40 * (i + 1) / len(files))
            job.updated_at = datetime.now()
        
        job.status = "generating"
        job.progress = 70.0
        job.message = "Generating documentation..."
        job.updated_at = datetime.now()
        
        documentation = await doc_generator.generate_documentation(
            parsed_data,
            style=request.doc_style,
            model=request.llm_model,
            include_examples=request.include_examples,
            include_tests=request.include_tests,
            include_metrics=request.include_metrics
        )
        
        job.progress = 90.0
        job.message = "Saving documentation..."
        job.updated_at = datetime.now()
        
        output_path = Path(f"output/{job_id}")
        output_path.mkdir(parents=True, exist_ok=True)
        
        if request.doc_style == "markdown":
            doc_file = output_path / "documentation.md"
            doc_file.write_text(documentation)
        elif request.doc_style == "html":
            doc_file = output_path / "documentation.html"
            html = await template_manager.render_html(documentation)
            doc_file.write_text(html)
        else:
            doc_file = output_path / f"documentation.{request.doc_style}"
            doc_file.write_text(documentation)
        
        job.status = "completed"
        job.progress = 100.0
        job.message = "Documentation generated successfully"
        job.result_path = str(doc_file)
        job.updated_at = datetime.now()
        
    except Exception as e:
        logger.error(f"Error processing job {job_id}: {str(e)}")
        job.status = "failed"
        job.error = str(e)
        job.message = "Documentation generation failed"
        job.updated_at = datetime.now()

@app.get("/api/status/{job_id}")
async def get_job_status(job_id: str):
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return jobs_db[job_id]

@app.get("/api/download/{job_id}")
async def download_documentation(job_id: str):
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs_db[job_id]
    
    if job.status != "completed":
        raise HTTPException(status_code=400, detail="Documentation not ready")
    
    if not job.result_path or not Path(job.result_path).exists():
        raise HTTPException(status_code=404, detail="Documentation file not found")
    
    return FileResponse(
        path=job.result_path,
        filename=Path(job.result_path).name,
        media_type="application/octet-stream"
    )

@app.post("/api/upload")
async def upload_codebase(file: UploadFile = File(...)):
    try:
        upload_path = Path(f"repos/upload_{datetime.now().timestamp()}")
        upload_path.mkdir(parents=True, exist_ok=True)
        
        file_path = upload_path / file.filename
        
        content = await file.read()
        file_path.write_bytes(content)
        
        if file.filename.endswith(('.zip', '.tar', '.tar.gz')):
            import zipfile
            import tarfile
            
            if file.filename.endswith('.zip'):
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(upload_path)
            else:
                with tarfile.open(file_path, 'r:*') as tar_ref:
                    tar_ref.extractall(upload_path)
        
        return {
            "message": "File uploaded successfully",
            "path": str(upload_path)
        }
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/templates")
async def get_templates():
    return await template_manager.list_templates()

@app.post("/api/templates/{template_name}")
async def apply_template(template_name: str, job_id: str):
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs_db[job_id]
    
    if job.status != "completed":
        raise HTTPException(status_code=400, detail="Documentation not ready")
    
    try:
        result = await template_manager.apply_template(
            template_name,
            job.result_path
        )
        return {"message": "Template applied successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/languages")
async def get_supported_languages():
    return {
        "languages": [
            {"name": "Python", "extensions": [".py"], "parser": "tree-sitter"},
            {"name": "JavaScript", "extensions": [".js", ".jsx"], "parser": "tree-sitter"},
            {"name": "TypeScript", "extensions": [".ts", ".tsx"], "parser": "tree-sitter"},
            {"name": "Java", "extensions": [".java"], "parser": "tree-sitter"},
            {"name": "C++", "extensions": [".cpp", ".cc", ".h", ".hpp"], "parser": "tree-sitter"},
            {"name": "Go", "extensions": [".go"], "parser": "tree-sitter"},
            {"name": "Rust", "extensions": [".rs"], "parser": "tree-sitter"},
            {"name": "C#", "extensions": [".cs"], "parser": "regex"},
            {"name": "PHP", "extensions": [".php"], "parser": "regex"},
            {"name": "Ruby", "extensions": [".rb"], "parser": "regex"}
        ]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "jobs_count": len(jobs_db),
        "active_jobs": sum(1 for j in jobs_db.values() if j.status in ["scanning", "parsing", "generating"])
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )