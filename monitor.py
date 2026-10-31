import os
import json
import urllib.request
import urllib.parse
from datetime import datetime
import urllib.error

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
STATE_FILE = "stock_state.json"

# Deine feste Discord Kanal-ID
CHANNEL_ID = 1565663068695044187

# Wir löschen den alten Zustand, um einen neuen Restock zu erzwingen
if os.path.exists(STATE_FILE):
    try:
        os.remove(STATE_FILE)
        print("Alten Speicherstand gelöscht, um Restock zu erzwingen.")
    except Exception as e:
        print(f"Konnte State-File nicht löschen: {e}")

PRODUCTS = ["231555"] # Für den schnellen Test reicht ein Produkt

def check_smyths_stock_SIMULATED():
    print("Starte simulierten Smyths Stock Check...")
    
    # --- KÜNSTLICHER RESTOCK-DATENSATZ ---
    prod_name = "One Piece TCG: Wings of the Captain Booster Display"
    price = "119,99 €"
    store_name = "Hamburg-Altona"
    stock_display = "3 Stück"
    full_address = "Sülldorfer Landstraße 42, 22589 Hamburg"
    product_url = "https://smythstoys.com"
    maps_url = f"https://google.com{urllib.parse.quote(store_name)}"
    
    print(f"SIMULATION: Restock entdeckt: {prod_name} in {store_name}!")
    
    # Sendet die Nachricht sofort ab
    send_discord_bot_message(prod_name, price, store_name, stock_display, full_address, product_url, maps_url)
    print("Simulierter Stock Check beendet.")

def send_discord_bot_message(prod_name, price, store_name, stock_display, full_address, product_url, maps_url):
    if not DISCORD_TOKEN:
        print("Fehler: Kein DISCORD_TOKEN in den GitHub Umgebungs-Variablen gefunden!")
        return
        
    api_url = f"https://discord.com{CHANNEL_ID}/messages"
    now = datetime.now()
    timestamp_str = now.strftime("%d.%m.%Y um %H:%M Uhr")
    
    fancy_text = (
        f"╔════════════════════════════════════════════╗\n"
        f"        **SMYTHS TOYS INSTORE RESTOCK**\n"
        f"╚════════════════════════════════════════════╝\n\n"
        f"📝 **Product:** `{prod_name}`\n"
        f"💰 **Price:** `{price}`\n\n"
        f"📍 **Store:** `{store_name}`\n"
        f"📦 **Stock:** `{stock_display} ✅`\n"
        f"🏠 **Address:** `{full_address}`\n\n"
        f"🔗 **Links:**\n"
        f"• [Product]({product_url})\n"
        f"• [Google Maps Navigation]({maps_url})\n\n"
        f"────────────────────────────────────────\n"
        f"*TCGAlarm • Live Pings • Smyths Monitor • heute um {timestamp_str}*"
    )
    
    payload = json.dumps({"content": fancy_text}).encode("utf-8")
    headers = {
        "Authorization": f"Bot {DISCORD_TOKEN.strip()}",
        "Content-Type": "application/json",
        "User-Agent": "DiscordBot (https://github.com, 1.0.0)"
    }
    
    try:
        req = urllib.request.Request(api_url, data=payload, headers=headers)
        with urllib.request.urlopen(req) as res:
            print(f"Erfolg: Künstliche Nachricht für '{prod_name}' an Discord gesendet!")
    except urllib.error.HTTPError as e:
        print(f"Discord API Fehler ({e.code}): {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"Allgemeiner Fehler beim Senden an Discord: {e}")

# Simulation starten
check_smyths_stock_SIMULATED()
