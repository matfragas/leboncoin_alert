import os
import json
import yaml
from parser import fetch_ads
from notion_api import send_to_notion
import requests

SEEN_PATH = "data/seen_ads.json"

def test_scrapfly_key():
    key = os.getenv("SCRAPFLY_API_KEY")
    if not key:
        print("❌ Clé API Scrapfly manquante dans l'environnement (SCRAPFLY_API_KEY).")
        return False

    print(f"🔑 Clé Scrapfly détectée (début) : {key[:6]}...")

    try:
        test_url = "https://www.duckduckgo.com"
        api_url = "https://api.scrapfly.io/scrape"
        headers = {"X-API-KEY": key}
        params = {
            "url": test_url,
            "render_js": "false"
        }

        response = requests.get(api_url, headers=headers, params=params)

        if response.status_code == 200:
            print("✅ Clé API Scrapfly valide !")
            return True
        else:
            print(f"❌ Scrapfly a rejeté la clé : HTTP {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test Scrapfly : {e}")
        return False

def load_seen_ads():
    if not os.path.exists(SEEN_PATH):
        print("🟡 Aucun fichier seen_ads.json, initialisation…")
        return set()
    try:
        with open(SEEN_PATH, 'r') as f:
            content = f.read().strip()
            if not content:
                print("🟡 Fichier seen_ads.json vide.")
                return set()
            return set(json.loads(content))
    except Exception as e:
        print(f"🔴 Erreur lecture seen_ads.json : {e}")
        return set()

def save_seen_ads(seen):
    try:
        with open(SEEN_PATH, 'w') as f:
            json.dump(list(seen), f)
        print("✅ Annonces vues enregistrées.")
    except Exception as e:
        print(f"🔴 Erreur sauvegarde seen_ads.json : {e}")

def main():
    print("🚀 Démarrage du script LeBonCoin → Notion")

    if not test_scrapfly_key():
    print("🛑 Arrêt du script : clé Scrapfly invalide.")
    return

    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    seen_ads = load_seen_ads()
    new_seen = seen_ads.copy()

    for search in config["searches"]:
        print(f"\n🔍 Recherche : {search['name']}")
        try:
            ads = fetch_ads(search["url"])
            print(f"➡️ {len(ads)} annonces trouvées")

            for ad in ads:
                if ad["url"] not in seen_ads:
                    print(f"🆕 Nouvelle annonce : {ad['title']} | {ad['price']}")
                    send_to_notion(ad, search["name"])
                    new_seen.add(ad["url"])
                else:
                    print(f"⏩ Déjà vue : {ad['title']}")
        except Exception as e:
            print(f"🔴 Erreur dans la recherche : {e}")

    save_seen_ads(new_seen)
    print("🏁 Fin du script.\n")

if __name__ == "__main__":
    main()
