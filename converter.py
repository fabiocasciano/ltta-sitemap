import requests
from bs4 import BeautifulSoup # Questa libreria serve a leggere l'HTML

BASE_URL = "https://ltta.tecnopolo.fe.it"
OUTPUT_FILE = "sitemap-embed.html"

def scrape_sitemap():
    print(f"Inizio scansione del sito: {BASE_URL}")
    try:
        response = requests.get(BASE_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Trova tutti i link (tag <a>) che iniziano con l'indirizzo del tuo sito
        links = set() # Usiamo un set per evitare duplicati
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('/') or BASE_URL in href:
                # Trasforma i link relativi (/chi-siamo) in assoluti
                full_url = href if href.startswith('http') else f"{BASE_URL}{href}"
                links.add(full_url)

        if not links:
            print("Non ho trovato link! Forse Google Sites blocca la lettura diretta.")
            return

        print(f"Ho trovato {len(links)} link. Genero il file...")

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("<html><body style='font-family:sans-serif;'><ul>")
            for l in sorted(links):
                f.write(f"<li><a href='{l}' target='_top'>{l}</a></li>")
            f.write("</ul></body></html>")
            
    except Exception as e:
        print(f"Errore durante lo scraping: {e}")

if __name__ == "__main__":
    scrape_sitemap()
