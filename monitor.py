import os
import requests

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://smythstoys.com"
}

session = requests.Session()
all_discovered_products = {}

# ==============================================================================
# 1. SCHRITT: SCANNE AUTOMATISCH DIE RELEVANTEN ID-NUMMERNBLÖCKE FÜR TCG (BLISTER/ETBS)
# ==============================================================================
# Wir scannen die Nummern-Kreise, in denen Smyths TCG-Artikel einspeist (z.B. 210160 bis 210200, etc.)
id_ranges = [
    range(222380, 222390),  # One Piece Haupt-ID Kreis
    range(236160, 236175),  # Starter Decks & Spezial-Kits
    range(231550, 231560),  # Displays & Booster-Wellen
    range(210160, 210180),  # Pokémon Blister-Kreis (inkl. 210168 Rostock-Drop)
    range(220260, 220270),  # Tin-Boxen
    range(229865, 229880),  # Top-Trainer-Boxen (ETBs) & Kollektionen
    range(226780, 226795)   # Spezial-Kollektionen / Hype-Sets
]

print("⚡ Starte API-Direktscan für alle Blister, Boxen und TCG-Artikel...")

for id_range in id_ranges:
    for prod_id in id_range:
        str_id = str(prod_id)
        API_URL = f"https://smythstoys.com{str_id}/stock"
        try:
            response = session.get(API_URL, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                # Wir holen den echten Produktnamen direkt aus der API-Datenbank
                # Das funktioniert auch dann, wenn der Artikel auf der Website versteckt ist!
                prod_name = data.get("productName", "").strip()
                if not prod_name:
                    continue
                    
                name_lower = prod_name.lower()
                
                # FILTER: Nur echte TCG-Artikel durchlassen
                allowed = ["booster", "display", "tin", "deck", "box", "kollektion", "blister", "top-trainer", "etb", "sammelkarten", "card game"]
                ignored = ["plüsch", "figur", "spielzeug", "puzzle", "kuscheltier", "kostüm"]
                
                if any(term in name_lower for term in allowed) and not any(x in name_lower for x in ignored):
                    all_discovered_products[str_id] = prod_name
        except Exception:
            pass

print(f"✅ Scanner-Setup abgeschlossen. Überwache dauerhaft {len(all_discovered_products)} TCG-Produkte im Express-Modus.")

# ==============================================================================
# 2. SCHRITT: BUNDESWEITE LIVE-BESTANDSPRÜFUNG (ONLINE + INSTORE)
# ==============================================================================
for prod_id, prod_name in all_discovered_products.items():
    API_URL = f"https://smythstoys.com{prod_id}/stock"
    try:
        response = session.get(API_URL, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            price = data.get("price", {}).get("formattedValue", "N/A")
            image_url = f"https://smythstoys.com{data.get('productImage')}" if data.get('productImage') else "https://imgur.com"
            product_url = f"https://smythstoys.comp/{prod_id}"
            
            # --- CHECK A: ONLINE EXPRESS CHECK ---
            online_stock = data.get("stockLevel", 0)
            if online_stock > 0 or data.get("stockLevelStatus") == "inStock":
                payload = {
                    "username": "TCG Alerts Monitor",
                    "avatar_url": "https://imgur.com",
                    "embeds": [
                        {
                            "author": {"name": "Smyths Toys Online Restock", "icon_url": "https://imgur.com"},
                            "title": prod_name,
                            "url": product_url,
                            "color": 16711680,
                            "thumbnail": {"url": image_url},
                            "fields": [
                                {"name": "Price", "value": price, "inline": False},
                                {"name": "Store", "value": "Smyths Toys Onlineshop (Zentrallager)", "inline": True},
                                {"name": "Stock", "value": f"{online_stock} Stück online!", "inline": True},
                                {"name": "Links", "value": f"[Direkt bestellen]({product_url})", "inline": False}
                            ],
                            "footer": {"text": "TCG Alerts • Instant Restock Pings", "icon_url": "https://imgur.com"}
                        }
                    ]
                }
                requests.post(DISCORD_WEBHOOK, json=payload)

            # --- CHECK B: FILIAL-EXPRESS CHECK ---
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
                        "embeds": [
                            {
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
                                "footer": {"text": "TCG Alerts • Instant Restock Pings", "icon_url": "https://imgur.com"}
                            }
                        ]
                    }
                    requests.post(DISCORD_WEBHOOK, json=payload)
    except Exception:
        pass
