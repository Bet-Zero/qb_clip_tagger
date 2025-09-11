# app.py
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_file,
    abort,
)
from pathlib import Path
import logging
import os
import sys
import subprocess
import tempfile
import shutil
import threading
import time

import config
from tag_utils import process_clip_tags
from search_clips import load_logs, matches

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Store path separately so we can reuse it
CLIP_STATE = {"filename": "", "path": ""}


# Helper to list player folders
def get_player_names():
    base = config.BASE_DIR
    names = []
    if base.exists():
        for entry in base.iterdir():
            if entry.is_dir() and not entry.name.startswith("_") and not entry.name.startswith("."):
                names.append(entry.name)

    # Return names in alphabetical order for nicer suggestions
    names.sort(key=lambda n: n.lower())
    return names

@app.route("/players")
def players():
    return jsonify({"players": get_player_names()})


@app.route("/clip/<player>/<year>/<path:filename>")
def serve_clip(player, year, filename):
    """Return the video file for the given player/year/filename."""
    path = Path(config.BASE_DIR) / player / year / filename
    if not path.exists():
        # Fallback: try old flat structure for backward compatibility
        old_path = Path(config.BASE_DIR) / player / filename
        if old_path.exists():
            path = old_path
        else:
            abort(404)
    return send_file(path)


@app.route("/search")
def search_page():
    players = get_player_names()
    results = []
    if request.args:
        # Split comma-separated strings into arrays and filter out empty strings
        filters = {
            "player": request.args.get("player"),
            "playtype": request.args.get("playtype"),
            "outcome": request.args.get("outcome"),
            "context": request.args.get("context"),
            "situation": request.args.get("situation"),
            "quality": request.args.get("quality"),
            "distance": request.args.get("distance"),
            "year": request.args.get("year"),
            "traits": [t for t in request.args.get("traits", "").split(",") if t],
            "roles": [r for r in request.args.get("roles", "").split(",") if r],
            "subroles": [s for s in request.args.get("subroles", "").split(",") if s],
            "badges": [b for b in request.args.get("badges", "").split(",") if b],
            # Game information fields
            "opponent": request.args.get("opponent"),
            "home_away": request.args.get("home_away"),
            "quarter": request.args.get("quarter"),
            "down": request.args.get("down"),
        }
        logs = load_logs()
        for entry in logs:
            if matches(entry, filters):
                year = entry.get("year", "2025")  # Default year for backward compatibility
                path = Path(config.BASE_DIR) / entry["player"] / year / entry["filename"]
                results.append(
                    {
                        "label": f"{entry['player']}: {entry['filename']} ({year})",
                        "full_path": str(path),
                        "player": entry["player"],
                        "year": year,
                        "filename": entry["filename"],
                    }
                )
    return render_template("search.html", players=players, results=results, args=request.args)


def reveal_in_finder(path):
    if sys.platform.startswith("darwin"):
        subprocess.run(["open", "-R", path])
    elif os.name == "nt":
        subprocess.run(["explorer", "/select,", path])
    else:
        subprocess.run(["xdg-open", os.path.dirname(path)])


@app.route("/reveal", methods=["POST"])
def reveal():
    data = request.get_json()
    path = data.get("path") if data else None
    if not path:
        return jsonify({"error": "no path"}), 400
    try:
        reveal_in_finder(path)
    except Exception as exc:
        logging.error("Failed to reveal %s: %s", path, exc)
        return jsonify({"error": "failed"}), 500
    return jsonify({"status": "ok"})


def schedule_cleanup(dir_path):
    def _cleanup():
        time.sleep(20)
        shutil.rmtree(dir_path, ignore_errors=True)

    threading.Thread(target=_cleanup, daemon=True).start()


@app.route("/reveal_list", methods=["POST"])
def reveal_list():
    data = request.get_json()
    paths = data.get("paths") if data else None
    if not paths:
        return jsonify({"error": "no paths"}), 400
    try:
        tmpdir = tempfile.mkdtemp(prefix="clip_list_")
        for p in paths:
            name = os.path.basename(p)
            dest = os.path.join(tmpdir, name)
            try:
                os.symlink(p, dest)
            except Exception:
                shutil.copy(p, dest)
        if sys.platform.startswith("darwin"):
            subprocess.run(["open", tmpdir])
        elif os.name == "nt":
            subprocess.run(["explorer", tmpdir])
        else:
            subprocess.run(["xdg-open", tmpdir])
        schedule_cleanup(tmpdir)
    except Exception as exc:
        logging.error("Failed to reveal list: %s", exc)
        return jsonify({"error": "failed"}), 500
    return jsonify({"status": "ok"})


@app.route("/tag")
def tag_form():
    clip_name = request.args.get("file", "")  # <- match Electron URL ?file=...
    CLIP_STATE["filename"] = clip_name
    clip_path = config.WATCH_FOLDER / clip_name
    if clip_name and clip_path.exists():
        CLIP_STATE["path"] = str(clip_path)
    else:
        CLIP_STATE["path"] = ""
    return render_template("tagger.html", clip=CLIP_STATE)

@app.route("/submit", methods=["POST"])
def submit():
    logging.info("📩 Form submitted")

    if CLIP_STATE["path"]:
        logging.info(f"📂 Saving tags for: {CLIP_STATE['path']}")
        data = request.form.to_dict(flat=False)
        logging.info("🧠 Tag data: %s", data)
        try:
            process_clip_tags(CLIP_STATE["path"], data)
        except Exception as exc:
            logging.error("Failed to process clip: %s", exc)
    else:
        logging.warning("⚠️ No valid clip path found, skipping save.")

    # Reset clip state
    CLIP_STATE["filename"] = ""
    CLIP_STATE["path"] = ""
    # Return small page that closes the Electron window
    return render_template("close.html")


if __name__ == "__main__":    app.run(debug=True)