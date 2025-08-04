import requests
from bs4 import BeautifulSoup
import os

SCRAPFLY_KEY = os.getenv("SCRAPFLY_API_KEY")

def fetch_ads(url):
    print(f"🔍 Scrapfly scraping : {url}")

    api_url = "https://api.scrapfly.io/scrape"
    params = {
        "key": SCRAPFLY_KEY,
        "url": url,
        "render_js": True,
        "wait_for_selector": 'a[data-qa-id="aditem_container"]'
    }

    try:
        response = requests.get(api_url, params=params)
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
