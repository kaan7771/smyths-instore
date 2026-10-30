import os
import requests

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

print("⚡ Zünde den unblockbaren Profi-Restock im Code-Block-Design...")

prod_id = "231555"
prod_name = "One Piece TCG: Wings of the Captain Booster Display"
price = "119,99 €"
product_url = f"https://smythstoys.com{prod_id}"

store_name = "Hamburg-Altona"
stock_level = 3
full_address = "Sülldorfer Landstraße 42, 22589 Hamburg"
maps_url = f"https://google.com+{store_name}"

fancy_text = (
    f"╔════════════════════════════════════════════╗\n"
    f"  **🟠 SMYTHS TOYS INSTORE RESTOCK 🟠**\n"
    f"╚════════════════════════════════════════════╝\n\n"
    f"📝 **Produkt:** `{prod_name}`\n"
    f"💰 **Preis:** `{price}`\n\n"
    f"📍 **Filiale:** `{store_name}`\n"
    f"📦 **Bestand:** `{stock_level} Stück vor Ort! ✅`\n"
    f"🏠 **Adresse:** `{full_address}`\n\n"
    f"🔗 **Links:**\n"
    f"• [🛒 Zum Produkt-Shop]({product_url})\n"
    f"• [🗺️ Google Maps Navigation]({maps_url})\n\n"
    f"────────────────────────────────────────\n"
    f"*TCG Alerts • Live Pings • Smyths Monitor*"
)

payload = {
    "content": fancy_text
}

requests.post(DISCORD_WEBHOOK, json=payload)
print(f"🔥 Unblockbarer Premium-Alarm für {prod_name} erfolgreich gesendet!")
