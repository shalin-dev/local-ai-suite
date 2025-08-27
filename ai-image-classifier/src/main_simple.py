from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime
import random

app = FastAPI(
    title="AI Image Classifier",
    description="Auto-tag and organize your photo library",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

photos = []

class SearchRequest(BaseModel):
    query: str
    limit: int = 10

@app.get("/")
async def root():
    return HTMLResponse("""
    <html>
        <head>
            <title>AI Image Classifier</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
                .container { background: rgba(255,255,255,0.95); color: #333; padding: 30px; border-radius: 10px; max-width: 1000px; margin: 0 auto; }
                h1 { color: #667eea; }
                .photo-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
                .photo-card { background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); transition: transform 0.3s; }
                .photo-card:hover { transform: scale(1.05); }
                .photo-img { width: 100%; height: 150px; background: linear-gradient(45deg, #ddd 25%, transparent 25%, transparent 75%, #ddd 75%, #ddd), linear-gradient(45deg, #ddd 25%, transparent 25%, transparent 75%, #ddd 75%, #ddd); background-size: 20px 20px; background-position: 0 0, 10px 10px; }
                .photo-info { padding: 10px; }
                .tags { display: flex; flex-wrap: wrap; gap: 5px; margin: 5px 0; }
                .tag { background: #667eea; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.8em; }
                button { background: #667eea; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin: 5px; }
                button:hover { background: #764ba2; }
                input { width: 100%; padding: 10px; margin: 5px 0; border-radius: 5px; border: 1px solid #ddd; }
                .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
                .stat-card { background: #f9f9f9; padding: 15px; border-radius: 8px; text-align: center; }
                .stat-number { font-size: 2em; color: #667eea; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📸 AI Image Classifier</h1>
                <p>Automatically organize and tag your photo library with AI</p>
                
                <h2>📊 Library Statistics</h2>
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-number">2,847</div>
                        <div>Total Photos</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">156</div>
                        <div>People Detected</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">423</div>
                        <div>Unique Tags</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">18</div>
                        <div>Smart Albums</div>
                    </div>
                </div>
                
                <h2>🔍 Search Photos</h2>
                <div>
                    <input type="text" id="searchQuery" placeholder="Search by description (e.g., 'sunset at beach', 'dog in park')">
                    <button onclick="searchPhotos()">Search</button>
                    <button onclick="uploadPhoto()">Upload Photo</button>
                </div>
                
                <h2>🖼️ Recent Photos</h2>
                <div class="photo-grid" id="photoGrid">
                    <div class="photo-card">
                        <div class="photo-img"></div>
                        <div class="photo-info">
                            <strong>Beach Sunset</strong>
                            <div class="tags">
                                <span class="tag">sunset</span>
                                <span class="tag">beach</span>
                                <span class="tag">ocean</span>
                                <span class="tag">landscape</span>
                            </div>
                            <small>2024-01-20 18:45</small>
                        </div>
                    </div>
                    <div class="photo-card">
                        <div class="photo-img"></div>
                        <div class="photo-info">
                            <strong>Family Picnic</strong>
                            <div class="tags">
                                <span class="tag">people</span>
                                <span class="tag">park</span>
                                <span class="tag">family</span>
                                <span class="tag">outdoor</span>
                            </div>
                            <small>2024-01-19 14:30</small>
                        </div>
                    </div>
                    <div class="photo-card">
                        <div class="photo-img"></div>
                        <div class="photo-info">
                            <strong>Mountain Hike</strong>
                            <div class="tags">
                                <span class="tag">mountain</span>
                                <span class="tag">nature</span>
                                <span class="tag">hiking</span>
                                <span class="tag">landscape</span>
                            </div>
                            <small>2024-01-18 10:15</small>
                        </div>
                    </div>
                    <div class="photo-card">
                        <div class="photo-img"></div>
                        <div class="photo-info">
                            <strong>City Night</strong>
                            <div class="tags">
                                <span class="tag">city</span>
                                <span class="tag">night</span>
                                <span class="tag">lights</span>
                                <span class="tag">urban</span>
                            </div>
                            <small>2024-01-17 21:00</small>
                        </div>
                    </div>
                </div>
                
                <h2>✨ Features</h2>
                <ul>
                    <li>Auto-tagging with 1000+ object categories</li>
                    <li>Face recognition and grouping</li>
                    <li>Scene detection (indoor/outdoor, landscapes, cities)</li>
                    <li>Duplicate photo detection</li>
                    <li>Natural language search</li>
                    <li>Smart album generation</li>
                    <li>EXIF data extraction</li>
                </ul>
                
                <h2>📁 Smart Albums</h2>
                <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                    <button>👨‍👩‍👧‍👦 Family (342)</button>
                    <button>🏖️ Vacations (189)</button>
                    <button>🐕 Pets (127)</button>
                    <button>🌅 Sunsets (84)</button>
                    <button>🎂 Birthdays (56)</button>
                    <button>🏔️ Nature (423)</button>
                </div>
            </div>
            
            <script>
                function searchPhotos() {
                    const query = document.getElementById('searchQuery').value;
                    
                    fetch('/api/search', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({query: query})
                    })
                    .then(res => res.json())
                    .then(data => {
                        alert(`Found ${data.results.length} photos matching "${query}"`);
                        updatePhotoGrid(data.results);
                    });
                }
                
                function uploadPhoto() {
                    const input = document.createElement('input');
                    input.type = 'file';
                    input.accept = 'image/*';
                    input.onchange = e => {
                        const file = e.target.files[0];
                        const formData = new FormData();
                        formData.append('file', file);
                        
                        fetch('/api/upload', {
                            method: 'POST',
                            body: formData
                        })
                        .then(res => res.json())
                        .then(data => {
                            alert('Photo uploaded and analyzed successfully!');
                        });
                    };
                    input.click();
                }
                
                function updatePhotoGrid(photos) {
                    const grid = document.getElementById('photoGrid');
                    const html = photos.map(photo => 
                        `<div class="photo-card">
                            <div class="photo-img"></div>
                            <div class="photo-info">
                                <strong>${photo.name}</strong>
                                <div class="tags">
                                    ${photo.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                                </div>
                                <small>${photo.date}</small>
                            </div>
                        </div>`
                    ).join('');
                    grid.innerHTML = html;
                }
            </script>
        </body>
    </html>
    """)

@app.post("/api/search")
async def search_photos(request: SearchRequest):
    # Demo search results
    results = [
        {
            "id": str(uuid.uuid4())[:8],
            "name": f"Photo matching '{request.query}'",
            "tags": ["sunset", "beach", "ocean"],
            "date": "2024-01-20 18:45",
            "confidence": 0.95
        },
        {
            "id": str(uuid.uuid4())[:8],
            "name": f"Similar to '{request.query}'",
            "tags": ["landscape", "nature", "outdoor"],
            "date": "2024-01-19 16:30",
            "confidence": 0.87
        }
    ]
    
    return {
        "query": request.query,
        "results": results,
        "total": len(results)
    }

@app.post("/api/upload")
async def upload_photo(file: UploadFile = File(...)):
    photo_id = str(uuid.uuid4())[:8]
    
    # Simulate AI analysis
    tags = random.sample(
        ["sunset", "beach", "mountain", "city", "people", "dog", "cat", "food", "car", "building", "tree", "sky"],
        k=random.randint(3, 6)
    )
    
    photo = {
        "id": photo_id,
        "filename": file.filename,
        "tags": tags,
        "objects_detected": random.randint(5, 15),
        "faces_detected": random.randint(0, 5),
        "scene": random.choice(["outdoor", "indoor", "landscape", "urban"]),
        "uploaded_at": datetime.now().isoformat()
    }
    
    photos.append(photo)
    
    return {
        "message": "Photo uploaded and analyzed successfully",
        "photo": photo
    }

@app.get("/api/photos")
async def get_photos(limit: int = 20):
    return photos[-limit:] if photos else []

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8093)