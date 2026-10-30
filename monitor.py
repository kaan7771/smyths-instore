import os
import requests
from datetime import datetime

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

# HIER DIE PRODUKTE DIREKT MIT VOLLSTÄNDIGER API-URL EINTRAGEN
PRODUCTS = [
    {
        "id": "231555",
        "detail_url": "https://smythstoys.com",
        "api_url": "https://smythstoys.com"
    },
    {
        "id": "233342",
        "detail_url": "https://smythstoys.com",
        "api_url": "https://smythstoys.com"
    }
]

def check_smyths_stock():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    for prod in PRODUCTS:
        print(f"🔍 Prüfe Bestände für Produkt-ID: {prod['id']}...")
        
        try:
            response = requests.get(prod["api_url"], headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"⚠️ API-Fehler ({response.status_code}) bei ID {prod['id']}")
                continue
                
            data = response.json()
            prod_name = data.get("product", {}).get("name", f"Smyths Produkt {prod['id']}")
            price = data.get("product", {}).get("price", {}).get("formattedValue", "N/A")
            
            for store in data.get("pointOfServices", []):
                stock_data = store.get("stockLevelStatus", {})
                stock_level = store.get("stockLevel", 0)
                
                if stock_data.get("code") == "inStock" or stock_level > 0:
                    store_name = store.get("name", "Unbekannte Filiale")
                    
                    if stock_level >= 15:
                        stock_display = "15+"
                    else:
                        stock_display = str(stock_level)
                    
                    address_data = store.get("address", {})
                    full_address = f"{address_data.get('line1', '')}, {address_data.get('postalCode', '')} {address_data.get('town', '')}"
                    maps_url = f"https://google.com+{store_name.replace(' ', '+')}"
                    
                    send_discord_alert(prod_name, price, store_name, stock_display, full_address, prod["detail_url"], maps_url)
                    
        except Exception as e:
            print(f"❌ Fehler beim Scrapen von ID {prod['id']}: {e}")

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
    print(f"🔥 Live-Restock für {store_name} als Text-Box gesendet!")

# Überwachung starten
check_smyths_stock()
