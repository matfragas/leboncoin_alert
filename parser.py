import requests

def fetch_ads_mobile_api(category_id=19, location_code="53000", price_min=0, price_max=10000, keywords="armoire"):
    url = "https://api.leboncoin.fr/finder/search"
    params = {
        "filters": {
            "category": category_id,
            "locations": [{"zipcode": location_code}],
            "price": {"min": price_min, "max": price_max},
            "keywords": keywords
        },
        "limit": 30,
        "limit_alu": 3,
        "owner_type": "all",
        "sort_by": "time",
        "sort_order": "desc"
    }

    headers = {
        "User-Agent": "LBC/1.0 (Android)",
        "Content-Type": "application/json"
    }

    try:
        print(f"📡 Appel API mobile pour '{keywords}' à {location_code}")
        res = requests.post(url, json=params, headers=headers)

        if res.status_code != 200:
            print(f"🔴 Statut HTTP {res.status_code}")
            return []

        data = res.json()
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
        print(f"🔴 Erreur API : {e}")
        return []
