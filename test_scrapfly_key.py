import requests
import os

SCRAPFLY_KEY = os.getenv("SCRAPFLY_API_KEY") or "live_xxxxx"  # remplace ici si besoin

def test_scrapfly_key():
    print("🔍 Test de la clé Scrapfly...")

    url = "https://api.scrapfly.io/scrape"
    headers = {
        "X-API-KEY": SCRAPFLY_KEY
    }
    params = {
        "url": "https://httpbin.dev/anything",
        "render_js": "true",
        "asp": "true"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        print("✅ Clé Scrapfly valide et fonctionnelle !")
    else:
        print(f"❌ Erreur : HTTP {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_scrapfly_key()
