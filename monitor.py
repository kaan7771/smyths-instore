import os
import requests

# Link zum Smyths-Toys-Produkt
PRODUCT_URL = "https://smythstoys.com"

# Holt deine geheime Webhook-URL
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    response = requests.get(PRODUCT_URL, headers=headers, timeout=15)
    
    # TEST-MODUS: Wir prüfen absichtlich auf das Wort "Spielzeug", um den Ping zu erzwingen!
    if "Smyths" in response.text:
        payload = {
            "content": f"🚨 **TEST-ALARM: DER MONITOR FUNKTIONIERT!** 🚨\n\nDas Produkt wurde auf Smyths Toys gescannt.\nLink: {PRODUCT_URL}"
        }
        
        # Schickt die Nachricht ab und prüft direkt den Status
        res = requests.post(DISCORD_WEBHOOK, json=payload)
        
        if res.status_code == 204:
            print("Erfolgreich gesendet! Status 204.")
        else:
            print(f"Discord hat die Nachricht abgelehnt. Fehlercode: {res.status_code}")
    else:
        print("Wort nicht gefunden.")
        
except Exception as e:
    print(f"Fehler: {e}")

