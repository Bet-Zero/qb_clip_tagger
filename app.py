# app.py
from flask import Flask, render_template, request, redirect, jsonify
from tag_utils import process_clip_tags
from pathlib import Path

app = Flask(__name__)

# Store path separately so we can reuse it
CLIP_STATE = {"filename": "", "path": ""}

@app.route("/players")
def players():
    base = Path("/Volumes/Samsung PSSD T7/NBAFilm")
    names = []
    if base.exists():
        for entry in base.iterdir():
            if entry.is_dir() and not entry.name.startswith("_") and not entry.name.startswith("."):
                names.append(entry.name)
    return jsonify({"players": names})

@app.route("/tag")
def tag_form():
    clip_name = request.args.get("file", "")  # <- match Electron URL ?file=...
    CLIP_STATE["filename"] = clip_name
    clip_path = Path("/Volumes/Samsung PSSD T7/NBAFilm/_ToTag") / clip_name
    if clip_name and clip_path.exists():
        CLIP_STATE["path"] = str(clip_path)
    else:
        CLIP_STATE["path"] = ""
    return render_template("tagger.html", clip=CLIP_STATE)

@app.route("/submit", methods=["POST"])
def submit():
    print("📩 Form submitted")

    if CLIP_STATE["path"]:
        print(f"📂 Saving tags for: {CLIP_STATE['path']}")
        data = request.form.to_dict(flat=False)
        print("🧠 Tag data:", data)
        process_clip_tags(CLIP_STATE["path"], data)
    else:
        print("⚠️ No valid clip path found, skipping save.")

    # Reset clip state
    CLIP_STATE["filename"] = ""
    CLIP_STATE["path"] = ""
    return redirect("/tag")


if __name__ == "__main__":
    app.run(debug=True)