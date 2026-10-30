import os
import requests
import json
from datetime import datetime

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

PRODUCTS = ["231555", "233342"]

def check_smyths_stock():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for prod_id in PRODUCTS:
        print(f"🔍 Frage Live-Schnittstelle über Gateway ab für ID: {prod_id}...")
        
        # Smyths Toys Ziel-URL
        smyths_url = f"https://smythstoys.com{prod_id}/pointOfServices"
        
        # Korrekte Gateway-URL ohne Formatierungsfehler
        api_url = f"https://allorigins.win{smyths_url}"
        
        try:
            response = requests.get(api_url, headers=headers, timeout=15)
            if response.status_code != 200:
                print(f"⚠️ Gateway-Fehler ({response.status_code}) bei ID {prod_id}")
                continue
                
            wrapper_data = response.json()
            smyths_raw = wrapper_data.get("contents", "")
            
            if not smyths_raw or "pointOfServices" not in smyths_raw:
                print(f"ℹ️ Keine aktiven Bestände oder temporäre Blockade für ID {prod_id}.")
                continue
                
            data = json.loads(smyths_raw)
            prod_name = data.get("product", {}).get("name", "One Piece TCG Product")
            price = data.get("product", {}).get("price", {}).get("formattedValue", "119,99 €")
            
            for store in data.get("pointOfServices", []):
                stock_level = store.get("stockLevel", 0)
                stock_status = store.get("stockLevelStatus", {}).get("code", "")
                
                if stock_level > 0 or stock_status == "inStock":
                    store_name = store.get("name", "Smyths Filiale")
                    
                    if stock_level >= 15:
                        stock_display = "15+"
                    else:
                        stock_display = str(stock_level)
                    
                    address_data = store.get("address", {})
                    full_address = f"{address_data.get('line1', '')}, {address_data.get('postalCode', '')} {address_data.get('town', '')}"
                    product_url = f"https://smythstoys.com{prod_id}"
                    maps_url = f"https://google.com+{store_name.replace(' ', '+')}"
                    
                    send_discord_alert(prod_name, price, store_name, stock_display, full_address, product_url, maps_url)
                    
        except Exception as e:
            print(f"❌ Fehler bei der Verarbeitung von ID {prod_id}: {e}")

def send_discord_alert(prod_name, price, store_name, stock_display, full_address, product_url, maps_url):
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
    
    payload = {
        "username": "TCGAlarm",
        "content": fancy_text
    }
    
    requests.post(DISCORD_WEBHOOK, json=payload)
    print(f"🔥 Live-Restock für {store_name} erfolgreich an Discord übermittelt!")

check_smyths_stock()

