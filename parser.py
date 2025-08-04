import undetected_chromedriver as uc
from bs4 import BeautifulSoup

def fetch_ads(url):
    print(f"🌐 Chargement de la page : {url}")
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    driver = uc.Chrome(options=options)

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    ads = []
    for card in soup.select('a[data-qa-id="aditem_container"]'):
        try:
            title = card.select_one('[data-qa-id="aditem_title"]').text.strip()
            price = card.select_one('[data-qa-id="aditem_price"]').text.strip()
            link = "https://www.leboncoin.fr" + card["href"]
            ads.append({
                "title": title,
                "price": price,
                "url": link
            })
        except Exception as e:
            print(f"🔴 Erreur parsing d'une annonce : {e}")
    return ads
