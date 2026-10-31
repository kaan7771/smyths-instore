import os
import json
import urllib.request
import urllib.parse
from datetime import datetime
import urllib.error

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
STATE_FILE = "stock_state.json"

CHANNEL_ID = 1565663068695044187

PRODUCTS = [
    "231555", "233342", "263107", "261550", "265957", "259979", "256326", 
    "25412",  "254136", "254173", "254960", "256897", "256903", "257422", 
    "257657", "264014", "264015", "264148", "264149", "264175", "257662", 
    "257692", "257700", "260757", "260819", "260842", "260843", "261685", 
    "261697", "262745", "262746", "263116", "263158", "263166", "263203", 
    "264181", "264190", "265574", "265581", "265612", "265613", "252104", 
    "258850"
]

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

def check_smyths_stock():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    current_state = load_state()
    new_state = {}

    print("Starte Smyths Live Stock Check...")

    for prod_id in PRODUCTS:
        target_url = f"https://smythstoys.com{prod_id}/pointOfServices"
        cache_buster = int(datetime.now().timestamp())
        
        # KORREKTUR: Explizite Trennung von Basis-URL und Query-Parametern für AllOrigins
        encoded_url = urllib.parse.quote_plus(target_url)
        api_url = f"https://allorigins.win{encoded_url}&cb={cache_buster}"
        
        try:
            req = urllib.request.Request(api_url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                if response.status == 200:
                    raw_data = response.read().decode("utf-8")
                    wrapper = json.loads(raw_data)
                    smyths_raw = wrapper.get("contents", "")
                    
                    if not smyths_raw or "pointOfServices" not in smyths_raw:
                        print(f"Warnung: Keine Daten im Proxy für Produkt {prod_id}.")
                        continue
                        
                    data = json.loads(smyths_raw)
                    prod_name = data.get("product", {}).get("name", f"TCG Produkt {prod_id}")
                    price = data.get("product", {}).get("price", {}).get("formattedValue", "N/A")
                    
                    for store in data.get("pointOfServices", []):
                        stock_level = store.get("stockLevel", 0)
                        stock_status = store.get("stockLevelStatus", {}).get("code", "")
                        store_name = store.get("name", "Smyths Filiale")
                        
                        is_in_stock = stock_level > 0 or stock_status == "inStock"
                        state_key = f"{prod_id}_{store_name}"
                        
                        new_state[state_key] = is_in_stock
                        was_in_stock = current_state.get(state_key, False)
                        
                        if is_in_stock and not was_in_stock:
                            print(f"Echter Restock gefunden: {prod_name} in {store_name}!")
                            
                            if stock_level >= 15:
                                stock_display = "15"
                            else:
                                stock_display = str(stock_level)
                            
                            address_data = store.get("address", {})
                            full_address = f"{address_data.get('line1', '')}, {address_data.get('postalCode', '')} {address_data.get('town', '')}"
                            product_url = f"https://smythstoys.com{prod_id}"
                            
                            send_discord_bot_message(prod_name, price, store_name, stock_display, full_address, product_url)
                            
        except Exception as e:
            print(f"Fehler bei Produkt {prod_id}: {e}")
            continue

    save_state(new_state)
    print("Smyths Live Stock Check beendet.")

def send_discord_bot_message(prod_name, price, store_name, stock_display, full_address, product_url):
    if not DISCORD_TOKEN:
        print("Fehler: Kein DISCORD_TOKEN gefunden!")
        return
        
    import http.client
    
    now = datetime.now()
    timestamp_str = now.strftime("%d.%m.%Y um %H:%M Uhr")
    
    embed_description = (
        "📝 **Product:** `" + prod_name + "`\n"
        "💰 **Price:** `" + price + "`\n\n"
        "📍 **Store:** `" + store_name + "`\n"
        "📦 **Stock:** `" + stock_display + "`\n"
        "🏠 **Address:** `" + full_address + "`\n\n"
        "🔗 **Links:**\n"
        "• [Product](" + product_url + ")"
    )
    
    payload_dict = {
        "embeds": [
            {
                "title": "╔════════════════════════════════════════════╗\n        **SMYTHS TOYS INSTORE RESTOCK**\n╚════════════════════════════════════════════╝",
                "description": embed_description,
                "color": 16753920,
                "footer": {
                    "text": "TCGAlarm • Live Pings • Smyths Monitor • heute um " + timestamp_str
                }
            }
        ]
    }
    
    payload = json.dumps(payload_dict).encode("utf-8")
    
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
            print("Erfolg: Live Restock Embed erfolgreich gesendet!")
        else:
            print(f"Discord API Fehler ({response.status}): {data}")
            
        conn.close()
    except Exception as e:
        print(f"Netzwerkfehler beim Senden an Discord: {e}")

check_smyths_stock()
