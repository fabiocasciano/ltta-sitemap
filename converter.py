import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://ltta.tecnopolo.fe.it"
XML_FILE = "sitemap.xml"
HTML_FILE = "sitemap.html"

def get_all_links():
    to_visit = {BASE_URL, f"{BASE_URL}/italiano", f"{BASE_URL}/english"}
    visited = set()
    all_links = set()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    print("Scansione in corso per creazione file sitemap...")

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
            time.sleep(0.1) 
            
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
    print(f"Creato {XML_FILE}.")

def save_html(links):
    # Generazione dei singoli elementi della lista
    li_elements = ""
    for link in links:
        # Mostriamo il percorso relativo per pulizia visiva
        relative_path = link.replace(BASE_URL, "")
        if not relative_path: relative_path = "/"
        li_elements += f'        <li class="sitemap-item"><a href="{link}" target="_top">{relative_path}</a></li>\n'

    html_content = f"""<style>
        .sitemap-container {{ font-family: sans-serif; line-height: 1.5; }}
        .sitemap-list {{ list-style: none; padding-left: 20px; }}
        .sitemap-item {{ margin: 3px 0; border-left: 1px solid #ccc; padding-left: 10px; }}
        .sitemap-item a {{ text-decoration: none; color: #007bff; font-size: 13px; }}
        .sitemap-item a:hover {{ text-decoration: underline; }}
        .count {{ color: #666; font-size: 12px; margin-bottom: 10px; }}
    </style>
    <div class="sitemap-container">
        <div class="count">Pagine rilevate: <strong>{len(links)}</strong></div>
        <ul class="sitemap-list">
{li_elements}        </ul>
    </div>"""

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Creato {HTML_FILE}.")

if __name__ == "__main__":
    links = get_all_links()
    save_xml(links)
    save_html(links)
