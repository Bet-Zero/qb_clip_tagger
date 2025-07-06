# File renaming and tag saving logic
# tag_utils.py
import os
import json
import shutil
from pathlib import Path

BASE_DIR = Path("/Volumes/Samsung PSSD T7/NBAFilm")

def process_clip_tags(clip_path, data):
    player = data.get("player", [""])[0]
    side = data.get("side", ["Offense"])[0]
    playtype = data.get("playtype", [""])[0]
    outcome = data.get("outcome", [""])[0]

    traits = data.get("traits", [])
    roles = data.get("roles", [])
    subroles = data.get("subroles", [])
    badges = data.get("badges", [])
    context = data.get("context", [""])[0]
    situation = data.get("situation", [""])[0]

    # Rename file
    new_name = f"{playtype}_{outcome}.mp4"
    new_dir = BASE_DIR / player / side
    new_dir.mkdir(parents=True, exist_ok=True)
    new_path = new_dir / new_name
    shutil.move(clip_path, new_path)

    # Save tags
    log_path = BASE_DIR / player / "tag_log.json"
    log = []
    if log_path.exists():
        with open(log_path, "r") as f:
            log = json.load(f)

    log.append({
        "filename": new_name,
        "side": side,
        "playtype": playtype,
        "outcome": outcome,
        "traits": traits,
        "roles": roles,
        "subroles": subroles,
        "badges": badges,
        "context": context,
        "situation": situation
    })

    with open(log_path, "w") as f:
        json.dump(log, f, indent=2)

    print(f"✅ Saved + moved: {new_name}")
