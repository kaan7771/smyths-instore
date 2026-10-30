import os
import json
import urllib.request
from datetime import datetime

# Holt das sichere Bot-Token aus den GitHub Actions Secrets
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

def send_pure_text_pings():
    if not DISCORD_TOKEN:
        print("❌ Fehler: Kein DISCORD_TOKEN in den Umgebungsvariablen gefunden!")
        return

    # Deine korrekte Kanal-ID (1565663068695044187)
    api_url = "https://discord.com"
    token = DISCORD_TOKEN.strip()
    
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json",
        "User-Agent": "DiscordBot (https://github.com, 1.0.0)"
    }

    # Wir senden 2 ganz einfache Textzeilen
    for i in range(1, 3):
        now = datetime.now()
        timestamp_str = now.strftime("%d.%m.%Y um %H:%M Uhr")
        
        # Komplett reiner Text, um jede Form von Discord-Filter auszuhebeln
        simple_text = f"🚨 BOT-TEST-PING {i}/2 ERFOLGREICH! Der Smyths Monitor steht und die Kanal-ID passt perfekt. Zeit: {timestamp_str}"
        
        payload = json.dumps({"content": simple_text}).encode("utf-8")
        
        try:
            req = urllib.request.Request(api_url, data=payload, headers=headers)
            with urllib.request.urlopen(req) as res:
                print(f"🔥 Reiner Text-Ping {i} erfolgreich gesendet!")
        except Exception as e:
            print(f"❌ Fehler bei Text-Ping {i}: {e}")

send_pure_text_pings()
