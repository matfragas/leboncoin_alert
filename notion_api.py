from notion_client import Client
import os

notion = Client(auth=os.environ["NOTION_TOKEN"])
DATABASE_ID = os.environ["NOTION_DATABASE_ID"]

def send_to_notion(ad, category):
    notion.pages.create(parent={"database_id": DATABASE_ID}, properties={
        "Nom": {"title": [{"text": {"content": ad["title"]}}]},
        "Prix": {"rich_text": [{"text": {"content": ad["price"]}}]},
        "Lien": {"url": ad["url"]},
        "Catégorie": {"select": {"name": category}}
    })
