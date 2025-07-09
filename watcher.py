import os
import time
import subprocess
from queue import Queue
import threading
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import config

# Path setup
WATCH_FOLDER = config.WATCH_FOLDER
DEST_FOLDER = config.BASE_DIR

# Function to launch Electron popup synchronously
def open_electron_popup(clip_filename):
    electron_path = config.ELECTRON_DIR
    command = ["npm", "start", "--prefix", str(electron_path), clip_filename]
    # Run and wait so localStorage is written before next clip
    try:
        subprocess.run(command, check=True)
    except Exception as exc:
        logging.error("Failed to launch Electron for %s: %s", clip_filename, exc)

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
        if not event.is_directory and Path(event.src_path).suffix.lower() in config.VIDEO_EXTS:
            time.sleep(1)  # Give the system time to finalize write
            full_path = event.src_path
            filename = os.path.basename(full_path)

            logging.info("🎥 New clip detected: %s", filename)
            event_queue.put(filename)

# Main watcher logic
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("✅ Watching for new clips in: %s", WATCH_FOLDER)
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


