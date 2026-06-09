"""
Module: downloader
Handles the fetching and saving of EPUB files from AO3.
"""

import os
import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://archiveofourown.org"

HEADERS = {
    # AO3 is more likely to work correctly if it looks like a browser
    "User-Agent": "Mozilla/5.0 (compatible; ao3-archiver/1.0)"
}

def get_epub_url(work_id, session):
    """
    Scrapes an AO3 work page to find the direct EPUB download URL.

    Args:
        work_id (str): The numeric AO3 work ID.
        session (requests.Session): A shared session object (with cookies already set).

    Returns:
        str | None: The full EPUB download URL, "RATE_LIMITED" on 429, or None if not found.
    """
    work_url = f"{BASE_URL}/works/{work_id}"

    try:
        response = session.get(work_url, headers=HEADERS)

        if response.status_code == 429:
            return "RATE_LIMITED"

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # Detect login wall because AO3 redirects locked works to a page with a login form
        if soup.find("form", {"id": "new_user"}):
            return "LOCKED"

        # AO3's download menu is a <li class="download"> containing per-format links
        download_section = soup.find("li", class_="download")
        if not download_section:
            return None

        for a_tag in download_section.find_all("a"):
            if a_tag.text.strip().upper() == "EPUB":
                href = a_tag.get("href")
                if href:
                    return BASE_URL + href

        return None

    except requests.RequestException as e:
        print(f"\n -> [Exception] Could not load work page for ID {work_id}: {e}")
        return None

def download_epub(work_id, session, folder_path=None, delay=5, output_dir="."):
    """
    Downloads an EPUB for a given AO3 work ID, saving it into the correct subfolder.

    Args:
        work_id (str): The numeric AO3 work ID.
        session (requests.Session): A shared session object (with cookies already set).
        folder_path (list[str] | None): Folder hierarchy from bookmarks, e.g. ["ASOIAF"].
                                        None or [] means save directly into output_dir.
        delay (int): Seconds to wait between requests.
        output_dir (str): Base directory to save files into.

    Returns:
        str: "success", "skipped", "locked", or "failed".
    """

    # --- [ 1. Resolve output subdirectory from folder_path ] ---
    if folder_path:
        save_dir = os.path.join(output_dir, *folder_path)
    else:
        save_dir = output_dir

    os.makedirs(save_dir, exist_ok=True)

    # --- [ 2. Skip if already downloaded ] ---
    # Check for any existing EPUB for this work ID to support resuming interrupted runs
    existing = [f for f in os.listdir(save_dir) if f.endswith(".epub") and work_id in f]
    if existing:
        return "skipped"

    # --- [ 3. Rate limiting ] ---
    time.sleep(delay)

    # --- [ 4. Scrape the real EPUB URL from the work page ] ---
    epub_url = get_epub_url(work_id, session)

    if epub_url == "LOCKED":
        print(f"\n -> [Locked] Work {work_id} requires an AO3 account — skipping.")
        return "locked"

    if epub_url == "RATE_LIMITED":
        print(f"\n -> [429] Rate limited scraping ID {work_id}. Pausing 5 minutes...")
        time.sleep(300)
        return "failed"

    if not epub_url:
        print(f"\n -> [Error] Could not find EPUB link for ID {work_id}.")
        return "failed"

    # --- [ 5. Fetch and save the EPUB ] ---
    time.sleep(delay)

    try:
        response = session.get(epub_url, headers=HEADERS)

        if response.status_code == 200:
            filename = epub_url.split("/")[-1].split("?")[0]
            filepath = os.path.join(save_dir, filename)

            with open(filepath, "wb") as f:
                f.write(response.content)
            return "success"

        elif response.status_code == 429:
            print(f"\n -> [429] Rate limited downloading ID {work_id}. Pausing 5 minutes...")
            time.sleep(300)
            return "failed"

        else:
            print(f"\n -> [Error {response.status_code}] Failed to download ID {work_id}.")
            return "failed"

    except requests.RequestException as e:
        print(f"\n -> [Exception] Connection error on ID {work_id}: {e}")
        return "failed"