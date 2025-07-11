import os
import json
from pathlib import Path
import importlib

import tempfile

import pytest


def test_process_clip_tags(monkeypatch, tmp_path):
    base = tmp_path / "NBAFilm"
    base.mkdir()
    monkeypatch.setenv("NBA_BASE_DIR", str(base))
    monkeypatch.syspath_prepend(os.getcwd())
    # reload modules with new env
    config = importlib.import_module("config")
    importlib.reload(config)
    tag_utils = importlib.import_module("tag_utils")
    importlib.reload(tag_utils)

    clip_dir = tmp_path / "watch"
    clip_dir.mkdir()
    clip_path = clip_dir / "test.mp4"
    clip_path.write_text("data")

    data = {
        "player": ["Jordan"],
        "side": ["Offense"],
        "playtype": ["dunk"],
        "outcome": ["Make"],
        "traits": [],
        "roles": [],
        "subroles": [],
        "badges": [],
        "context": [""],
        "situation": ["iso"],
        "quality": ["Good"],
    }

    tag_utils.process_clip_tags(str(clip_path), data)

    player_dir = base / "Jordan" / "Offense"
    files = list(player_dir.iterdir())
    assert len(files) == 1
    saved = files[0]
    assert saved.name == "dunk_iso_Make.mp4"
    log_path = base / "Jordan" / "tag_log.json"
    with open(log_path) as f:
        log = json.load(f)
    assert log[0]["filename"] == saved.name


def test_process_clip_tags_duplicates(monkeypatch, tmp_path):
    base = tmp_path / "NBAFilm"
    base.mkdir()
    monkeypatch.setenv("NBA_BASE_DIR", str(base))
    monkeypatch.syspath_prepend(os.getcwd())
    config = importlib.import_module("config")
    importlib.reload(config)
    tag_utils = importlib.import_module("tag_utils")
    importlib.reload(tag_utils)

    clip_dir = tmp_path / "watch"
    clip_dir.mkdir()
    clip1 = clip_dir / "a.mp4"
    clip1.write_text("data")
    clip2 = clip_dir / "b.mp4"
    clip2.write_text("data")

    data = {
        "player": ["Jordan"],
        "side": ["Offense"],
        "playtype": ["dunk"],
        "outcome": ["Make"],
        "traits": [],
        "roles": [],
        "subroles": [],
        "badges": [],
        "context": [""],
        "situation": ["iso"],
        "quality": ["Good"],
    }

    tag_utils.process_clip_tags(str(clip1), data)
    tag_utils.process_clip_tags(str(clip2), data)

    player_dir = base / "Jordan" / "Offense"
    names = sorted(p.name for p in player_dir.iterdir())
    assert names == ["dunk_iso_Make.mp4", "dunk_iso_Make_1.mp4"]