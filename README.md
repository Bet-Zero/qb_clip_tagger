# NBA Clip Tagger

This tool watches a folder for new video clips and pops up a tagging UI. Tagged clips are moved into player folders with a unique filename and a log entry is created. A search script allows finding clips by different criteria.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. (Optional) Adjust paths by setting environment variables:
   - `NBA_BASE_DIR` – base directory containing player folders (default is `/Volumes/Samsung PSSD T7/NBAFilm`)
   - `NBA_WATCH_FOLDER` – folder where new clips appear (default is `<BASE_DIR>/_ToTag`)
   - `NBA_ELECTRON_DIR` – location of the Electron popup (default is `<BASE_DIR>/__Tools/clip_tagger_web/electron_app`)

## Running

Use `python tagger.py` to start the Flask server and watcher. When new clips appear in the watch folder, the Electron UI opens for tagging.

## Searching Clips

Run `python search_clips.py` with filters such as `--player`, `--playtype`, `--trait`, etc. Multiple filters narrow the results. The script outputs paths to matching clips.

## Testing

Run tests with:

```bash
pytest
```

