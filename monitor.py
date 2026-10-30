import os
import requests

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

payload = {
    "content": "🚀 **DER DISCORD-WEBHOOK FUNKTIONIERT PERFEKT!** 🚀\nDas GitHub-System hat eine direkte Verbindung zu deinem Server aufgebaut."
}

res = requests.post(DISCORD_WEBHOOK, json=payload)
print(f"Discord Antwort-Code: {res.status_code}")

