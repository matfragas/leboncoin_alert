import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_ads(url):
    print(f"🌐 Ouverture de la page : {url}")
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)
    driver.get(url)

    try:
        # On attend que les cartes d'annonces apparaissent
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-qa-id="aditem_container"]'))
        )
        print("✅ Annonces détectées sur la page.")

    except Exception as e:
        print(f"🔴 Aucune annonce détectée après attente : {e}")
        driver.quit()
        return []

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    ads = []
    cards = soup.select('a[data-qa-id="aditem_container"]')
    print(f"🔎 {len(cards)} cartes détectées (annonces brutes)")

    for card in cards:
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
            print(f"🔴 Erreur lecture annonce : {e}")

    return ads
