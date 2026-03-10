from bs4 import BeautifulSoup

def extract_ao3_links():
    # Hardcoded filename for now!
    filename = 'bookmarks.html'
    
    # 1. Open and read the HTML file
    # 2. Parse the HTML
    # 3. Find all links
    # 4. Filter for only AO3 work links
    with open(filename, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    all_links = soup.find_all('a')
    ao3_links =[]
    
    for link in all_links:
        url = link.get('href')
        if url and 'archiveofourown.org/works/' in url:
            ao3_links.append(url)
            
    return ao3_links

if __name__ == '__main__':
    links = extract_ao3_links()
    print(f"Found {len(links)} AO3 fics!")
    
    # Print the first 3 to verify it works
    for link in links[:3]:
        print(link)