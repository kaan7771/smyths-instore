import os
import requests

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

print("⚡ Starte künstlichen Ultra-Express-Testlauf (Reiner Text)...")

prod_id = "231555"
prod_name = "One Piece TCG: Wings of the Captain Booster Display"
price = "119,99 €"
product_url = f"https://smythstoys.com{prod_id}"

# Künstliche Filialdaten für Hamburg
store_name = "Hamburg-Altona"
stock_level = 3
full_address = "Sülldorfer Landstraße 42, 22589 Hamburg"
maps_url = f"https://google.com+{store_name}"

# Die unfehlbare, reine Text-Nachricht
text_payload = {
    "content": f"🟠 **Smyths Toys Instore Restock!** 🟠\n\n**Produkt:** {prod_name}\n**Preis:** {price}\n**Filiale:** {store_name}\n**Bestand:** {stock_level} Stück vor Ort!\n**Adresse:** {full_address}\n\nShop-Link: {product_url}\nGoogle Maps: {maps_url}"
}

requests.post(DISCORD_WEBHOOK, json=text_payload)
print(f"🔥 Künstlicher Text-Alarm für {prod_name} erfolgreich an Discord gesendet!")

