"""
Module: main
Entry point for the AO3 Archiver CLI application.
"""

# --- [ Imports ] ---
import argparse
import sys
import os
import requests
from extractor import extract_ao3_links
from downloader import download_epub

def main():
    # --- [ 1. CLI config ] ---
    parser = argparse.ArgumentParser(
        description="Extract and download AO3 fics from a bookmarks HTML file."
    )
    parser.add_argument("file", help="Path to the bookmarks HTML file")
    parser.add_argument("--limit", type=int, default=0,
                        help="Max number of fics to download (for testing)")
    parser.add_argument("--delay", type=int, default=5,
                        help="Seconds to wait between requests (default: 5)")
    parser.add_argument("--output", type=str, default="downloads",
                        help="Directory to save EPUB files (default: ./downloads)")

    args = parser.parse_args()

    # --- [ 2. Prep output directory ] ---
    os.makedirs(args.output, exist_ok=True)

    # --- [ 3. Extraction ] ---
    try:
        fics_data = extract_ao3_links(args.file)
        print(f"Found {len(fics_data)} unique AO3 fics.")
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    # --- [ 4. Apply limit ] ---
    work_ids = list(fics_data.keys())
    if args.limit > 0:
        work_ids = work_ids[:args.limit]
        print(f"Test mode: limiting to {args.limit} fics.")

    # --- [ 5. Download loop ] ---
    print(f"\nSaving to: ./{args.output}/")
    print("Starting downloads...\n")

    success_count = 0
    session = requests.Session()  # reuse TCP connections across all downloads

    for work_id in work_ids:
        print(f"  Fetching ID {work_id}...", end=" ", flush=True)
        result = download_epub(work_id, session, delay=args.delay, output_dir=args.output)
        if result:
            print("✓")
            success_count += 1
        else:
            print("✗")

    print(f"\nDone. {success_count}/{len(work_ids)} downloaded successfully.")

if __name__ == "__main__":
    main()