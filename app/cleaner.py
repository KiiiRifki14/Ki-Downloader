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
