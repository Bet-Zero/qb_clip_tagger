import os
import time
import shutil
import subprocess
from flask import Flask
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Path setup
WATCH_FOLDER = "/Volumes/Samsung PSSD T7/NBAFilm/_ToTag"
DEST_FOLDER = "/Volumes/Samsung PSSD T7/NBAFilm/NBA"

# Function to launch Electron popup
def open_electron_popup(clip_filename):
    electron_path = "/Volumes/Samsung PSSD T7/NBAFilm/__Tools/clip_tagger_web/electron_app"
    command = ["npm", "start", "--prefix", electron_path, clip_filename]
    subprocess.Popen(command)

# Watchdog handler
class ClipHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".mp4"):
            time.sleep(1)  # Give the system time to finalize write
            full_path = event.src_path
            filename = os.path.basename(full_path)

            print(f"🎥 New clip detected: {filename}")
            open_electron_popup(filename)

# Main watcher logic
if __name__ == "__main__":
    print(f"✅ Watching for new clips in: {WATCH_FOLDER}")
    observer = Observer()
    observer.schedule(ClipHandler(), path=WATCH_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
