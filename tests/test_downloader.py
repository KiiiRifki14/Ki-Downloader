from app.downloader import detect_platform, get_video_info

def test_detect_platform():
    assert detect_platform("https://www.tiktok.com/@user/video/123456789") == "tiktok"
    assert detect_platform("https://www.instagram.com/reel/C123456789/") == "instagram"
    assert detect_platform("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "youtube"
    assert detect_platform("https://x.com/user/status/123456789") == "twitter"
    assert detect_platform("https://unknown-domain.com") == "generic"
