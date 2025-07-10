# NBA Clip Tagger

This tool watches a folder for new video clips and pops up a tagging UI. Tagged clips are moved into player folders with a unique filename (duplicates get numbered suffixes) and a log entry is created. A search script allows finding clips by different criteria.

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

Launch the tagger and watcher together with the `tagger` command:

```bash
./tagger
```

When new clips appear in the watch folder, the Electron UI opens for tagging.

## Searching Clips

Search using the `search` command:

```bash
./search [filters]
```

Filters such as `--player`, `--playtype`, `--trait`, etc. can be combined to narrow results. Matching clip paths are printed to stdout.

## Testing

Run tests with:

```bash
pytest
```
