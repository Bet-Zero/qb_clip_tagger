import os
import time
import subprocess
from queue import Queue
import threading
from flask import Flask
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Path setup
WATCH_FOLDER = "/Volumes/Samsung PSSD T7/NBAFilm/_ToTag"
DEST_FOLDER = "/Volumes/Samsung PSSD T7/NBAFilm/NBA"

# Function to launch Electron popup synchronously
def open_electron_popup(clip_filename):
    electron_path = "/Volumes/Samsung PSSD T7/NBAFilm/__Tools/clip_tagger_web/electron_app"
    command = ["npm", "start", "--prefix", electron_path, clip_filename]
    # Run and wait so localStorage is written before next clip
    subprocess.run(command)

event_queue = Queue()

def queue_worker():
    while True:
        filename = event_queue.get()
        if filename is None:
            break
        open_electron_popup(filename)
        event_queue.task_done()

worker_thread = threading.Thread(target=queue_worker, daemon=True)
worker_thread.start()


# Watchdog handler
class ClipHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".mp4"):
            time.sleep(1)  # Give the system time to finalize write
            full_path = event.src_path
            filename = os.path.basename(full_path)

            print(f"🎥 New clip detected: {filename}")
            event_queue.put(filename)

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
    # Stop queue worker
    event_queue.put(None)
    worker_thread.join()
