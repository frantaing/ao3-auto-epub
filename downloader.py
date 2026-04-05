"""
Module: downloader
Handles the fetching and saving of EPUB files from AO3.
"""

# --- [ Imports ] ---
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
        session (requests.Session): A shared session object.

    Returns:
        str | None: The full EPUB download URL, or None if not found.
    """
    work_url = f"{BASE_URL}/works/{work_id}"

    try:
        response = session.get(work_url, headers=HEADERS)

        if response.status_code == 429:
            return "RATE_LIMITED"

        if response.status_code != 200:
            return None

        # DEBUG: save the raw HTML to see what AO3 actually returned
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(response.text)

        soup = BeautifulSoup(response.text, "html.parser")

        # AO3's download menu has a <li class="download"> containing format links
        download_section = soup.find("li", class_="download")
        if not download_section:
            return None

        for a_tag in download_section.find_all("a"):
            if a_tag.text.strip().upper() == "EPUB":
                href = a_tag.get("href")
                if href:
                    # href is relative, e.g. /downloads/12345/Title.epub?updated_at=...
                    return BASE_URL + href

        return None

    except requests.RequestException as e:
        print(f"\n -> [Exception] Could not load work page for ID {work_id}: {e}")
        return None


def download_epub(work_id, session, delay=5, output_dir="."):
    """
    Downloads an EPUB file for a given AO3 Work ID.

    Args:
        work_id (str): The numeric ID of the AO3 work.
        session (requests.Session): A shared session object.
        delay (int): Seconds to wait before each request.
        output_dir (str): Directory to save the downloaded file.

    Returns:
        bool: True if download was successful, False otherwise.
    """
    # --- [ 1. Rate limiting ] ---
    time.sleep(delay)

    # --- [ 2. Scrape the actual EPUB URL ] ---
    epub_url = get_epub_url(work_id, session)

    if epub_url == "RATE_LIMITED":
        print(f"\n -> [429] Rate limited scraping ID {work_id}. Pausing 5 minutes...")
        time.sleep(300)
        return False

    if not epub_url:
        print(f"\n -> [Error] Could not find EPUB link for ID {work_id}.")
        return False

    # --- [ 3. Fetch the EPUB ] ---
    time.sleep(delay)  # second polite pause before the actual download

    try:
        response = session.get(epub_url, headers=HEADERS)

        if response.status_code == 200:
            # Derive filename from the URL path
            filename = epub_url.split("/")[-1].split("?")[0]  # strips query params
            filepath = f"{output_dir}/{filename}"

            with open(filepath, "wb") as f:
                f.write(response.content)
            return True

        elif response.status_code == 429:
            print(f"\n -> [429] Rate limited downloading ID {work_id}. Pausing 5 minutes...")
            time.sleep(300)
            return False

        else:
            print(f"\n -> [Error {response.status_code}] Failed to download ID {work_id}.")
            return False

    except requests.RequestException as e:
        print(f"\n -> [Exception] Connection error on ID {work_id}: {e}")
        return False