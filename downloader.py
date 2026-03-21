"""
Module: downloader
Handles the fetching and saving of EPUB files from AO3.
"""

# === [ IMPORTS ] ===
import time
import requests

def download_epub(work_id, delay=5):
    """
    Downloads an EPUB file for a given AO3 Work ID.
    
    Args:
        work_id (str): The numeric ID of the AO3 work.
        delay (int): Seconds to wait before downloading to avoid rate limits.
        
    Returns:
        bool: True if download was successful, False otherwise.
    """
    # --- [ 1. Rate Limiting ] ---
    # AO3 blocks IPs that send too many requests too quickly
    time.sleep(delay)
    
    # --- [ 2. Construct Download URL ] ---
    # The AO3 download endpoint requires the ID and a filename ending in .epub
    url = f"https://archiveofourown.org/downloads/{work_id}/fic_{work_id}.epub"
    
    # --- [ 3. Fetch and Save ] ---
    try:
        response = requests.get(url, allow_redirects=True)
        
        # Check if the server responded with a success code (HTTP 200)
        if response.status_code == 200:
            filename = f"fic_{work_id}.epub"
            with open(filename, 'wb') as file:
                file.write(response.content)
            return True
            
        # Handle the specific "Too Many Requests" error (HTTP 429)
        elif response.status_code == 429:
            print(f" -> [Error 429] Rate limited on ID {work_id}. Pausing is required.")
            return False
            
        # Handle any other HTTP errors (like 404 Not Found)
        else:
            print(f" ->[Error {response.status_code}] Failed to download ID {work_id}.")
            return False
            
    except requests.RequestException as e:
        print(f" -> [Exception] Connection error on ID {work_id}: {e}")
        return False