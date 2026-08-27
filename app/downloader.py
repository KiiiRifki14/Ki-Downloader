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
