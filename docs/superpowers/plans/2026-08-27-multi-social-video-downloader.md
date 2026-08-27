# Multi-Social Video Downloader Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a high-performance, multi-platform video downloader web app (TikTok, Instagram, YouTube, Facebook, Twitter/X, Threads, Pinterest) with FastAPI backend, clean light emerald & white responsive frontend, modular ad monetization slots, and cross-site embeddable iframe widget support.

**Architecture:** Asynchronous FastAPI backend providing REST endpoints (`/api/analyze`, `/api/download`, `/api/file/{uuid}/{filename}`) and static file serving (`/` and `/embed`). Core media engine uses `yt-dlp` and `instaloader` with background file cleanup. Frontend built with pure HTML5, CSS3 (Clean Emerald & White theme system), and ES6 JS.

**Tech Stack:** Python 3.10+, FastAPI, Uvicorn, yt-dlp, instaloader, pytest, HTML5, CSS3, Vanilla JavaScript, Google Fonts (Plus Jakarta Sans).

---

### Task 1: Environment & Project Structure Setup

**Files:**
- Create: `requirements.txt`
- Create: `app/__init__.py`
- Create: `app/main.py`
- Create: `static/css/style.css`
- Create: `static/js/ads-config.js`

- [ ] **Step 1: Update `requirements.txt` with FastAPI and Uvicorn dependencies**

```text
fastapi>=0.100.0
uvicorn>=0.22.0
yt-dlp>=2025.01.01
instaloader>=4.10
requests>=2.31.0
pytest>=7.0.0
httpx>=0.24.0
```

- [ ] **Step 2: Create basic FastAPI app in `app/main.py`**

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

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

@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "Ki.Downloader"}
```

- [ ] **Step 3: Create initial test file `tests/test_health.py`**

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

- [ ] **Step 4: Run pytest to verify health check passes**

Run: `python -m pytest tests/test_health.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add requirements.txt app/ main.py tests/
git commit -m "feat: initialize FastAPI application and health check endpoint"
```

---

### Task 2: Core Media Downloader Backend Engine (`app/downloader.py` & `app/cleaner.py`)

**Files:**
- Create: `app/downloader.py`
- Create: `app/cleaner.py`
- Test: `tests/test_downloader.py`

- [ ] **Step 1: Write test for downloader helper functions in `tests/test_downloader.py`**

```python
from app.downloader import detect_platform, get_video_info

