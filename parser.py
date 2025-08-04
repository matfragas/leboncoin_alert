import requests
from bs4 import BeautifulSoup
import os

SCRAPFLY_KEY = os.getenv("SCRAPFLY_API_KEY")

if not SCRAPFLY_KEY:
    print("🔴 Clé API Scrapfly manquante dans l'environnement !")
    return []
else:
    print(f"🔑 Clé Scrapfly détectée (masquée): {SCRAPFLY_KEY[:6]}...***")

def fetch_ads(url):
    print(f"🔍 Scrapfly scraping : {url}")

    api_url = "https://api.scrapfly.io/scrape"
    params = {
        "url": url,
        "render_js": "true",  # ATTENTION : doit être "true" en string
        "wait_for_selector": 'a[data-qa-id="aditem_container"]'
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": SCRAPFLY_KEY
    }

    try:
        response = requests.get(api_url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"🔴 Erreur Scrapfly : {response.status_code} - {response.text}")
            return []

        html = response.json()["result"]["content"]
        soup = BeautifulSoup(html, "html.parser")
        ads = []

        for card in soup.select('a[data-qa-id="aditem_container"]'):
            try:
                title = card.select_one('[data-qa-id="aditem_title"]').text.strip()
                price = card.select_one('[data-qa-id="aditem_price"]').text.strip()
                link = "https://www.leboncoin.fr" + card["href"]
                ads.append({
                    "title": title,
                    "price": price,
                    "url": link
                })
            except Exception as e:
                print(f"🔴 Erreur parsing : {e}")

        print(f"✅ {len(ads)} annonces extraites")
        return ads

    except Exception as e:
        print(f"🔴 Erreur Scrapfly API : {e}")
        return []
