import requests

SCRAPFLY_KEY = "scp-live-328b47fe39e0434887d3786c3a473bad"  # Remplace par ta clé

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
