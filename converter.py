import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://ltta.tecnopolo.fe.it"
XML_FILE = "sitemap.xml"

def get_all_links():
    to_visit = {BASE_URL, f"{BASE_URL}/italiano", f"{BASE_URL}/english"}
    visited = set()
    all_links = set()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    print("Scansione in corso per creazione file XML...")

    while to_visit:
        current_url = to_visit.pop()
        if current_url in visited:
            continue
        
        try:
            response = requests.get(current_url, headers=headers, timeout=10)
            visited.add(current_url)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for a in soup.find_all('a', href=True):
                    link = a['href']
                    if link.startswith('/'):
                        link = f"{BASE_URL}{link}"
                    
                    if link.startswith(BASE_URL) and "#" not in link:
                        all_links.add(link)
                        if link not in visited:
                            to_visit.add(link)
            time.sleep(0.1) # Rispetto per il server
            
        except Exception as e:
            print(f"Errore su {current_url}: {e}")

    return sorted(all_links)

def save_xml(links):
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for link in links:
        xml_content += f'  <url>\n    <loc>{link}</loc>\n  </url>\n'
    
    xml_content += '</urlset>'
    
    with open(XML_FILE, "w", encoding="utf-8") as f:
        f.write(xml_content)
    print(f"Successo! Creato {XML_FILE} con {len(links)} URL.")

if __name__ == "__main__":
    links = get_all_links()
    save_xml(links)
