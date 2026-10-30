import os
import json
import urllib.request
from datetime import datetime

# Deine verifizierte Webhook-URL für den Kanal #smyths-instore
DISCORD_WEBHOOK_URL = "https://discord.com"

def send_pure_text_pings():
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    for i in range(1, 3):
        now = datetime.now()
        timestamp_str = now.strftime("%d.%m.%Y um %H:%M Uhr")
        
        # Einfacher, reiner Text ohne Boxen oder Links, um Discord-Filter zu umgehen
        simple_text = f"🚨 TEST-PING {i}/2 ERFOLGREICH! Der Smyths Monitor steht und ist einsatzbereit. Zeit: {timestamp_str}"
        
        payload = json.dumps({
            "username": "TCGAlarm Test",
            "content": simple_text
        }).encode("utf-8")
        
        try:
            req = urllib.request.Request(DISCORD_WEBHOOK_URL, data=payload, headers=headers)
            with urllib.request.urlopen(req) as res:
                print(f"🔥 Reiner Text-Ping {i} erfolgreich gesendet!")
        except Exception as e:
            print(f"❌ Fehler bei Text-Ping {i}: {e}")

send_pure_text_pings()

