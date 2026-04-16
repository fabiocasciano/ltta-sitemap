import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://ltta.tecnopolo.fe.it"
OUTPUT_FILE = "sitemap-embed.html"

def get_all_links():
    to_visit = {BASE_URL, f"{BASE_URL}/italiano", f"{BASE_URL}/english"}
    visited = set()
    all_links = set()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print("Inizio scansione profonda... potrebbe volere un minuto.")

    while to_visit:
        current_url = to_visit.pop()
        if current_url in visited:
            continue
        
        print(f"Scansione in corso: {current_url}")
        try:
            response = requests.get(current_url, headers=headers, timeout=10)
            visited.add(current_url)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for a in soup.find_all('a', href=True):
                    link = a['href']
                    
                    # Normalizza il link
                    if link.startswith('/'):
                        link = f"{BASE_URL}{link}"
                    
                    # Se il link appartiene al sito e non è stato visitato, aggiungilo alla coda
                    if link.startswith(BASE_URL) and "#" not in link:
                        all_links.add(link)
                        if link not in visited:
                            to_visit.add(link)
            
            # Piccolo ritardo per non sovraccaricare il server
            time.sleep(0.1)
            
        except Exception as e:
            print(f"Errore su {current_url}: {e}")

    return sorted(all_links)

def save_to_html(links):
    html_content = """
    <style>
        .sitemap-container { font-family: sans-serif; line-height: 1.5; }
        .sitemap-list { list-style: none; padding-left: 20px; }
        .sitemap-item { margin: 3px 0; border-left: 1px solid #ccc; padding-left: 10px; }
        .sitemap-item a { text-decoration: none; color: #007bff; font-size: 13px; }
        .sitemap-item a:hover { text-decoration: underline; }
        .count { color: #666; font-size: 12px; margin-bottom: 10px; }
    </style>
    <div class="sitemap-container">
        <div class="count">Pagine rilevate: <strong>""" + str(len(links)) + """</strong></div>
        <ul class="sitemap-list">
    """
    for link in links:
        # Pulisce l'URL per visualizzarlo meglio
        label = link.replace(BASE_URL, "")
        if not label: label = "/"
        html_content += f'<li class="sitemap-item"><a href="{link}" target="_top">{label}</a></li>\n'
    
    html_content += "</ul></div>"
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    links = get_all_links()
    save_to_html(links)
    print(f"Finito! Trovati {len(links)} link.")
