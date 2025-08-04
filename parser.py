import requests
import json

def fetch_ads_mobile_api(category_id, location_code, price_min=0, price_max=999999, keywords=""):
    url = "https://api.leboncoin.fr/finder/search"

    headers = {
        "User-Agent": "LBC/2406231723 CFNetwork/1402.0.8 Darwin/22.2.0",  # user-agent iOS
        "Content-Type": "application/json",
        "X-LBC-Source": "search_page"
    }

    payload = {
        "filters": {
            "category": category_id,
            "locations": [{"zipcode": location_code}],
            "keywords": keywords,
            "price": {
                "min": price_min,
                "max": price_max
            }
        },
        "limit": 35,
        "sort_by": "time",
        "sort_order": "desc"
    }

    print(f"📡 Appel API mobile avec mots-clés '{keywords}' à {location_code}")

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        if response.status_code != 200:
            print(f"🔴 Statut HTTP {response.status_code} - {response.text}")
            return []

        data = response.json()
        ads = []

        for ad in data.get("ads", []):
            ads.append({
                "title": ad.get("subject", "Sans titre"),
                "price": f"{ad.get('price', 0)} €",
                "url": "https://www.leboncoin.fr" + ad.get("url", "")
            })

        print(f"✅ {len(ads)} annonces trouvées.")
        return ads

    except Exception as e:
        print(f"🔴 Erreur lors de l'appel API : {e}")
        return []