def test_detect_platform():
    assert detect_platform("https://www.tiktok.com/@user/video/123456789") == "tiktok"
    assert detect_platform("https://www.instagram.com/reel/C123456789/") == "instagram"
    assert detect_platform("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "youtube"
    assert detect_platform("https://x.com/user/status/123456789") == "twitter"
    assert detect_platform("https://unknown-domain.com") == "generic"
```

- [ ] **Step 2: Run test to verify it fails before implementation**

Run: `python -m pytest tests/test_downloader.py -v`
Expected: FAIL with "ImportError: cannot import name 'detect_platform'"

- [ ] **Step 3: Implement `app/downloader.py` and `app/cleaner.py`**

Create `app/downloader.py`:
```python
import os
import uuid
import yt_dlp
import instaloader
from pathlib import Path

TEMP_DIR = Path("temp_downloads")
TEMP_DIR.mkdir(exist_ok=True)

def detect_platform(url: str) -> str:
    url_lower = url.lower()
    if "tiktok.com" in url_lower:
        return "tiktok"
    elif "instagram.com" in url_lower:
        return "instagram"
    elif "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "youtube"
    elif "twitter.com" in url_lower or "x.com" in url_lower:
        return "twitter"
    elif "facebook.com" in url_lower or "fb.watch" in url_lower:
        return "facebook"
    elif "threads.net" in url_lower:
        return "threads"
    elif "pinterest.com" in url_lower or "pin.it" in url_lower:
        return "pinterest"
    return "generic"

def get_video_info(url: str):
    platform = detect_platform(url)
    try:
        if platform == "instagram":
            return {
                "title": "Instagram Media Post",
                "thumbnail": None,
                "platform": "instagram",
                "slides_support": True
            }
        
        ydl_opts = {"quiet": True, "skip_download": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title", "Social Media Video"),
                "thumbnail": info.get("thumbnail"),
                "duration": info.get("duration"),
                "platform": platform,
                "uploader": info.get("uploader", "")
            }
    except Exception as e:
        return None

def download_media(url: str):
    session_id = str(uuid.uuid4())
    target_dir = TEMP_DIR / session_id
    target_dir.mkdir(parents=True, exist_ok=True)
    found_files = []

    platform = detect_platform(url)
    try:
        if platform == "instagram":
            L = instaloader.Instaloader(
                save_metadata=False,
                download_videos=True,
                download_video_thumbnails=False,
                download_geotags=False,
                download_comments=False,
                compress_json=False
            )
            shortcode = None
            if "/p/" in url:
                shortcode = url.split("/p/")[1].split("/")[0]
            elif "/reel/" in url:
                shortcode = url.split("/reel/")[1].split("/")[0]
            
            if shortcode:
                post = instaloader.Post.from_shortcode(L.context, shortcode)
                L.download_post(post, target=target_dir)
        else:
            outtmpl = str(target_dir / "%(title)s.%(ext)s")
            ydl_opts = {
                "outtmpl": outtmpl,
                "quiet": True,
                "noplaylist": True,
                "format": "bestvideo+bestaudio/best",
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        for f in os.listdir(target_dir):
            if f.endswith(('.jpg', '.jpeg', '.png', '.mp4', '.webm', '.m4a', '.mp3')):
                found_files.append({
                    "filename": f,
                    "filepath": str(target_dir / f),
                    "relative_url": f"/api/file/{session_id}/{f}",
                    "is_video": f.endswith(('.mp4', '.webm')),
                    "is_image": f.endswith(('.jpg', '.jpeg', '.png'))
                })
        found_files.sort(key=lambda x: x["filename"])
        return session_id, found_files
    except Exception as e:
        return session_id, []
```

Create `app/cleaner.py`:
```python
import os
import time
import shutil
from pathlib import Path

TEMP_DIR = Path("temp_downloads")

def cleanup_old_files(max_age_seconds: int = 900):
    if not TEMP_DIR.exists():
        return
    now = time.time()
    for folder in TEMP_DIR.iterdir():
        if folder.is_dir():
            folder_age = now - folder.stat().st_mtime
            if folder_age > max_age_seconds:
                try:
                    shutil.rmtree(folder)
                except Exception:
                    pass
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_downloader.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add app/downloader.py app/cleaner.py tests/test_downloader.py
git commit -m "feat: implement media downloader engine and auto cleanup task"
```

---

### Task 3: REST API Endpoints (`app/main.py`)

**Files:**
- Modify: `app/main.py`
- Test: `tests/test_api.py`

- [ ] **Step 1: Write test for API endpoints in `tests/test_api.py`**

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_analyze_endpoint_missing_url():
    response = client.post("/api/analyze", json={})
    assert response.status_code == 422

def test_analyze_invalid_url():
    response = client.post("/api/analyze", json={"url": "invalid-url"})
    assert response.status_code == 400
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_api.py -v`
Expected: FAIL with 404 Not Found

- [ ] **Step 3: Implement REST Endpoints in `app/main.py`**

Update `app/main.py`:
```python
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
        raise HTTPException(status_code=400, detail="URL tidak valid!")
    
    session_id, files = download_media(req.url)
    if not files:
        raise HTTPException(status_code=500, detail="Gagal mendownload media dari tautan ini.")
    return {"status": "success", "session_id": session_id, "files": files}

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
```

- [ ] **Step 4: Run pytest to verify API endpoints pass**

Run: `python -m pytest tests/test_api.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add app/main.py tests/test_api.py
git commit -m "feat: implement analyze, download, serve_file, and embed API endpoints"
```

---

### Task 4: Clean Light Emerald Frontend UI (`static/index.html` & `static/css/style.css`)

**Files:**
- Create: `static/index.html`
- Create: `static/css/style.css`

- [ ] **Step 1: Create `static/css/style.css` with Light Emerald & Crisp White Design Tokens**

```css
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
  --bg-main: #f8fafc;
  --bg-card: #ffffff;
  --text-main: #0f172a;
  --text-muted: #64748b;
  --primary-emerald: #059669;
  --primary-hover: #047857;
  --primary-light: #ecfdf5;
  --border-color: #e2e8f0;
  --shadow-sm: 0 2px 10px rgba(0, 0, 0, 0.03);
  --shadow-md: 0 8px 30px rgba(0, 0, 0, 0.06);
  --radius-lg: 16px;
  --radius-full: 9999px;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Plus Jakarta Sans', sans-serif;
  background-color: var(--bg-main);
  color: var(--text-main);
  line-height: 1.5;
  padding-bottom: 80px;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

/* Header Navbar */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  margin-bottom: 24px;
}

.logo {
  font-size: 22px;
  font-weight: 800;
  color: var(--text-main);
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo span {
  color: var(--primary-emerald);
}

.btn-embed-trigger {
  background-color: var(--primary-light);
  color: var(--primary-emerald);
  border: 1px solid var(--border-color);
  padding: 8px 16px;
  border-radius: var(--radius-full);
  font-weight: 600;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-embed-trigger:hover {
  background-color: var(--primary-emerald);
  color: #ffffff;
}

/* Hero Section */
.hero {
  text-align: center;
  margin-bottom: 32px;
}

.hero-title {
  font-size: 36px;
  font-weight: 800;
  letter-spacing: -0.5px;
  margin-bottom: 8px;
}

.hero-title span {
  color: var(--primary-emerald);
}

.hero-subtitle {
  color: var(--text-muted);
  font-size: 15px;
}

.platforms-pills {
  display: flex;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 16px;
}

.badge {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
}

/* Card Input Box */
.input-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow-md);
  margin-bottom: 24px;
}

.input-group {
  display: flex;
  gap: 10px;
}

.input-url {
  flex: 1;
  padding: 16px 20px;
  border-radius: 12px;
  border: 2px solid var(--border-color);
  font-size: 16px;
  outline: none;
  transition: border-color 0.2s;
}

.input-url:focus {
  border-color: var(--primary-emerald);
}

.btn-paste {
  background: var(--bg-main);
  border: 1px solid var(--border-color);
  padding: 0 16px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  color: var(--text-muted);
}

.btn-submit {
  width: 100%;
  margin-top: 14px;
  padding: 16px;
  background-color: var(--primary-emerald);
  color: #ffffff;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-submit:hover {
  background-color: var(--primary-hover);
}

/* Result Section */
.results-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow-md);
  margin-bottom: 24px;
  display: none;
}

.media-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
  margin-top: 16px;
}

.media-item {
  background: var(--bg-main);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 12px;
  text-align: center;
}

.media-preview {
  width: 100%;
  max-height: 250px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 10px;
}

.btn-download {
  display: inline-block;
  width: 100%;
  padding: 10px;
  background-color: var(--primary-emerald);
  color: #ffffff;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 700;
  font-size: 14px;
}

/* Ad Container */
.ad-slot {
  margin: 20px 0;
  text-align: center;
  min-height: 90px;
  background: #f1f5f9;
  border: 1px dashed var(--border-color);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  font-size: 12px;
}
```

- [ ] **Step 2: Create `static/index.html`**

```html
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ki.Downloader - Pengunduh Video Multi Medsos</title>
  <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
  <div class="container">
    <header class="header">
      <div class="logo">Ki<span>.Downloader</span></div>
      <button class="btn-embed-trigger" onclick="openEmbedModal()">⚡ Embed ke Web Saya</button>
    </header>

    <!-- Top Header Ad Slot -->
    <div id="ad-header" class="ad-slot">Iklan Header (728x90 / 320x50)</div>

    <section class="hero">
      <h1 class="hero-title">Download Video <span>Tanpa Watermark</span></h1>
      <p class="hero-subtitle">Unduh video & foto dari TikTok, Instagram, YouTube, Twitter/X, FB, dan lainnya.</p>
      <div class="platforms-pills">
        <span class="badge">TikTok No-WM</span>
        <span class="badge">IG Reels & Carousel</span>
        <span class="badge">YouTube HD & MP3</span>
        <span class="badge">Twitter/X</span>
        <span class="badge">Facebook</span>
        <span class="badge">Pinterest</span>
      </div>
    </section>

    <main class="input-card">
      <div class="input-group">
        <input type="text" id="urlInput" class="input-url" placeholder="Tempelkan link video di sini...">
        <button class="btn-paste" onclick="pasteClipboard()">📋 Tempel</button>
      </div>
      <button class="btn-submit" id="btnCheck" onclick="processDownload()">⬇️ Download Sekarang</button>
    </main>

    <!-- Mid Form Ad Slot -->
    <div id="ad-mid" class="ad-slot">Iklan Mid Form</div>

    <section id="resultsCard" class="results-card">
      <h3 id="mediaTitle">Hasil Download</h3>
      <div id="mediaGrid" class="media-grid"></div>
    </section>
  </div>

  <!-- Script Imports -->
  <script src="/static/js/ads-config.js"></script>
  <script src="/static/js/main.js"></script>
</body>
</html>
```

- [ ] **Step 3: Commit UI components**

```bash
git add static/index.html static/css/style.css
git commit -m "feat: create clean light emerald UI layout and design tokens"
```

---

### Task 5: Monetization Ad Slots Manager (`static/js/ads-config.js` & `static/js/main.js`)

**Files:**
- Create: `static/js/ads-config.js`
- Create: `static/js/main.js`

- [ ] **Step 1: Create `static/js/ads-config.js`**

```javascript
const ADS_CONFIG = {
  enabled: true,
  slots: {
    header: {
      active: true,
      code: '<div style="padding:15px; color:#64748b; font-weight:600;">[ Slot Iklan Banner Header ]</div>'
    },
    midForm: {
      active: true,
      code: '<div style="padding:15px; color:#64748b; font-weight:600;">[ Slot Iklan Banner Mid Form ]</div>'
    },
    nativeResult: {
      active: true,
      code: '<div style="padding:15px; color:#64748b; font-weight:600;">[ Slot Iklan Native Result ]</div>'
    }
  }
};

function renderAds() {
  if (!ADS_CONFIG.enabled) return;
  
  const headerAd = document.getElementById("ad-header");
  if (headerAd && ADS_CONFIG.slots.header.active) {
    headerAd.innerHTML = ADS_CONFIG.slots.header.code;
  }
  
  const midAd = document.getElementById("ad-mid");
  if (midAd && ADS_CONFIG.slots.midForm.active) {
    midAd.innerHTML = ADS_CONFIG.slots.midForm.code;
  }
}

document.addEventListener("DOMContentLoaded", renderAds);
```

- [ ] **Step 2: Create `static/js/main.js` for handling clipboard paste & backend API interaction**

```javascript
async function pasteClipboard() {
  try {
    const text = await navigator.clipboard.readText();
    if (text) {
      document.getElementById("urlInput").value = text;
    }
  } catch (err) {
    alert("Gagal membaca clipboard. Tempelkan link secara manual.");
  }
}

async function processDownload() {
  const urlInput = document.getElementById("urlInput").value.trim();
  const btnCheck = document.getElementById("btnCheck");
  const resultsCard = document.getElementById("resultsCard");
  const mediaGrid = document.getElementById("mediaGrid");

  if (!urlInput) {
    alert("Harap masukkan link video!");
    return;
  }

  btnCheck.disabled = true;
  btnCheck.innerText = "⏳ Sedang memproses media...";
  resultsCard.style.display = "none";
  mediaGrid.innerHTML = "";

  try {
    const res = await fetch("/api/download", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: urlInput })
    });

    const data = await res.json();
    if (res.ok && data.status === "success") {
      resultsCard.style.display = "block";
      document.getElementById("mediaTitle").innerText = `Ditemukan ${data.files.length} File Media`;

      data.files.forEach((file, index) => {
        const card = document.createElement("div");
        card.className = "media-item";

        let previewHtml = "";
        if (file.is_image) {
          previewHtml = `<img src="${file.relative_url}" class="media-preview">`;
        } else if (file.is_video) {
          previewHtml = `<video src="${file.relative_url}" class="media-preview" controls></video>`;
        }

        card.innerHTML = `
          ${previewHtml}
          <a href="${file.relative_url}" download="${file.filename}" class="btn-download">⬇️ Download Media #${index + 1}</a>
        `;
        mediaGrid.appendChild(card);
      });
    } else {
      alert(data.detail || "Gagal memproses video.");
    }
  } catch (err) {
    alert("Terjadi kesalahan jaringan atau server.");
  } finally {
    btnCheck.disabled = false;
    btnCheck.innerText = "⬇️ Download Sekarang";
  }
}

function openEmbedModal() {
  const embedCode = `<iframe src="${window.location.origin}/embed" width="100%" height="480" frameborder="0"></iframe>`;
  prompt("Salin kode iframe berikut untuk dipasang di website Anda:", embedCode);
}
```

- [ ] **Step 3: Commit JS modules**

```bash
git add static/js/ads-config.js static/js/main.js
git commit -m "feat: implement ad slot manager and main application JS logic"
```

---

### Task 6: Cross-Site Embed Engine (`static/embed.html`)

**Files:**
- Create: `static/embed.html`
- Modify: `app/main.py`

- [ ] **Step 1: Create `static/embed.html`**

```html
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ki.Downloader Embed Widget</title>
  <link rel="stylesheet" href="/static/css/style.css">
  <style>
    body { background: #ffffff; padding: 10px; }
    .container { max-width: 100%; padding: 0; }
    .header, .hero, .btn-embed-trigger, #ad-header { display: none; }
  </style>
</head>
<body>
  <div class="container">
    <div style="text-align:center; font-weight:800; font-size:18px; margin-bottom:12px; color:#059669;">
      ⚡ Video Downloader Widget
    </div>
    <main class="input-card" style="box-shadow:none; border:1px solid #e2e8f0;">
      <div class="input-group">
        <input type="text" id="urlInput" class="input-url" placeholder="Tempel link video...">
        <button class="btn-paste" onclick="pasteClipboard()">📋 Tempel</button>
      </div>
      <button class="btn-submit" id="btnCheck" onclick="processDownload()">⬇️ Download Now</button>
    </main>

    <section id="resultsCard" class="results-card" style="box-shadow:none;">
      <h3 id="mediaTitle">Hasil Download</h3>
      <div id="mediaGrid" class="media-grid"></div>
    </section>
  </div>

  <script src="/static/js/ads-config.js"></script>
  <script src="/static/js/main.js"></script>
</body>
</html>
```

- [ ] **Step 2: Commit embed module**

```bash
git add static/embed.html
git commit -m "feat: create lightweight embeddable widget page"
```

---

### Task 7: Full Integration Testing & Verification

**Files:**
- Test: `tests/test_full_app.py`

- [ ] **Step 1: Create full integration test in `tests/test_full_app.py`**

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_index_page_returns_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "Ki.Downloader" in response.text

def test_embed_page_returns_html():
    response = client.get("/embed")
    assert response.status_code == 200
    assert "Video Downloader Widget" in response.text
```

- [ ] **Step 2: Run pytest across full test suite**

Run: `python -m pytest tests/ -v`
Expected: ALL PASS

- [ ] **Step 3: Commit final test suite**

```bash
git add tests/test_full_app.py
git commit -m "test: add integration tests for index and embed routes"
```
