import os
import requests

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

print("⚡ Zünde den künstlichen Profi-Restock ohne Profil-Überschreibung...")

prod_id = "231555"
prod_name = "One Piece TCG: Wings of the Captain Booster Display"
price = "119,99 €"

# Ein absolut sicheres Cloud-Bild
image_url = "https://imgur.com"
product_url = f"https://smythstoys.com{prod_id}"

store_name = "Hamburg-Altona"
stock_level = 3
full_address = "Sülldorfer Landstraße 42, 22589 Hamburg"
maps_url = f"https://google.com+{store_name}"

# Payloads OHNE username und avatar_url -> Das umgeht die Discord-Sperre!
payload = {
    "embeds": [{
        "author": {
            "name": "Smyths Toys Instore Restock",
            "icon_url": "https://imgur.com"
        },
        "title": prod_name,
        "url": product_url,
        "color": 16766720,
        "thumbnail": {"url": image_url},
        "fields": [
            {"name": "Price", "value": price, "inline": False},
            {"name": "Store", "value": store_name, "inline": True},
            {"name": "Stock", "value": f"{stock_level}", "inline": True},
            {"name": "Address", "value": full_address, "inline": False},
            {"name": "Links", "value": f"[Google Maps]({maps_url}) · [Product]({product_url})", "inline": False}
        ],
        "footer": {
            "text": "TCG Alerts • Live Pings",
            "icon_url": "https://imgur.com"
        }
    }]
}

requests.post(DISCORD_WEBHOOK, json=payload)
print(f"🔥 Premium-Alarm für {prod_name} erfolgreich gesendet!")
