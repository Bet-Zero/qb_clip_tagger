# File renaming and tag saving logic
# tag_utils.py
import os
import json
import shutil
import logging
from pathlib import Path
from datetime import datetime
import uuid

import config

logging.basicConfig(level=logging.INFO)

BASE_DIR = config.BASE_DIR

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

    # Rename file with unique suffix
    ext = Path(clip_path).suffix
    unique = datetime.now().strftime("%Y%m%d%H%M%S") + "_" + uuid.uuid4().hex[:6]
    new_name = f"{playtype}_{situation}_{outcome}_{unique}{ext}"
    new_dir = BASE_DIR / player / side
    try:
        new_dir.mkdir(parents=True, exist_ok=True)
        new_path = new_dir / new_name
        shutil.move(clip_path, new_path)
    except Exception as exc:
        logging.error("Failed to move clip %s -> %s: %s", clip_path, new_path, exc)
        raise

    # Save tags
    log_path = BASE_DIR / player / "tag_log.json"
    log = []
    if log_path.exists():
        try:
            with open(log_path, "r") as f:
                log = json.load(f)
        except Exception as exc:
            logging.error("Failed to load log %s: %s", log_path, exc)
            log = []

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

    try:
        with open(log_path, "w") as f:
            json.dump(log, f, indent=2)
    except Exception as exc:
        logging.error("Failed to write log %s: %s", log_path, exc)
        raise

    logging.info("✅ Saved + moved: %s", new_name)

