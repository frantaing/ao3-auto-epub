# ao3-auto-epub

A CLI tool to bulk-download AO3 fics as EPUBs from your browser bookmarks export. Mirrors your bookmark folder structure, handles rate limiting, and resumes interrupted runs automatically.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py bookmarks.html
```

| Flag | Description | Default |
|------|-------------|---------|
| `--output` | Directory to save EPUBs | `~/Downloads/ao3-archiver/` |
| `--delay` | Seconds between requests | `5` |
| `--limit` | Max fics to download (useful for testing) | no limit |

**Examples:**
```bash
# Custom output folder
python main.py bookmarks.html --output ~/Documents/fics

# Test run with 3 fics
python main.py bookmarks.html --limit 3

# All options
python main.py bookmarks.html --output ~/Documents/fics --delay 10 --limit 5
```

## Notes

- EPUBs are organised into subfolders matching your bookmark folders
- Locked (members-only) works are detected and listed at the end of a run. *They are not downloaded!*
- Already-downloaded works are skipped automatically, so interrupted runs can be safely resumed
- AO3 rate limits aggressive scrapers, so the default 5s delay is intentional, don't go lower!
