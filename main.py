"""
Module: main
Entry point for the AO3 Archiver CLI application.
"""

import argparse
import os
import sys
import requests
from extractor import extract_ao3_links
from downloader import download_epub

DEFAULT_OUTPUT = os.path.join(os.path.expanduser("~"), "Downloads", "ao3-archiver")

def main():
    # --- [ 1. CLI config ] ---
    parser = argparse.ArgumentParser(
        description="Extract and download AO3 fics from a bookmarks HTML file."
    )
    parser.add_argument(
        "file",
        help="Path to your exported bookmarks HTML file (e.g. ~/Desktop/bookmarks.html)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Max number of fics to download. Useful for testing. (default: no limit)"
    )
    parser.add_argument(
        "--delay",
        type=int,
        default=5,
        help="Seconds to wait between requests to avoid rate limiting. (default: 5)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=DEFAULT_OUTPUT,
        help="Directory to save EPUB files. (default: ~/Downloads/ao3-archiver)"
    )

    args = parser.parse_args()

    # --- [ 2. Resolve & display paths ] ---
    input_path = os.path.abspath(args.file)
    output_path = os.path.abspath(os.path.expanduser(args.output))

    print(f"Bookmarks file : {input_path}")
    print(f"Saving EPUBs to: {output_path}")

    os.makedirs(output_path, exist_ok=True)

    # --- [ 3. Extraction ] ---
    try:
        fics_data = extract_ao3_links(input_path)
        print(f"\nFound {len(fics_data)} unique AO3 fics.")
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    # --- [ 4. Apply limit ] ---
    work_ids = list(fics_data.keys())
    if args.limit > 0:
        work_ids = work_ids[:args.limit]
        fic_word = "fic" if args.limit == 1 else "fics"
        print(f"Test mode: limiting to {args.limit} {fic_word}.")

    # --- [ 5. Download loop ] ---
    print("\nStarting downloads...\n")
    counts = {"success": 0, "skipped": 0, "locked": 0, "failed": 0}
    session = requests.Session()
    session.cookies.set("view_adult", "true", domain="archiveofourown.org")

    for work_id in work_ids:
        fic = fics_data[work_id]
        folder_path = fic["folder_path"]

        folder_label = "/".join(folder_path) if folder_path else "root"
        print(f"  [{folder_label}] Fetching ID {work_id}...", end=" ", flush=True)

        status = download_epub(
            work_id,
            session,
            folder_path=folder_path,
            delay=args.delay,
            output_dir=output_path,
        )

        counts[status] += 1

        labels = {
            "success": "✓",
            "skipped": "— skipped (already exists)",
            "locked": "— locked",
            "failed": "✗"
        }
        print(labels[status])

    print(f"\nDone.")
    print(f"  ✓  Downloaded : {counts['success']}")
    print(f"  —  Skipped    : {counts['skipped']}")
    print(f"  ⚠  Locked     : {counts['locked']}")
    print(f"  ✗  Failed     : {counts['failed']}")
    print(f"\nFiles saved to: {output_path}")

if __name__ == "__main__":
    main()