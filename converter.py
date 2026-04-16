import requests
import xml.etree.ElementTree as ET

XML_URL = "https://ltta.tecnopolo.fe.it/sitemap.xml"
OUTPUT_FILE = "sitemap-embed.html"

def generate_html():
    try:
        response = requests.get(XML_URL)
        root = ET.fromstring(response.content)
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        urls = [u.find('sm:loc', ns).text for u in root.findall('sm:url', ns)]
        urls.sort() # Ordina alfabeticamente per raggruppare italiano ed english

        html_content = """
        <style>
            .sitemap-body { font-family: sans-serif; font-size: 14px; line-height: 1.6; color: #333; }
            .sitemap-body ul { list-style: none; padding-left: 20px; }
            .sitemap-body li { margin: 4px 0; position: relative; }
            .sitemap-body li::before { content: "└─"; position: absolute; left: -18px; color: #bbb; }
            .sitemap-body a { text-decoration: none; color: #007bff; }
            .sitemap-body a:hover { text-decoration: underline; }
            .lang-header { font-weight: bold; color: #0056b3; margin-top: 15px; display: block; }
        </style>
        <div class="sitemap-body">
            <ul>
        """

        for url in urls:
            # Rendi i link un po' più leggibili rimuovendo il dominio se preferisci, 
            # o lasciali interi per sicurezza:
            label = url.replace("https://ltta.tecnopolo.fe.it/", "/")
            html_content += f"<li><a href='{url}' target='_top'>{label}</a></li>\n"

        html_content += "</ul></div>"

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(html_content)
            
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    generate_html()
