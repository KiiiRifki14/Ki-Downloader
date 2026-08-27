import os
import uuid
import yt_dlp
import instaloader
import requests
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
                "title": "Instagram Media / Profile / Story",
                "thumbnail": None,
                "platform": "instagram",
                "slides_support": True
            }
        
        ydl_opts = {"quiet": True, "skip_download": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title", "Social Media Content"),
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
            
            # 1. Instagram Post or Reel
            if "/p/" in url or "/reel/" in url:
                shortcode = url.split("/p/")[1].split("/")[0] if "/p/" in url else url.split("/reel/")[1].split("/")[0]
                post = instaloader.Post.from_shortcode(L.context, shortcode)
                L.download_post(post, target=target_dir)

            # 2. Instagram Profile (Profile Picture DP HD + Stories + Highlights)
            elif "/stories/" not in url and not url.endswith("/p/") and not url.endswith("/reel/"):
                clean_url = url.split("instagram.com/")[1].strip("/")
                username = clean_url.split("/")[0].split("?")[0]
                if username:
                    profile = instaloader.Profile.from_username(L.context, username)
                    # Download Profile Picture HD
                    L.download_profilepic(profile)
                    # Attempt to download active stories
                    try:
                        for story in L.get_stories(userids=[profile.userid]):
                            for item in story.get_items():
                                L.download_storyitem(item, target=target_dir)
                    except Exception:
                        pass
                    # Attempt to download highlights / sorotan
                    try:
                        for highlight in L.get_highlights(user=profile):
                            for item in highlight.get_items():
                                L.download_storyitem(item, target=target_dir)
                    except Exception:
                        pass

            # 3. Instagram Stories / Highlights Fallback
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

        # Scan target folder for downloaded photos, videos, and avatars
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
        # Fallback to yt-dlp if instaloader encounters private/login restriction
        try:
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
        except Exception:
            return session_id, []
