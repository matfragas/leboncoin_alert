import requests

def fetch_ads(url):
    print(f"🌐 Récupération JSON depuis : {url}")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        # Transforme une URL classique en URL API JSON
        if "/recherche/" in url:
            url = url.replace("www.leboncoin.fr/recherche", "api.leboncoin.fr/finder/search")
            url = url.replace("?", "?limit=35&")  # limite à 35 résultats max (peut augmenter)

        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print(f"🔴 Statut HTTP {res.status_code} pour l'URL {url}")
            return []

        data = res.json()
        if "ads" not in data:
            print("🔴 Réponse JSON invalide ou pas d’annonces")
            return []

        ads = []
        for ad in data["ads"]:
            try:
                ads.append({
                    "title": ad.get("subject", "Sans titre"),
                    "price": f"{ad.get('price', 0)} €",
                    "url": "https://www.leboncoin.fr" + ad.get("url", "")
                })
            except Exception as e:
                print(f"🔴 Erreur parsing annonce JSON : {e}")

        print(f"✅ {len(ads)} annonces trouvées.")
        return ads

    except Exception as e:
        print(f"🔴 Exception lors de l'appel API : {e}")
        return []
