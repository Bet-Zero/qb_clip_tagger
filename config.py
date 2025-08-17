import os
from pathlib import Path

BASE_DIR = Path(os.getenv("NFL_BASE_DIR", "/Volumes/Samsung PSSD T7/NFLFilm"))
WATCH_FOLDER = Path(os.getenv("NFL_WATCH_FOLDER", str(BASE_DIR / "_ToTag")))
ELECTRON_DIR = Path(os.getenv("NFL_ELECTRON_DIR", str(BASE_DIR / "__Tools/clip_tagger_web/electron_app")))
VIDEO_EXTS = [ext.lower() for ext in os.getenv("NFL_VIDEO_EXTS", ".mp4,.mov,.mkv,.avi").split(',')]
