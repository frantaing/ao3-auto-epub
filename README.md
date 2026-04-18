# ao3-auto-epub

A CLI tool to bulk-download AO3 fics from your browser bookmarks as EPUB files.

## Requirements

```
pip install beautifulsoup4 requests
```

## Usage

**Basic - download all AO3 fics from your bookmarks:**
```bash
python main.py bookmarks.html
```

**Specify a custom output folder:**
```bash
python main.py bookmarks.html --output ~/Documents/fics
```

**Test run - only download the first 3 fics:**
```bash
python main.py bookmarks.html --limit 3
```

**Adjust the delay between requests (default is 5 seconds):**
```bash
python main.py bookmarks.html --delay 10
```

**All options together:**
```bash
python main.py bookmarks.html --output ~/Documents/fics --limit 5 --delay 10
```

EPUBs are saved to `~/Downloads/ao3-archiver/` by default.