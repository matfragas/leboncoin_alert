from notion_client import Client
import os

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

if not NOTION_TOKEN or not DATABASE_ID:
    print("🔴 Variables d'environnement manquantes : NOTION_TOKEN ou DATABASE_ID")

notion = Client(auth=NOTION_TOKEN)

def send_to_notion(ad, category):
    try:
        print(f"📤 Envoi vers Notion : {ad['title']}")
        notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties={
                "Nom": {"title": [{"text": {"content": ad["title"]}}]},
                "Prix": {"rich_text": [{"text": {"content": ad["price"]}}]},
                "Lien": {"url": ad["url"]},
                "Catégorie": {"select": {"name": category}},
            }
        )
        print("✅ Annonce ajoutée dans Notion.")
    except Exception as e:
        print(f"🔴 Erreur lors de l’envoi à Notion : {e}")
