import requests

SCRAPFLY_KEY = "scp-live-69f48ed54ff0440398714a7095f09269"  # Remplace par ta clé

url = "https://api.scrapfly.io/scrape"
params = {
    "url": "https://httpbin.dev/anything",
    "render_js": "true",
    "asp": "true"
}
headers = {
    "X-API-KEY": SCRAPFLY_KEY
}

response = requests.get(url, headers=headers, params=params)

print(f"Status: {response.status_code}")
print(response.text)
