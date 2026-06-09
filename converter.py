import requests
from bs4 import BeautifulSoup
import time

# Configurazione iniziale
BASE_URL = "https://ltta.tecnopolo.fe.it"
XML_FILE = "sitemap.xml"
HTML_FILE = "sitemap.html"

def get_all_links():
    # Inizializzazione dei set per la scansione
    to_visit = {BASE_URL, f"{BASE_URL}/italiano", f"{BASE_URL}/english"}
    visited = set()
    all_links = set()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

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
    print(f"Creato {XML_FILE} con successo.")

def save_html(links):
    # Generazione dei singoli elementi della lista HTML
    li_elements = ""
    for link in links:
        # Mostriamo il percorso relativo per pulizia visiva
        relative_path = link.replace(BASE_URL, "")
        if not relative_path: 
            relative_path = "/"
            
        # Nota: target="_blank" garantisce la cliccabilità su Google Sites
        li_elements += f'      <li class="sitemap-item"><a href="{link}" target="_blank">{relative_path}</a></li>\n'
        
    # Costruzione della pagina HTML finale usando le tue classi CSS
    html_content = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<style>
  body {{ font-family: sans-serif; margin: 0; padding: 10px; background-color: #ffffff; }}
  .sitemap-container {{ font-family: sans-serif; line-height: 1.5; }}
  .sitemap-list {{ list-style: none; padding-left: 20px; margin: 0; }}
  .sitemap-item {{ margin: 3px 0; border-left: 1px solid #ccc; padding-left: 10px; }}
  .sitemap-item a {{ text-decoration: none; color: #007bff; font-size: 13px; }}
  .sitemap-item a:hover {{ text-decoration: underline; }}
  .count {{ color: #666; font-size: 12px; margin-bottom: 10px; }}
</style>
</head>
<body>

<div class="sitemap-container">
  <div class="count">Pagine rilevate: <strong>{len(links)}</strong></div>
  <ul class="sitemap-list">
{li_elements}  </ul>
</div>

</body>
</html>"""

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Creato {HTML_FILE} con successo.")

if __name__ == "__main__":
    # Esegue la scansione una volta sola e genera entrambi i file
    links = get_all_links()
    save_xml(links)
    save_html(links)
