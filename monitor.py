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
        "Cache-Control": "no-cache"
    }
    
    for prod in PRODUCTS:
        print(f"🔍 Prüfe Bestände für Produkt-ID: {prod['id']}...")
        
        try:
            response = requests.get(prod["detail_url"], headers=headers, timeout=15)
            if response.status_code != 200:
                print(f"⚠️ Fehler beim Laden der Seite ({response.status_code}) bei ID {prod['id']}")
                continue
            
            # Liest den globalen Produktdaten-Block aus, in dem Smyths Toys alle Filialbestände speichert
            match = re.search(r'pointOfServicesData\s*:\s*(\[.*?\])\s*,', response.text)
            if not match:
                match = re.search(r'data-point-of-services\s*=\s*["\'](.*?)["\']', response.text)
                
            if match:
                raw_data = match.group(1).replace('&quot;', '"')
                stores = json.loads(raw_data)
                
                # Produktname und Preis automatisch finden
                name_match = re.search(r'<h1[^>]*>([^<]+)</h1>', response.text)
                prod_name = name_match.group(1).strip() if name_match else "One Piece TCG Product"
                
                price_match = re.search(r'class=["\']price[^"\']*["\'][^>]*>([^<]+)', response.text)
                price = price_match.group(1).strip() if price_match else "119,99 €"
                
                for store in stores:
                    stock_level = store.get("stockLevel", 0)
                    stock_status = store.get("stockLevelStatus", {}).get("code", "")
                    
                    if stock_level > 0 or stock_status == "inStock":
                        store_name = store.get("displayName", store.get("name", "Smyths Filiale"))
                        
                        if stock_level >= 15:
                            stock_display = "15+"
                        else:
                            stock_display = str(stock_level)
                        
                        address_data = store.get("address", {})
                        full_address = f"{address_data.get('line1', '')}, {address_data.get('postalCode', '')} {address_data.get('town', '')}"
                        maps_url = f"https://google.com+{store_name.replace(' ', '+')}"
                        
                        send_discord_alert(prod_name, price, store_name, stock_display, full_address, prod["detail_url"], maps_url)
            else:
                print(f"ℹ️ Seite erfolgreich geladen, scanne alternative Datenblöcke für ID {prod['id']}...")
                
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
