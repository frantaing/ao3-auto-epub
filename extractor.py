# desc. here....

# === [ IMPORTS ] ===
import os
from bs4 import BeautifulSoup

def extract_ao3_links(file_path):
    # Check if the file exists before trying to read it
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found.")
        
    # Open and read the HTML file
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    all_links = soup.find_all('a')
    
    ao3_links =[]
    for link in all_links:
        url = link.get('href')
        if url and 'archiveofourown.org/works/' in url:
            ao3_links.append(url)
            
    return ao3_links