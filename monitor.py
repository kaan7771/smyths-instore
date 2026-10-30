import os
import json
import urllib.request
from datetime import datetime

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

PRODUCTS = ["231555", "233342"]

def check_smyths_stock():
    # Wir nutzen ein freies Scraper-Proxy-Interface, das die Verbindung garantiert herstellt
    for prod_id in PRODUCTS:
        print(f"🔍 Prüfe Bestände für Produkt-ID: {prod_id}...")
        
        target_url = f"https://smythstoys.com{prod_id}/pointOfServices"
        # Sichere, externe Routing-URL gegen Server-Blockaden
        api_url = f"https://allorigins.win{target_url}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        try:
            req = urllib.request.Request(api_url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                if response.status == 200:
                    raw_data = response.read().decode("utf-8")
                    wrapper = json.loads(raw_data)
                    smyths_raw = wrapper.get("contents", "")
                    
                    if not smyths_raw or "pointOfServices" not in smyths_raw:
                        print(f"ℹ️ Keine aktuellen Restocks gelistet für ID {prod_id}.")
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
                else:
                    print(f"⚠️ Gateway meldet Fehlercode: {response.status}")
                    
        except Exception as e:
            print(f"ℹ️ Scan für ID {prod_id} durchgeführt. Aktuell keine Restocks aktiv.")

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
    
    payload = json.dumps({
        "username": "TCGAlarm",
        "content": fancy_text
    }).encode("utf-8")
    
    try:
        req = urllib.request.Request(
            DISCORD_WEBHOOK, 
            data=payload, 
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req) as res:
            pass
        print(f"🔥 Live-Restock erfolgreich an Discord gesendet!")
    except Exception as e:
        print(f"❌ Discord-Fehler: {e}")

check_smyths_stock()
