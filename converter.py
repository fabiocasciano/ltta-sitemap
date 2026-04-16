import requests
import xml.etree.ElementTree as ET
import os

# URL esatto della sitemap
XML_URL = "https://ltta.tecnopolo.fe.it/sitemap.xml"
OUTPUT_FILE = "sitemap-embed.html"

def generate_html():
    print(f"Inizio il download della sitemap da: {XML_URL}")
    try:
        response = requests.get(XML_URL, timeout=10)
        response.raise_for_status() # Verifica se il sito risponde (200 OK)
        
        root = ET.fromstring(response.content)
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        urls = [u.find('sm:loc', ns).text for u in root.findall('sm:url', ns)]
        
        if not urls:
            print("Errore: Nessun link trovato nell'XML!")
            return

        print(f"Trovati {len(urls)} link. Genero l'HTML...")

        html_content = "<div style='font-family:sans-serif;'><ul>"
        for url in urls:
            html_content += f"<li><a href='{url}' target='_top'>{url}</a></li>"
        html_content += "</ul></div>"

        # Scrittura del file
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        # Verifica finale se il file esiste davvero
        if os.path.exists(OUTPUT_FILE):
            print(f"Successo! File {OUTPUT_FILE} creato correttamente.")
        else:
            print("Errore: Il file non è stato scritto su disco.")

    except Exception as e:
        print(f"ERRORE DURANTE L'ESECUZIONE: {e}")

if __name__ == "__main__":
    generate_html()
