import os
import requests

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

# ==============================================================================
# DEINE FESTEN DAUER-FAVORITEN (Werden IMMER im System direkt abgefragt!)
# ==============================================================================
FAVORITE_IDS = {
    # --- ONE PIECE TCG ---
    "222384": "One Piece TCG: Booster Pack (sortiert)",
    "236166": "One Piece TCG: Zoro & Sanji Starter Deck (ST-12)",
    "236167": "One Piece TCG: 3D2Y Starter Deck (ST-13)",
    "231555": "One Piece TCG: Wings of the Captain Booster Display",
    
    # --- POKÉMON TCG ---
    "220263": "Pokémon TCG: Sanfte Alola-Vulpix Tin-Box",
    "229871": "Pokémon TCG: Paldeas Schicksale Top-Trainer-Box (ETB)",
    "234567": "Pokémon TCG: Aktuelles Boosterpack (Sortiert)",
    "226789": "Pokémon TCG: Karmesin & Purpur 151 Kollektion",
    "218432": "Pokémon TCG: Strahlende Sterne Top-Trainer-Box"
}

KEYWORDS = ["pokemon", "one piece card game"]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://smythstoys.com"
}

session = requests.Session()
all_discovered_products = {}

# 1. Schritt: Favoriten direkt einspeisen
for fav_id, fav_name in FAVORITE_IDS.items():
    all_discovered_products[fav_id] = fav_name

# 2. Schritt: Live-Suche nach neuen Produkten im Hintergrund
for keyword in KEYWORDS:
    search_url = f"https://smythstoys.com{keyword}&pageSize=100"
    try:
        search_res = session.get(search_url, headers=headers, timeout=12)
        if search_res.status_code == 200:
            search_data = search_res.json()
            products_list = search_data.get("products", [])
            for p in products_list:
                code = p.get("code")
                name = p.get("name", "")
                name_lower = name.lower()
                
                allowed_terms = ["booster", "display", "tin", "deck", "box", "kollektion", "blister", "top-trainer", "etb", "sammelkarten"]
                is_tcg_product = any(term in name_lower for term in allowed_terms)
                is_ignored = "plüsch" in name_lower or "figur" in name_lower or "spielzeug" in name_lower or "puzzle" in name_lower
                
                if is_tcg_product and not is_ignored:
                    all_discovered_products[code] = name
    except Exception:
        pass

print(f"🔎 Überwache aktuell insgesamt {len(all_discovered_products)} Produkte (Favoriten + Suchtreffer).")

# 3. Schritt: Bestandsprüfung für alle gesammelten IDs deutschlandweit
for prod_id, prod_name in all_discovered_products.items():
    API_URL = f"https://smythstoys.com{prod_id}/stock"
    try:
        response = session.get(API_URL, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            price = data.get("price", {}).get("formattedValue", "N/A")
            image_url = f"https://smythstoys.com{data.get('productImage')}" if data.get('productImage') else "https://imgur.com"
            
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
                    
                    product_url = f"https://smythstoys.comp/{prod_id}"
                    maps_url = f"https://google.com+{store_name}"
                    
                    payload = {
                        "username": "TCG Alerts Monitor",
                        "avatar_url": "https://imgur.com",
                        "embeds": [
                            {
                                "title": prod_name,
                                "description": "🟠 **Smyths Toys Instore Restock**",
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
                                "footer": {
                                    "text": "TCG Alerts • Instant Restock Pings",
                                    "icon_url": "https://imgur.com"
                                }
                            }
                        ]
                    }
                    requests.post(DISCORD_WEBHOOK, json=payload)
    except Exception:
        pass
