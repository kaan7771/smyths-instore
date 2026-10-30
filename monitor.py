import os
import requests
import re
import json
from datetime import datetime

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

PRODUCTS = [
    {
        "id": "231555",
        "detail_url": "https://smythstoys.com"
    },
    {
        "id": "233342",
        "detail_url": "https://smythstoys.com"
    }
]

def check_smyths_stock():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }
    
    for prod in PRODUCTS:
        print(f"🔍 Prüfe Bestände für Produkt-ID: {prod['id']}...")
        
        try:
            response = requests.get(prod["detail_url"], headers=headers, timeout=15)
            if response.status_code != 200:
                print(f"⚠️ Fehler beim Laden der Seite ({response.status_code}) bei ID {prod['id']}")
                continue
            
            # Findet die versteckten Filialdaten im Quelltext der Smyths-Webseite
            match = re.search(r'data-point-of-services\s*=\s*["\']({.*?})["\']', response.text)
            
            # Ausweichlösung falls das Attribut anders heißt
            if not match:
                match = re.search(r'id=["\']pointOfServicesData["\'][^>]*>([^<]+)', response.text)
                
            if match:
                data_str = match.group(1).replace('&quot;', '"')
                data = json.loads(data_str)
                
                # Produkt-Grunddaten auslesen
                prod_name = "One Piece TCG Display" if prod['id'] == "231555" else f"Smyths Produkt {prod['id']}"
                price_match = re.search(r'class=["\']price["\'][^>]*>([^<]+)', response.text)
                price = price_match.group(1).strip() if price_match else "119,99 €"
                
                for store in data if isinstance(data, list) else data.get("pointOfServices", []):
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
                        maps_url = f"https://google.com+{store_name.replace(' ', '+')}"
                        
                        send_discord_alert(prod_name, price, store_name, stock_display, full_address, prod["detail_url"], maps_url)
            else:
                print(f"ℹ️ Aktuell keine In-Store Bestandsdaten auf der Seite für ID {prod['id']} hinterlegt.")
                
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
    print(f"🔥 Live-Restock für {store_name} erfolgreich gesendet!")

check_smyths_stock()
