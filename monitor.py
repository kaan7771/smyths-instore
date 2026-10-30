import json
import urllib.request
from datetime import datetime

# Deine verifizierte Webhook-URL mit dem offiziellen /slack Kompatibilitäts-Zusatz
SLACK_WEBHOOK_URL = "https://discord.com"

def send_forced_slack_ping():
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    now = datetime.now()
    timestamp_str = now.strftime("%d.%m.%Y um %H:%M Uhr")
    
    # Slack-kompatibles Payload-Format, das Discords Filter direkt umgeht
    payload_data = {
        "username": "TCGAlarm Live-Test",
        "text": (
            f"╔════════════════════════════════════════════╗\n"
            f"        **⚙️ ERZWUNGENER LIVE FAKE-PING ⚙️**\n"
            f"╚════════════════════════════════════════════╝\n\n"
            f"📝 **Product:** `Smyths Instore Brücken-Test`\n"
            f"📦 **Status:** `Verbindung erfolgreich erzwungen! ✅`\n\n"
            f"────────────────────────────────────────\n"
            f"*Der Webhook-Kanal steht! • {timestamp_str}*"
        )
    }
    
    payload = json.dumps(payload_data).encode("utf-8")
    
    try:
        req = urllib.request.Request(SLACK_WEBHOOK_URL, data=payload, headers=headers)
        with urllib.request.urlopen(req) as res:
            print("🔥 Absoluter Webhook-Fallpack-Ping erfolgreich rausgefeuert!")
    except Exception as e:
        print(f"❌ Kritischer Fehler beim Erzwingen: {e}")

send_forced_slack_ping()
