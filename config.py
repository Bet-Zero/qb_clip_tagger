import os
from pathlib import Path

BASE_DIR = Path(os.getenv("NBA_BASE_DIR", "/Volumes/Samsung PSSD T7/NBAFilm"))
WATCH_FOLDER = Path(os.getenv("NBA_WATCH_FOLDER", str(BASE_DIR / "_ToTag")))
ELECTRON_DIR = Path(os.getenv("NBA_ELECTRON_DIR", str(BASE_DIR / "__Tools/clip_tagger_web/electron_app")))
VIDEO_EXTS = [ext.lower() for ext in os.getenv("NBA_VIDEO_EXTS", ".mp4,.mov,.mkv,.avi").split(',')]
