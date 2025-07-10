import argparse
import json
from pathlib import Path

import config


def load_logs():
    logs = []
    base = config.BASE_DIR
    if not base.exists():
        return logs
    for player_dir in base.iterdir():
        if player_dir.is_dir() and not player_dir.name.startswith(("_", ".")):
            log_path = player_dir / "tag_log.json"
            if log_path.exists():
                try:
                    with open(log_path, "r") as f:
                        data = json.load(f)
                    for entry in data:
                        entry["player"] = player_dir.name
                    logs.extend(data)
                except Exception:
                    pass
    return logs


def matches(entry, filters):
    for key, val in filters.items():
        if not val:
            continue
        if isinstance(val, list):
            if not set(val).issubset(set(entry.get(key, []))):
                return False
        else:
            if str(entry.get(key, "")) != str(val):
                return False
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description="Search tagged clips")
    parser.add_argument("--player")
    parser.add_argument("--side")
    parser.add_argument("--playtype")
    parser.add_argument("--outcome")
    parser.add_argument("--context")
    parser.add_argument("--situation")
    parser.add_argument("--trait", action="append", dest="traits")
    parser.add_argument("--role", action="append", dest="roles")
    parser.add_argument("--subrole", action="append", dest="subroles")
    parser.add_argument("--badge", action="append", dest="badges")

    args = parser.parse_args(argv)

    filters = {
        "player": args.player,
        "side": args.side,
        "playtype": args.playtype,
        "outcome": args.outcome,
        "context": args.context,
        "situation": args.situation,
        "traits": args.traits,
        "roles": args.roles,
        "subroles": args.subroles,
        "badges": args.badges,
    }

    logs = load_logs()
    results = [e for e in logs if matches(e, filters)]
    for e in results:
        path = Path(config.BASE_DIR) / e["player"] / e["side"] / e["filename"]
        print(path)


if __name__ == "__main__":
    main()

