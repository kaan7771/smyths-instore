import os
import json
import urllib.request
from datetime import datetime

# Deine hochgeladene Webhook-URL für den direkten Kanalzugriff
DISCORD_WEBHOOK_URL = "https://discord.com"

def send_clean_fake_ping():
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    now = datetime.now()
    timestamp_str = now.strftime("%d.%m.%Y um %H:%M Uhr")
    
    # Das exakte, saubere Original-Layout deines Monitors
    fancy_text = (
        f"╔════════════════════════════════════════════╗\n"
        f"        **SMYTHS TOYS INSTORE RESTOCK**\n"
        f"╚════════════════════════════════════════════╝\n\n"
        f"📝 **Product:** `Pokémon TCG: Erzwungener Test-Erfolg`\n"
        f"💰 **Price:** `€39.99`\n\n"
        f"📍 **Store:** `Smyths Hamburg-Altona`\n"
        f"📦 **Stock:** `5 ✅`\n"
        f"🏠 **Address:** `Musterstraße 1, 22765 Hamburg`\n\n"
        f"🔗 **Links:**\n"
        f"• [Product](https://smythstoys.com)\n"
        f"• [Google Maps Navigation](https://google.com)\n\n"
        f"────────────────────────────────────────\n"
        f"*TCGAlarm • Live Webhook • Smyths Monitor • heute um {timestamp_str}*"
    )
    
    payload = json.dumps({
        "username": "TCGAlarm Monitor",
        "content": fancy_text
    }).encode("utf-8")
    
    try:
        req = urllib.request.Request(DISCORD_WEBHOOK_URL, data=payload, headers=headers)
        with urllib.request.urlopen(req) as res:
            pass
        print("🔥 Sauberer Fake-Ping erfolgreich an Discord übermittelt!")
    except Exception as e:
        print(f"❌ Webhook-Fehler: {e}")

send_clean_fake_ping()
