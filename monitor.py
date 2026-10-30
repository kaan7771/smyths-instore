import os
import requests
from datetime import datetime

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

print("⚡ Sende bereinigtes Embed ohne überflüssige Icons...")

prod_id = "231555"
prod_name = "One Piece TCG: Wings of the Captain Booster Display"
price = "119,99 €"
product_url = f"https://smythstoys.com{prod_id}"

store_name = "Hamburg-Altona"
stock_level = 3
full_address = "Sülldorfer Landstraße 42, 22589 Hamburg"
maps_url = f"https://google.com+{store_name}"

# Aktuelle Uhrzeit ermitteln
now = datetime.now()
timestamp_str = now.strftime("%d.%m.%Y um %H:%M Uhr")

embed = {
    "title": "SMYTHS TOYS INSTORE RESTOCK",
    "description": (
        f"📝 **Product:** {prod_name}\n"
        f"💰 **Price:** {price}\n\n"
        f"📍 **Store:** {store_name}\n"
        f"📦 **Stock:** {stock_level} Stück ✅\n"
        f"🏠 **Address:** {full_address}\n\n"
        f"🔗 **Links:**\n"
        f"• [Product]({product_url})\n"
        f"• [Google Maps Navigation]({maps_url})"
    ),
    "color": 16746496,  # Orange farbener Akzentbalken
    "footer": {
        "text": f"TCGAlarm • Live Pings • Smyths Monitor • heute um {timestamp_str}"
    }
}

payload = {
    "username": "TCGAlarm",
    "embeds": [embed]
}

requests.post(DISCORD_WEBHOOK, json=payload)
print(f"🔥 Bereinigter Alarm erfolgreich gesendet!")

