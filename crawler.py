import urllib.request
import re
import json

# L'URL de ton Webhook Google Apps Script (À REMPLACER)
WEBHOOK_URL = "https://script.google.com/macros/s/AKfy.../exec"

def extract_urls_from_page(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
        # Trouve tous les liens http/https dans le code source
        links = re.findall(r'href=[\'"]?(https?://[^\'" >]+)', html)
        return links
    except Exception as e:
        print(f"Erreur lors de la lecture de {url}: {e}")
        return []

def main():
    nouveaux_sites = set()
    
    # 1. Lire les terrains de chasse depuis le fichier texte
    try:
        with open("sources.txt", "r") as f:
            sources = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Le fichier sources.txt n'existe pas.")
        return

    # 2. Chasser sur chaque source
    for source in sources:
        print(f"Analyse de la source : {source}")
        liens_trouves = extract_urls_from_page(source)
        for lien in liens_trouves:
            nouveaux_sites.add(lien)
            
    # 3. Envoyer la récolte à Google Apps Script
    if nouveaux_sites:
        payload = json.dumps({"urls": list(nouveaux_sites)}).encode('utf-8')
        req = urllib.request.Request(WEBHOOK_URL, data=payload, headers={'Content-Type': 'application/json'})
        try:
            urllib.request.urlopen(req)
            print(f"Succès : {len(nouveaux_sites)} liens envoyés au Webhook.")
        except Exception as e:
            print(f"Erreur d'envoi au Webhook : {e}")
    else:
        print("Aucun lien trouvé.")

if __name__ == "__main__":
    main()
