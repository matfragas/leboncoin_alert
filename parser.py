import requests
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

def fetch_ads(url):
    options = uc.ChromeOptions()
    options.headless = True
    driver = uc.Chrome(options=options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    ads = []
    for card in soup.select('a[data-qa-id="aditem_container"]'):
        title = card.select_one('[data-qa-id="aditem_title"]').text.strip()
        price = card.select_one('[data-qa-id="aditem_price"]').text.strip()
        link = "https://www.leboncoin.fr" + card["href"]
        ads.append({
            "title": title,
            "price": price,
            "url": link
        })
    return ads
