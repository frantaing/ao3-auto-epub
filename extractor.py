"""
Module: extractor
Handles parsing HTML bookmark files and extracting AO3 work data.
"""

# --- [ Imports ] ---
import os
import re
from bs4 import BeautifulSoup

def extract_ao3_links(file_path):
    """
    Reads an HTML bookmark file, extracts AO3 Work IDs, and deduplicates them.
    
    Args:
        file_path (str): The path to the bookmarks.html file.
        
    Returns:
        dict: A dictionary mapping Work IDs to their clean base URLs.
              Format: {'12345': 'https://archiveofourown.org/works/12345'}
    """
    
    # ---[ 1. File validation & loading ] ---
    # Make sure the file exists before attempting to load it into memory.
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found.")
        
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # --- [ 2. HTML parsing ] ---
    soup = BeautifulSoup(html_content, 'html.parser')
    all_links = soup.find_all('a')
    
    # --- [ 3. Extraction & deduplication ] ---
    # Use a dictionary where the key is the Work ID to auto-overwrite duplicate IDs
    unique_fics = {}
    
    for link in all_links:
        url = link.get('href')
        
        # Verify it's an AO3 work link, then extract the numeric ID
        if url and 'archiveofourown.org/works/' in url:
            match = re.search(r'/works/(\d+)', url)
            
            if match:
                work_id = match.group(1)
                clean_url = f"https://archiveofourown.org/works/{work_id}"
                unique_fics[work_id] = clean_url
                
    return unique_fics