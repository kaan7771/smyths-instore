import os
import json
import urllib.request
from datetime import datetime

# Holt das sichere Bot-Token aus den GitHub Actions Secrets
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

def send_test_pings():
    if not DISCORD_TOKEN:
        print("❌ Fehler: Kein DISCORD_TOKEN in den Umgebungsvariablen gefunden!")
        return

    api_url = "https://discord.com"
    token = DISCORD_TOKEN.strip()
    
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json",
        "User-Agent": "DiscordBot (https://github.com, 1.0.0)"
    }

    # Wir senden direkt 2 Nachrichten hintereinander
    for i in range(1, 3):
        now = datetime.now()
        timestamp_str = now.strftime("%d.%m.%Y um %H:%M Uhr")
        
        fancy_text = (
            f"╔════════════════════════════════════════════╗\n"
            f"        **⚙️ SMYTHS MONITOR TEST-PING {i}/2 ⚙️**\n"
            f"╚════════════════════════════════════════════╝\n\n"
            f"📝 **Product:** `Direkter Verbindungstest`\n"
            f"📦 **Status:** `Erfolgreich erzwungen ✅`\n\n"
            f"────────────────────────────────────────\n"
            f"*Der Bot-Kanal empfängt Daten! • {timestamp_str}*"
        )
        
        payload = json.dumps({"content": fancy_text}).encode("utf-8")
        
        try:
            req = urllib.request.Request(api_url, data=payload, headers=headers)
            with urllib.request.urlopen(req) as res:
                print(f"🔥 Test-Ping {i} erfolgreich gesendet!")
        except urllib.error.HTTPError as e:
            print(f"❌ Discord-Fehler bei Ping {i}: {e.code} - {e.read().decode('utf-8')}")
        except Exception as e:
            print(f"❌ Allgemeiner Fehler bei Ping {i}: {e}")

send_test_pings()
