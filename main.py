# desc. here....

# === [ IMPORTS ] ===
import argparse
import sys
from extractor import extract_ao3_links

def main():
    # 1. Set up the CLI argument parser
    # 2. REQUIRE: Provide a file path
    # 3. Parse what's typed in the terminal
    # 4. TRY: Pass file to the extractor module
    parser = argparse.ArgumentParser(description="Extract AO3 links from a bookmark HTML file.")
    parser.add_argument("file", help="Path to the bookmarks HTML file")
    args = parser.parse_args()
    try:
        links = extract_ao3_links(args.file)
        print(f"Found {len(links)} AO3 fics!")
        for link in links[:3]:
            print(link)
    except FileNotFoundError as error:
        print(error)
        sys.exit(1)

if __name__ == '__main__':
    main()