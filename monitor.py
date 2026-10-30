import os
import json
import urllib.request
from datetime import datetime

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

# DEINE KOMPLETTE NEUE LISTE AUS ALLEN LINKS (41 PRODUKTE)
PRODUCTS = [
    "231555", "233342", "263107", "261550", "265957", "259979", "256326", 
    "25412",  "254136", "254173", "254960", "256897", "256903", "257422", 
    "257657", "257662", "257692", "257700", "260757", "260819", "260842", 
    "260843", "261685", "261697", "262745", "262746", "263116", "263158", 
    "263166", "263203", "264014", "264015", "264148", "264149", "264175", 
    "264181", "264190", "265574", "265581", "265612", "265613", "252104", 
    "258850"
]

def check_smyths_stock():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    for prod_id in PRODUCTS:
        print(f"🔍 Prüfe Bestände für Produkt-ID: {prod_id}...")
        
        target_url = f"https://smythstoys.com{prod_id}/pointOfServices"
        api_url = f"https://allorigins.win{target_url}"
        
        try:
            req = urllib.request.Request(api_url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                if response.status == 200:
                    raw_data = response.read().decode("utf-8")
                    wrapper = json.loads(raw_data)
                    smyths_raw = wrapper.get("contents", "")
                    
                    if not smyths_raw or "pointOfServices" not in smyths_raw:
                        continue
                        
                    data = json.loads(smyths_raw)
                    prod_name = data.get("product", {}).get("name", f"TCG Produkt {prod_id}")
                    price = data.get("product", {}).get("price", {}).get("formattedValue", "N/A")
                    
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
            # Fehler abfangen falls eine ID temporär offline genommen wird
            continue

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
        print(f"🔥 Live-Restock erfolgreich an Discord übermittelt!")
    except Exception as e:
        print(f"❌ Discord-Fehler: {e}")

check_smyths_stock()
