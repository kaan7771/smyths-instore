import os
import json
import urllib.request
from datetime import datetime

# Holt das sichere Bot-Token aus deinen GitHub Secrets
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

def send_forced_bot_pings():
    if not DISCORD_TOKEN:
        print("❌ Fehler: Kein DISCORD_TOKEN in den GitHub Secrets gefunden!")
        return

    # Deine verifizierte Kanal-ID aus Discord
    api_url = "https://discord.com"
    token = DISCORD_TOKEN.strip()
    
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json",
        "User-Agent": "DiscordBot (https://github.com, 1.0.0)"
    }

    # Wir senden sofort 2 Test-Nachrichten hintereinander über den Bot
    for i in range(1, 3):
        now = datetime.now()
        timestamp_str = now.strftime("%d.%m.%Y um %H:%M Uhr")
        
        fancy_text = (
            f"╔════════════════════════════════════════════╗\n"
            f"        **🤖 ERZWUNGENER BOT-PING {i}/2 🤖**\n"
            f"╚════════════════════════════════════════════╝\n\n"
            f"📝 **Product:** `Reiner Bot-Verbindungstest`\n"
            f"📦 **Status:** `Kanal-ID korrigiert und zugestellt! ✅`\n\n"
            f"────────────────────────────────────────\n"
            f"*Der Bot läuft direkt über das Token! • {timestamp_str}*"
        )
        
        payload = json.dumps({"content": fancy_text}).encode("utf-8")
        
        try:
            req = urllib.request.Request(api_url, data=payload, headers=headers)
            with urllib.request.urlopen(req) as res:
                print(f"🔥 Bot-Ping {i} erfolgreich gesendet!")
        except urllib.error.HTTPError as e:
            print(f"❌ Discord-Fehler bei Bot-Ping {i}: {e.code} - {e.read().decode('utf-8')}")
        except Exception as e:
            print(f"❌ Allgemeiner Fehler bei Bot-Ping {i}: {e}")

send_forced_bot_pings()

