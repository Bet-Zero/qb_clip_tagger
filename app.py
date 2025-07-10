# app.py
from flask import Flask, render_template, request, redirect, jsonify
from pathlib import Path
import logging

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
    return names


@app.route("/players")
def players():
    return jsonify({"players": get_player_names()})


@app.route("/search")
def search_page():
    players = get_player_names()
    results = []
    if request.args:
        filters = {
            "player": request.args.get("player"),
            "side": request.args.get("side"),
            "playtype": request.args.get("playtype"),
            "outcome": request.args.get("outcome"),
            "context": request.args.get("context"),
            "situation": request.args.get("situation"),
            "traits": request.args.get("traits", "").split(",") if request.args.get("traits") else [],
            "roles": request.args.get("roles", "").split(",") if request.args.get("roles") else [],
            "subroles": request.args.get("subroles", "").split(",") if request.args.get("subroles") else [],
            "badges": request.args.get("badges", "").split(",") if request.args.get("badges") else [],
        }
        logs = load_logs()
        for entry in logs:
            if matches(entry, filters):
                path = Path(config.BASE_DIR) / entry["player"] / entry["side"] / entry["filename"]
                results.append({
                    "label": f"{entry['player']}/{entry['side']}/{entry['filename']}",
                    "full_path": str(path),
                })
    return render_template("search.html", players=players, results=results, args=request.args)

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
