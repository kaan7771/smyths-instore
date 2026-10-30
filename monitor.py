import os
import json
import urllib.request
from datetime import datetime

# Holt das sichere Bot-Token aus den GitHub Actions Secrets
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

def send_forced_mention_ping():
    if not DISCORD_TOKEN:
        print("❌ Fehler: Kein DISCORD_TOKEN in den Umgebungsvariablen gefunden!")
        return

    # Deine korrekte Kanal-ID
    api_url = "https://discord.com"
    token = DISCORD_TOKEN.strip()
    
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json",
        "User-Agent": "DiscordBot (https://github.com, 1.0.0)"
    }

    now = datetime.now()
    timestamp_str = now.strftime("%d.%m.%Y um %H:%M Uhr")
    
    # @everyone zwingt den Server dazu, die Nachricht in deine Benachrichtigungen zu pushen
    forced_text = f"🔔 @everyone **ERZWUNGENER BOT-PING:** Der Smyths Monitor steht und die Kanal-ID passt perfekt! Zeit: {timestamp_str}"
    
    payload = json.dumps({"content": forced_text}).encode("utf-8")
    
    try:
        req = urllib.request.Request(api_url, data=payload, headers=headers)
        with urllib.request.urlopen(req) as res:
            print("🔥 Erzwungener Mention-Ping erfolgreich gesendet!")
    except Exception as e:
        print(f"❌ Fehler: {e}")

send_forced_mention_ping()
