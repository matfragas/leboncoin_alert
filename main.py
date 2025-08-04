import json
import os
import yaml
from parser import fetch_ads
from notifier import send_alert

SEEN_FILE = "data/seen_ads.json"

def load_seen_ads():
    if not os.path.exists(SEEN_FILE):
        return set()
    with open(SEEN_FILE, 'r') as f:
        return set(json.load(f))

def save_seen_ads(seen):
    with open(SEEN_FILE, 'w') as f:
        json.dump(list(seen), f)

def main():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    seen_ads = load_seen_ads()
    new_seen = seen_ads.copy()

    for search in config["searches"]:
        ads = fetch_ads(search["url"])
        for ad in ads:
            if ad["url"] not in seen_ads:
                send_alert(ad, search["name"])
                new_seen.add(ad["url"])

    save_seen_ads(new_seen)

if __name__ == "__main__":
    main()
