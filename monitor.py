import os
import json
import urllib.request
from datetime import datetime

# Deine verifizierte Webhook-URL für den Kanal #smyths-instore
DISCORD_WEBHOOK_URL = "https://discord.com"

def send_instant_webhook_pings():
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    # Sendet sofort 2 Nachrichten hintereinander ohne Smyths-Abfrage
    for i in range(1, 3):
        now = datetime.now()
        timestamp_str = now.strftime("%d.%m.%Y um %H:%M Uhr")
        
        fancy_text = (
            f"╔════════════════════════════════════════════╗\n"
            f"        **⚙️ ERZWUNGENER WEBHOOK-PING {i}/2 ⚙️**\n"
            f"╚════════════════════════════════════════════╝\n\n"
            f"📝 **Product:** `Direkter Webhook-Verbindungstest`\n"
            f"📦 **Status:** `Erfolgreich durchgekommen ✅`\n\n"
            f"────────────────────────────────────────\n"
            f"*Verbindung steht! • {timestamp_str}*"
        )
        
        payload = json.dumps({
            "username": "TCGAlarm Monitor",
            "content": fancy_text
        }).encode("utf-8")
        
        try:
            req = urllib.request.Request(DISCORD_WEBHOOK_URL, data=payload, headers=headers)
            with urllib.request.urlopen(req) as res:
                print(f"🔥 Webhook-Ping {i} erfolgreich gesendet!")
        except Exception as e:
            print(f"❌ Kritischer Webhook-Fehler bei Ping {i}: {e}")

send_instant_webhook_pings()
