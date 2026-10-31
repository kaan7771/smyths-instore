import os
import json
from datetime import datetime

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
STATE_FILE = "stock_state.json"

# Deine feste Discord Kanal-ID
CHANNEL_ID = 1565663068695044187

if os.path.exists(STATE_FILE):
    try:
        os.remove(STATE_FILE)
        print("Alten Speicherstand gelöscht, um Restock zu erzwingen.")
    except Exception as e:
        print(f"Konnte State-File nicht löschen: {e}")

def check_smyths_stock_SIMULATED():
    print("Starte simulierten Smyths Stock Check...")
    
    prod_name = "One Piece TCG: Wings of the Captain Booster Display"
    price = "119,99 €"
    store_name = "Hamburg-Eidelstedt"
    stock_display = "3" 
    full_address = "Hörgensweg 5, 22523 Eimsbüttel"
    
    # Reine URLs ohne Klammern oder Formatierung für die Variablen
    product_url = "https://smythstoys.com"
    maps_url = "https://google.com"
    
    print(f"SIMULATION: Restock entdeckt: {prod_name} in {store_name}!")
    
    send_discord_bot_message(prod_name, price, store_name, stock_display, full_address, product_url, maps_url)
    print("Simulierter Stock Check beendet.")

def send_discord_bot_message(prod_name, price, store_name, stock_display, full_address, product_url, maps_url):
    if not DISCORD_TOKEN:
        print("Fehler: Kein DISCORD_TOKEN gefunden!")
        return
        
    import http.client
    
    now = datetime.now()
    timestamp_str = now.strftime("%d.%m.%Y um %H:%M Uhr")
    
    # Markdown-Hyperlinks direkt sauber im Text platziert
    fancy_text = (
        f"╔════════════════════════════════════════════╗\n"
        f"        **SMYTHS TOYS INSTORE RESTOCK**\n"
        f"╚════════════════════════════════════════════╝\n\n"
        f"📝 **Product:** `{prod_name}`\n"
        f"💰 **Price:** `{price}`\n\n"
        f"📍 **Store:** `{store_name}`\n"
        f"📦 **Stock:** `{stock_display}`\n"
        f"🏠 **Address:** `{full_address}`\n\n"
        f"🔗 **Links:**\n"
        f"• [Product]({product_url})\n"
        f"• [Google Maps Navigation]({maps_url})\n\n"
        f"────────────────────────────────────────\n"
        f"*TCGAlarm • Live Pings • Smyths Monitor • heute um {timestamp_str}*"
    )
    
    payload = json.dumps({"content": fancy_text})
    
    headers = {
        "Authorization": f"Bot {DISCORD_TOKEN.strip()}",
        "Content-Type": "application/json",
        "User-Agent": "DiscordBot (https://github.com, 1.0.0)"
    }
    
    try:
        conn = http.client.HTTPSConnection("discord.com")
        path = f"/api/v10/channels/{CHANNEL_ID}/messages"
        
        conn.request("POST", path, body=payload, headers=headers)
        response = conn.getresponse()
        data = response.read().decode("utf-8")
        
        status_code = int(response.status)
        if status_code == 200 or status_code == 201:
            print(f"Erfolg: Nachricht erfolgreich gesendet!")
        else:
            print(f"Discord API Fehler ({response.status}): {data}")
            
        conn.close()
    except Exception as e:
        print(f"Schwerwiegender Netzwerkfehler: {e}")

# Simulation starten
check_smyths_stock_SIMULATED()
