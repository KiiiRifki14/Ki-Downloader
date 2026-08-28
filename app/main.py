from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from pathlib import Path
from app.downloader import get_video_info, download_media, TEMP_DIR
from app.cleaner import cleanup_old_files

app = FastAPI(title="Ki.Downloader API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

class AnalyzeRequest(BaseModel):
    url: str

class DownloadRequest(BaseModel):
    url: str

@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "Ki.Downloader"}

@app.post("/api/analyze")
def analyze_url(req: AnalyzeRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(cleanup_old_files)
    if not req.url or not req.url.startswith("http"):
        raise HTTPException(status_code=400, detail="URL tidak valid! Harap masukkan URL lengkap.")
    
    info = get_video_info(req.url)
    if not info:
        raise HTTPException(status_code=400, detail="Gagal menganalisis link. Pastikan link dapat diakses.")
    return {"status": "success", "info": info}

@app.post("/api/download")
def download_url(req: DownloadRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(cleanup_old_files)
    if not req.url or not req.url.startswith("http"):
        raise HTTPException(status_code=400, detail="URL tidak valid! Harap masukkan link lengkap yang diawali http:// atau https://")
    
    try:
        session_id, files = download_media(req.url)
        if not files:
            raise HTTPException(status_code=400, detail="⚠️ Kebijakan Instagram: Pembacaan link akun profil secara otomatis diblokir oleh Instagram tanpa login. Solusi: Harap buka foto/video Reels dari akun publik ini, lalu tempelkan LINK POSTINGAN / REELS-nya langsung ke sini!")
        return {"status": "success", "session_id": session_id, "files": files}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal memproses media: {str(e)}")

@app.get("/api/file/{session_id}/{filename}")
def serve_file(session_id: str, filename: str):
    file_path = TEMP_DIR / session_id / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File tidak ditemukan atau telah kadaluarsa.")
    return FileResponse(path=file_path, filename=filename)

@app.get("/", response_class=HTMLResponse)
def index_page():
    index_file = Path("static/index.html")
    if index_file.exists():
        return HTMLResponse(content=index_file.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Ki.Downloader API Running</h1>")

@app.get("/embed", response_class=HTMLResponse)
def embed_page():
    embed_file = Path("static/embed.html")
    if embed_file.exists():
        return HTMLResponse(content=embed_file.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Ki.Downloader Embed Page</h1>")

@app.get("/google285291aa47519dbc.html")
def google_verification():
    verify_file = Path("static/google285291aa47519dbc.html")
    if verify_file.exists():
        return FileResponse(path=verify_file)
    return HTMLResponse(content="google-site-verification: google285291aa47519dbc.html")

@app.get("/sitemap.xml")
def sitemap_xml():
    sitemap_file = Path("static/sitemap.xml")
    if sitemap_file.exists():
        return FileResponse(path=sitemap_file, media_type="application/xml")
    return HTMLResponse(content="<xml></xml>", media_type="application/xml")
