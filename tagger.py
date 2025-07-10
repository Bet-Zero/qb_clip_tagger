import subprocess
import time
import signal
import os
import socket

# Paths (relative to this folder)
tagger_dir = os.getcwd()
watcher_path = os.path.join(tagger_dir, "watcher.py")


# Function to wait until Flask server is ready
def wait_for_port(host, port, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.1)
    raise RuntimeError(f"❌ Timed out waiting for {host}:{port} to become available")

def main():
    """Launch the Flask server and watcher together."""

    flask_process = subprocess.Popen([
        "python3",
        "app.py",
    ], cwd=tagger_dir)

    wait_for_port("localhost", 5000)

    watcher_process = subprocess.Popen([
        "python3",
        watcher_path,
    ])

    print("\n🚀 Tagger launched successfully.")
    print("🔁 Watching for new clips...")
    print("🛑 Press Ctrl+C to stop everything.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🧹 Shutting down...")
        flask_process.send_signal(signal.SIGINT)
        watcher_process.send_signal(signal.SIGINT)
        flask_process.wait()
        watcher_process.wait()
        print("✅ All processes stopped.")


if __name__ == "__main__":
    main()