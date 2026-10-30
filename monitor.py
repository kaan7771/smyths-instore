import os
import requests

# HIER KANNST DU DEN LINK GEGEN JEDES ANDERE DEUTSCHE SMYTHS-PRODUKT TAUSCHEN:
PRODUCT_URL = "https://smythstoys.com"

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    response = requests.get(PRODUCT_URL, headers=headers, timeout=15)
    
    if "15+" in response.text or "In den Warenkorb" in response.text:
        # Hier bauen wir das strukturierte Embed (die Box unter dem Namen)
        payload = {
            "username": "TCG Alerts Monitor",  # Der Name ganz oben
            "avatar_url": "https://imgur.com",  # Optional: Ein Profilbild-Link für den Bot
            "embeds": [
                {
                    "title": "One Piece Kartenspiel The World's Strongest Warriors\nEnglische Version Booster Pack sortiert",
                    "description": "🟠 **Smyths Toys Instore Restock**",
                    "url": PRODUCT_URL,
                    "color": 16766720,  # Orange/Gelbe Farbe für den Seitenstreifen
                    "fields": [
                        {
                            "name": "Price",
                            "value": "4,99 €",
                            "inline": False
                        },
                        {
                            "name": "Store",
                            "value": "Deutschlandweit (Online/Filiale)",
                            "inline": True
                        },
                        {
                            "name": "Stock",
                            "value": "15+",
                            "inline": True
                        },
                        {
                            "name": "Links",
                            "value": f"[Product]({PRODUCT_URL})",
                            "inline": False
                        }
                    ],
                    "footer": {
                        "text": "TCG Alerts • Instant Restock Pings",
                        "icon_url": "https://imgur.com"
                    }
                }
            ]
        }
        
        requests.post(DISCORD_WEBHOOK, json=payload)
        print("Erfolgreich! Die formatierte Box wurde an Discord gesendet.")
    else:
        print("Überprüfung durchgeführt: Aktuell kein Bestand vorrätig.")
        
except Exception as e:
    print(f"Fehler beim Abrufen der Webseite: {e}")
