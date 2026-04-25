"""
Module: extractor
Handles parsing HTML bookmark files and extracting AO3 work data.
"""

import os
import re
from bs4 import BeautifulSoup

def _parse_folder(dl_tag, folder_path):
    """
    Recursively walks a <DL> block, tracking the current folder path.

    Args:
        dl_tag (Tag): A BeautifulSoup <DL> tag to walk.
        folder_path (list[str]): The current folder hierarchy, e.g. ["ASOIAF"] or [].

    Returns:
        dict: Discovered AO3 fics in the format:
              {'12345': {'url': 'https://archiveofourown.org/works/12345', 'folder_path': ['ASOIAF']}}
    """
    fics = {}

    # Each direct child <DT> is either a link or a folder header
    for dt in dl_tag.find_all("dt", recursive=False):

        # --- Folder: <DT><H3>Folder Name</H3> followed by a <DL> ---
        h3 = dt.find("h3")
        if h3:
            subfolder_name = h3.get_text(strip=True)
            nested_dl = dt.find_next_sibling("dl")
            if nested_dl:
                # Recurse into the subfolder, extending the path
                fics.update(_parse_folder(nested_dl, folder_path + [subfolder_name]))
            continue

        # --- Link: <DT><A href="..."> ---
        a_tag = dt.find("a")
        if not a_tag:
            continue

        url = a_tag.get("href", "")
        if "archiveofourown.org/works/" not in url:
            continue

        match = re.search(r"/works/(\d+)", url)
        if not match:
            continue

        work_id = match.group(1)
        fics[work_id] = {
            "url": f"https://archiveofourown.org/works/{work_id}",
            "folder_path": folder_path,  # [] means root, no subfolder
        }

    return fics


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

    soup = BeautifulSoup(html_content, "html.parser")

    # The top-level <DL> is the root of the bookmark tree
    root_dl = soup.find("dl")
    if not root_dl:
        return {}

    return _parse_folder(root_dl, folder_path=[])