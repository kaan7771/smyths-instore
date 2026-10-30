import os
import json
import urllib.request
from datetime import datetime

# Holt das sichere Bot-Token aus den GitHub Actions Secrets
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

def send_fake_ping():
    if not DISCORD_TOKEN:
        print("❌ Fehler: Kein DISCORD_TOKEN in den Umgebungsvariablen gefunden!")
        return

    # Deine Kanal-ID
    api_url = "https://discord.com"

    now = datetime.now()
    timestamp_str = now.strftime("%d.%m.%Y um %H:%M Uhr")
    
    fancy_text = (
        f"╔════════════════════════════════════════════╗\n"
        f"        **⚠️ TEST: FAKE PING ERFOLGREICH ⚠️**\n"
        f"╚════════════════════════════════════════════╝\n\n"
        f"📝 **Product:** `Test TCG Pokémon Box`\n"
        f"💰 **Price:** `€39.99`\n\n"
        f"📍 **Store:** `Testfiliale Hamburg`\n"
        f"📦 **Stock:** `5 ✅`\n"
        f"🏠 **Address:** `Musterstraße 1, 20000 Hamburg`\n\n"
        f"────────────────────────────────────────\n"
        f"*Der Verbindungstest war erfolgreich! • {timestamp_str}*"
    )
    
    payload = json.dumps({
        "content": fancy_text
    }).encode("utf-8")
    
    try:
        req = urllib.request.Request(
            api_url, 
            data=payload, 
            headers={
                "Authorization": f"Bot {DISCORD_TOKEN}",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0"
            }
        )
        with urllib.request.urlopen(req) as res:
            pass
        print(f"🔥 Fake-Ping erfolgreich an Discord-Kanal übermittelt!")
    except Exception as e:
        print(f"❌ Discord-Bot-Fehler: {e}")

# Startet direkt den Fake-Ping
send_fake_ping()

