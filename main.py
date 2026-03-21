"""
Module: main
Entry point for the AO3 Archiver CLI application.
"""

# === [ IMPORTS ] ===
import argparse
import sys
from extractor import extract_ao3_links

def main():
    # --- [ 1. CLI Configuration ] ---
    parser = argparse.ArgumentParser(description="Extract AO3 links from a bookmark HTML file.")
    parser.add_argument("file", help="Path to the bookmarks HTML file")
    args = parser.parse_args()
    
    # --- [ 2. Execution & Output ] ---
    try:
        # Get the deduplicated dictionary of fics from the extractor
        fics_data = extract_ao3_links(args.file)
        
        print(f"Found {len(fics_data)} AO3 fics!")
        
        # Convert the dictionary items to a list so the first 3 can be sliced for a preview
        preview_items = list(fics_data.items())[:3]
        for work_id, clean_url in preview_items:
            print(f"ID: {work_id} | URL: {clean_url}")
            
    except FileNotFoundError as error:
        print(error)
        sys.exit(1)

if __name__ == '__main__':
    main()