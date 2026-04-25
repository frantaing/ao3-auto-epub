"""
Module: extractor
Handles parsing HTML bookmark files and extracting AO3 work data.
"""

import os
import re

def extract_ao3_links(file_path):
    """
    Reads an HTML bookmark file and extracts AO3 work IDs with their folder context.

    Args:
        file_path (str): Path to the bookmarks HTML file.

    Returns:
        dict: A dictionary mapping work IDs to their URL and folder path.
              Format: {
                '12345': {
                  'url': 'https://archiveofourown.org/works/12345',
                  'folder_path': ['ASOIAF']   # [] if bookmarked at root
                }
              }
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found.")

    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    fics = {}
    folder_stack = []  # Tracks current folder nesting

    # Tokenize the file line by line — the Netscape format is line-oriented
    for line in html_content.splitlines():
        line = line.strip()

        # --- Folder open: <DT><H3 ...>Folder Name</H3> ---
        folder_match = re.search(r'<H3[^>]*>([^<]+)</H3>', line, re.IGNORECASE)
        if folder_match:
            folder_name = folder_match.group(1).strip()
            folder_stack.append(folder_name)
            continue

        # --- Folder close: </DL> signals we've left the current folder ---
        if re.search(r'</DL>', line, re.IGNORECASE):
            if folder_stack:
                folder_stack.pop()
            continue

        # --- Link: <DT><A HREF="..."> ---
        link_match = re.search(r'<A\s+HREF="([^"]+)"', line, re.IGNORECASE)
        if link_match:
            url = link_match.group(1)
            if "archiveofourown.org/works/" in url:
                work_match = re.search(r'/works/(\d+)', url)
                if work_match:
                    work_id = work_match.group(1)
                    # Copy the stack so it isn't mutated later
                    fics[work_id] = {
                        "url": f"https://archiveofourown.org/works/{work_id}",
                        "folder_path": list(folder_stack),
                    }

    return fics