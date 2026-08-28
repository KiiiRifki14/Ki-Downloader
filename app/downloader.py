import os
import uuid
import re
import requests
import yt_dlp
import instaloader
from pathlib import Path

# Clear invalid SSL CA cert bundle variables if set on host machine (e.g. XAMPP on Windows)
for env_var in ("CURL_CA_BUNDLE", "SSL_CERT_FILE", "REQUESTS_CA_BUNDLE"):
    if env_var in os.environ and not os.path.exists(os.environ[env_var]):
        os.environ.pop(env_var, None)

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
    except Exception:
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
                max_connection_attempts=1,
                request_timeout=5.0,
                save_metadata=False,
                download_videos=True,
                download_video_thumbnails=False,
                download_geotags=False,
                download_comments=False,
                compress_json=False
            )
            
            # 1. Instagram Post or Reel
            if "/p/" in url or "/reel/" in url:
                try:
                    shortcode = url.split("/p/")[1].split("/")[0] if "/p/" in url else url.split("/reel/")[1].split("/")[0]
                    post = instaloader.Post.from_shortcode(L.context, shortcode)
                    L.download_post(post, target=target_dir)
                except Exception:
                    # Fallback yt-dlp for Post/Reel
                    outtmpl = str(target_dir / "%(title)s.%(ext)s")
                    ydl_opts = {
                        "outtmpl": outtmpl,
                        "quiet": True,
                        "noplaylist": True,
                        "format": "bestvideo+bestaudio/best",
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])

            # 2. Instagram Profile (Profile Picture DP HD + Stories + Highlights)
            elif "/stories/" not in url and not (url.endswith("/p/") or "/p/" in url) and not (url.endswith("/reel/") or "/reel/" in url):
                clean_url = url.split("instagram.com/")[1].strip("/")
                username = clean_url.split("/")[0].split("?")[0]
                if username:
                    # Method A: Instaloader Profile
                    try:
                        profile = instaloader.Profile.from_username(L.context, username)
                        pic_url = profile.profile_pic_url_hd or profile.profile_pic_url
                        if pic_url:
                            r_img = requests.get(pic_url, timeout=10)
                            if r_img.status_code == 200:
                                with open(target_dir / f"{username}_profile_pic.jpg", "wb") as f_img:
                                    f_img.write(r_img.content)
                        
                        # Attempt stories & highlights
                        try:
                            for story in L.get_stories(userids=[profile.userid]):
                                for item in story.get_items():
                                    L.download_storyitem(item, target=target_dir)
                        except Exception:
                            pass
                    except Exception:
                        pass

                    # Method B: Direct Instagram Scraping Fallback if Instaloader is rate limited
                    if not any(target_dir.iterdir()):
                        try:
                            headers = {
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                                "X-IG-App-ID": "936619743392459"
                            }
                            api_url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
                            r_api = requests.get(api_url, headers=headers, timeout=10)
                            if r_api.status_code == 200:
                                data = r_api.json()
                                user_data = data.get("data", {}).get("user", {})
                                pic_url = user_data.get("profile_pic_url_hd") or user_data.get("profile_pic_url")
                                if pic_url:
                                    r_img = requests.get(pic_url, timeout=10)
                                    if r_img.status_code == 200:
                                        with open(target_dir / f"{username}_profile_pic.jpg", "wb") as f_img:
                                            f_img.write(r_img.content)
                        except Exception:
                            pass

            # 3. Publer API Fallback for Instagram Media
            if not any(target_dir.iterdir()):
                try:
                    publer_headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                        "Content-Type": "application/json",
                        "Origin": "https://publer.io",
                        "Referer": "https://publer.io/tools/media-downloader"
                    }
                    r_pub = requests.post(
                        "https://publer.io/api/v1/media/download",
                        json={"url": url, "iphone": False},
                        headers=publer_headers,
                        timeout=15
                    )
                    if r_pub.status_code == 200 and len(r_pub.content) > 10000:
                        out_file = target_dir / "instagram_media.mp4"
                        with open(out_file, "wb") as f_out:
                            f_out.write(r_pub.content)
                except Exception:
                    pass

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

        # Scan target folder (including subdirectories created by Instaloader)
        for root, dirs, files in os.walk(target_dir):
            for f in files:
                if f.endswith(('.jpg', '.jpeg', '.png', '.mp4', '.webm', '.m4a', '.mp3')):
                    full_path = Path(root) / f
                    rel_name = full_path.name
                    # Move subfolder file to target_dir root if needed
                    if full_path.parent != target_dir:
                        dest = target_dir / rel_name
                        full_path.rename(dest)
                        full_path = dest
                    
                    found_files.append({
                        "filename": rel_name,
                        "filepath": str(full_path),
                        "relative_url": f"/api/file/{session_id}/{rel_name}",
                        "is_video": rel_name.endswith(('.mp4', '.webm')),
                        "is_image": rel_name.endswith(('.jpg', '.jpeg', '.png'))
                    })
        
        found_files.sort(key=lambda x: x["filename"])
        return session_id, found_files

    except Exception:
        # Final fallback with yt-dlp
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

            for root, dirs, files in os.walk(target_dir):
                for f in files:
                    if f.endswith(('.jpg', '.jpeg', '.png', '.mp4', '.webm', '.m4a', '.mp3')):
                        full_path = Path(root) / f
                        rel_name = full_path.name
                        if full_path.parent != target_dir:
                            dest = target_dir / rel_name
                            full_path.rename(dest)
                            full_path = dest
                        found_files.append({
                            "filename": rel_name,
                            "filepath": str(full_path),
                            "relative_url": f"/api/file/{session_id}/{rel_name}",
                            "is_video": rel_name.endswith(('.mp4', '.webm')),
                            "is_image": rel_name.endswith(('.jpg', '.jpeg', '.png'))
                        })
            found_files.sort(key=lambda x: x["filename"])
            return session_id, found_files
        except Exception:
            return session_id, []
