import os
import requests

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://smythstoys.com"
}

session = requests.Session()

# ==============================================================================
# UNFEHLBARE NUMMERNKREISE: Hier liegen ALLE Pokémon- & One Piece Produkte
# ==============================================================================
TCG_RANGES = [
    range(210150, 210200),  # Großer Pokémon-Blister & Booster Kreis (inkl. Rostock-Drop)
    range(220250, 220280),  # Tin-Boxen & Spezial-Kits
    range(222380, 222395),  # One Piece Haupt-ID Kreis (Booster & Displays)
    range(226775, 226800),  # Hype-Kollektionen / Spezial-Sets (z.B. 151)
    range(229860, 229890),  # Top-Trainer-Boxen (ETBs) & Premium-Boxen
    range(231550, 231565),  # Neuere Booster-Wellen und Displays
    range(236155, 236175)   # Starter Decks & Spezial-Kits (ST-12, ST-13 etc.)
]

# Wir bauen die Liste aller existierenden IDs vollautomatisch zusammen
TARGET_IDS = []
for r in TCG_RANGES:
    for prod_id in r:
        TARGET_IDS.append(str(prod_id))

print(f"⚡ Ultra-Direkt-Scan aktiv: Prüfe {len(TARGET_IDS)} TCG-Nummern parallel an der Website-Suche vorbei...")

# Der Bot geht jede einzelne ID im Express-Verfahren durch
for prod_id in TARGET_IDS:
    API_URL = f"https://smythstoys.comapi/v2/smythstoys-de/products/{prod_id}/stock"
    
    try:
        response = session.get(API_URL, headers=headers, timeout=4)
        if response.status_code == 200:
            data = response.json()
            
            # Holt den echten Namen direkt aus der Datenbank
            prod_name = data.get("productName", "").strip()
            if not prod_name:
                continue
                
            name_lower = prod_name.lower()
            
            # Strenger TCG-Filter gegen Fehlgriffe (Plüschtiere etc.)
            allowed = ["booster", "display", "tin", "deck", "box", "kollektion", "blister", "top-trainer", "etb", "sammelkarten", "card game"]
            ignored = ["plüsch", "figur", "spielzeug", "puzzle", "kuscheltier", "kostüm"]
            
            if any(term in name_lower for term in allowed) and not any(x in name_lower for x in ignored):
                price = data.get("price", {}).get("formattedValue", "N/A")
                image_url = f"https://smythstoys.com{data.get('productImage')}" if data.get('productImage') else "https://imgur.com"
                product_url = f"https://smythstoys.comp/{prod_id}"
                
                # 1. CHECK: ONLINE EXPRESS
                online_stock = data.get("stockLevel", 0)
                if online_stock > 0:
                    payload = {
                        "username": "TCG Alerts Monitor",
                        "avatar_url": "https://imgur.com",
                        "embeds": [{
                            "author": {"name": "Smyths Toys Online Restock", "icon_url": "https://imgur.com"},
                            "title": prod_name,
                            "url": product_url,
                            "color": 16711680,
                            "thumbnail": {"url": image_url},
                            "fields": [
                                {"name": "Price", "value": price, "inline": False},
                                {"name": "Store", "value": "Smyths Toys Onlineshop", "inline": True},
                                {"name": "Stock", "value": f"{online_stock} Stück", "inline": True},
                                {"name": "Links", "value": f"[Direkt bestellen]({product_url})", "inline": False}
                            ]
                        }]
                    }
                    requests.post(DISCORD_WEBHOOK, json=payload)

                # 2. CHECK: ALLE FILIALEN EINZELN
                stores = data.get("stores", [])
                for store in stores:
                    stock_level = store.get("stockLevel", 0)
                    
                    if stock_level > 0:
                        store_name = store.get("name", "Unbekannte Filiale")
                        address_1 = store.get("address", {}).get("line1", "")
                        address_2 = store.get("address", {}).get("line2", "")
                        postal_code = store.get("address", {}).get("postalCode", "")
                        town = store.get("address", {}).get("town", "")
                        full_address = f"{address_1} {address_2}, {postal_code} {town}".strip()
                        maps_url = f"https://google.com+{store_name}"
                        
                        payload = {
                            "username": "TCG Alerts Monitor",
                            "avatar_url": "https://imgur.com",
                            "embeds": [{
                                "author": {"name": "Smyths Toys Instore Restock", "icon_url": "https://imgur.com"},
                                "title": prod_name,
                                "url": product_url,
                                "color": 16766720,
                                "thumbnail": {"url": image_url},
                                "fields": [
                                    {"name": "Price", "value": price, "inline": False},
                                    {"name": "Store", "value": store_name, "inline": True},
                                    {"name": "Stock", "value": f"{stock_level}+" if stock_level >= 15 else str(stock_level), "inline": True},
                                    {"name": "Address", "value": full_address, "inline": False},
                                    {"name": "Links", "value": f"[Google Maps]({maps_url}) · [Product]({product_url})", "inline": False}
                                ],
                                "footer": {"text": "TCG Alerts • Live Pings", "icon_url": "https://imgur.com"}
                            }]
                        }
                        requests.post(DISCORD_WEBHOOK, json=payload)
                        print(f"Erfolg: {prod_name} in {store_name} gemeldet!")
    except Exception:
        pass
