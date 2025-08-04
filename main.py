import os
import json
import yaml
from parser import fetch_ads_mobile_api
from notion_api import send_to_notion

SEEN_PATH = "data/seen_ads.json"

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
    
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    seen_ads = load_seen_ads()
    new_seen = seen_ads.copy()

    for search in config["searches"]:
        print(f"\n🔍 Recherche : {search['name']}")
        try:
            ads = fetch_ads_mobile_api(
                category_id=search["category_id"],
                location_code=search["zipcode"],
                price_min=search.get("price_min", 0),
                price_max=search.get("price_max", 999999),
                keywords=search.get("keywords", "")
            )
            print(f"➡️ {len(ads)} annonces trouvées")

            for ad in ads:
                if ad["url"] not in seen_ads:
                    print(f"🆕 Nouvelle annonce : {ad['title']} | {ad['price']}")
                    send_to_notion(ad, search["name"])
                    new_seen.add(ad["url"])
                else:
                    print(f"⏩ Déjà vue : {ad['title']}")
        except Exception as e:
            print(f"🔴 Erreur lors de la recherche : {e}")

    save_seen_ads(new_seen)
    print("🏁 Fin du script.\n")

if __name__ == "__main__":
    main()
