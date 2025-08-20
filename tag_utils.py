# File renaming and tag saving logic
# tag_utils.py
import os
import json
import shutil
import logging
from pathlib import Path

import config

logging.basicConfig(level=logging.INFO)

BASE_DIR = config.BASE_DIR

def process_clip_tags(clip_path, data):
    player = data.get("player", [""])[0]
    playtype = data.get("playtype", [""])[0]
    outcome = data.get("outcome", [""])[0]

    # Split comma-separated strings into arrays
    traits = data.get("traits", [""])[0].split(",") if data.get("traits") else []
    roles = data.get("roles", [""])[0].split(",") if data.get("roles") else []
    subroles = data.get("subroles", [""])[0].split(",") if data.get("subroles") else []
    badges = data.get("badges", [""])[0].split(",") if data.get("badges") else []
    # Remove any empty strings that result from trailing commas
    traits = [t for t in traits if t]
    roles = [r for r in roles if r]
    subroles = [s for s in subroles if s]
    badges = [b for b in badges if b]

    context = data.get("context", [""])[0]
    situation = data.get("situation", [""])[0]
    quality = data.get("quality", ["Good"])[0]

    # Rename file with incrementing numeric suffix if needed
    ext = Path(clip_path).suffix
    base_name = f"{playtype}_{situation}_{outcome}"
    new_dir = BASE_DIR / player
    try:
        new_dir.mkdir(parents=True, exist_ok=True)
        count = 0
        candidate = new_dir / f"{base_name}{ext}"
        while candidate.exists():
            count += 1
            candidate = new_dir / f"{base_name}_{count}{ext}"
        new_path = candidate
        shutil.move(clip_path, new_path)
        new_name = new_path.name
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

    log.append(
        {
            "filename": new_name,
            "playtype": playtype,
            "outcome": outcome,
            "traits": traits,
            "roles": roles,
            "subroles": subroles,
            "badges": badges,
            "context": context,
            "situation": situation,
            "quality": quality,
        }
    )

    try:
        with open(log_path, "w") as f:
            json.dump(log, f, indent=2)
    except Exception as exc:
        logging.error("Failed to write log %s: %s", log_path, exc)
        raise

    logging.info("✅ Saved + moved: %s", new_name)

