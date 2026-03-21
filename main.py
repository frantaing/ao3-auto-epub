"""
Module: main
Entry point for the AO3 Archiver CLI application.
"""

# --- [ Imports ] ---
import argparse
import sys
from extractor import extract_ao3_links
from downloader import download_epub

def main():
    # ---[ 1. CLI config ] ---
    parser = argparse.ArgumentParser(description="Extract and download AO3 links from a bookmark HTML file.")
    parser.add_argument("file", help="Path to the bookmarks HTML file")
    
    # Add an optional limit flag [FOR TESTING]
    parser.add_argument(
        "--limit", 
        type=int, 
        default=0, 
        help="Maximum number of fics to download (useful for testing)"
    )
    
    args = parser.parse_args()
    
    # --- [ 2. Extraction ] ---
    try:
        fics_data = extract_ao3_links(args.file)
        print(f"Found {len(fics_data)} UNIQUE AO3 fics!")
    except FileNotFoundError as error:
        print(error)
        sys.exit(1)
        
    # --- [ 3. Downloading ] ---
    # Convert dictionary keys to a list to easily slice it
    work_ids = list(fics_data.keys())
    
    # Apply the limit if the user provided one via CLI
    if args.limit > 0:
        work_ids = work_ids[:args.limit]
        print(f"Test mode active: Limiting download to {args.limit} fics.")
        
    print("\nStarting downloads...")
    success_count = 0
    
    for work_id in work_ids:
        # flush=True forces the terminal to print this text immediately, 
        # before the time.sleep() pause kicks in.
        print(f"Downloading ID: {work_id}...", end=" ", flush=True)
        
        # Call the downloader
        if download_epub(work_id):
            print("SUCCESS")
            success_count += 1
        else:
            print("FAILED")
            
    print(f"\nFinished! Successfully downloaded {success_count}/{len(work_ids)} fics.")

if __name__ == '__main__':
    main()