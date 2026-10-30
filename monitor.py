import os
import json
import urllib.request
import urllib.parse
from datetime import datetime

# Deine Webhook-URL aus der Chat-Nachricht
DISCORD_WEBHOOK_URL = "https://discord.com"

def fake_smyths_stock_run():
    # Wir simulieren einfach 2 erfolgreiche Treffer direkt hier drin
    simulated_products = [
        {"name": "Pokémon TCG: Sanitoes Premium Kollektion", "price": "€39.99", "store": "Smyths Hamburg-Altona", "stock": "5"},
        {"name": "Glurak ex Super-Premium-Kollektion", "price": "€79.99", "store": "Smyths Berlin-Mall of Berlin", "stock": "12"}
    ]
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    for idx, prod in enumerate(simulated_products, 1):
        now = datetime.now()
        timestamp_str = now.strftime("%d.%m.%Y um %H:%M Uhr")
        
        fancy_text = (
            f"╔════════════════════════════════════════════╗\n"
            f"        **🔥 SMYTHS LIVE RESTOCK SIMULATION {idx}/2 🔥**\n"
            f"╚════════════════════════════════════════════╝\n\n"
            f"📝 **Product:** `{prod['name']}`\n"
            f"💰 **Price:** `{prod['price']}`\n\n"
            f"📍 **Store:** `{prod['store']}`\n"
            f"📦 **Stock:** `{prod['stock']} ✅`\n"
            f"🏠 **Address:** `Musterstraße, Deutschland`\n\n"
            f"────────────────────────────────────────\n"
            f"*Simulierter Test-Ping über Webhook-Route • {timestamp_str}*"
        )
        
        payload = json.dumps({
            "username": "TCGAlarm Monitor",
            "content": fancy_text
        }).encode("utf-8")
        
        try:
            req = urllib.request.Request(DISCORD_WEBHOOK_URL, data=payload, headers=headers)
            with urllib.request.urlopen(req) as res:
                print(f"🔥 Simulierter Live-Ping {idx} übermittelt!")
        except Exception as e:
            print(f"❌ Fehler: {e}")

fake_smyths_stock_run()
