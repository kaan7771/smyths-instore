import os
import requests

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

# Die Suchbegriffe, mit denen wir JEDES TCG-Produkt im Smyths-System aufspüren
KEYWORDS = ["pokemon", "one piece card game"]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://smythstoys.com"
}

session = requests.Session()
all_discovered_products = {}

# FESTE ABSICHERUNG: Die wichtigsten bekannten IDs (inkl. aller Booster & Blister) immer fest einspeisen
HARDCODED_IDS = {
    "222384": "One Piece TCG: Booster Pack (sortiert)",
    "236166": "One Piece TCG: Zoro & Sanji Starter Deck (ST-12)",
    "236167": "One Piece TCG: 3D2Y Starter Deck (ST-13)",
    "231555": "One Piece TCG: Wings of the Captain Booster Display",
    "210168": "Pokémon TCG: Set mit 2 Boosterpacks (Blister)",
    "220263": "Pokémon TCG: Sanfte Alola-Vulpix Tin-Box",
    "229871": "Pokémon TCG: Paldeas Schicksale Top-Trainer-Box (ETB)",
    "234567": "Pokémon TCG: Aktuelles Boosterpack (Sortiert)",
    "226789": "Pokémon TCG: Karmesin & Purpur 151 Kollektion",
    "218432": "Pokémon TCG: Strahlende Sterne Top-Trainer-Box"
}

for prod_id, prod_name in HARDCODED_IDS.items():
    all_discovered_products[prod_id] = prod_name

# LIVE-SUCHE: Wir ziehen uns ALLES, was Smyths aktuell unter den Begriffen listet (bis zu 200 Produkte!)
for keyword in KEYWORDS:
    for page in range(0, 2):  # Scannt Seite 1 und Seite 2 der internen API (Gesamt 200 Ergebnisse)
        search_url = f"https://smythstoys.com{keyword}&pageSize=100&currentPage={page}"
        try:
            search_res = session.get(search_url, headers=headers, timeout=12)
            if search_res.status_code == 200:
                search_data = search_res.json()
                products_list = search_data.get("products", [])
                for p in products_list:
                    code = p.get("code")
                    name = p.get("name", "")
                    name_lower = name.lower()
                    
                    # FILTER: Erfasst JEDEN Blister, Booster, Display, ETB, Tin, Box & Deck
                    allowed = ["booster", "display", "tin", "deck", "box", "kollektion", "blister", "top-trainer", "etb", "sammelkarten", "card game"]
                    ignored = ["plüsch", "figur", "spielzeug", "puzzle", "kuscheltier", "kostüm"]
                    
                    if any(term in name_lower for term in allowed) and not any(x in name_lower for x in ignored):
                        all_discovered_products[code] = name
        except Exception:
            pass

print(f"⚡ ULTRA-EXPRESS AKTIV: Überwache lückenlos {len(all_discovered_products)} TCG-Produkte.")

# LIVE-PRÜFUNG (ONLINE + INSTORE) FÜR ALLE GEFUNDENEN PRODUKTE
for prod_id, prod_name in all_discovered_products.items():
    API_URL = f"https://smythstoys.com{prod_id}/stock"
    try:
        response = session.get(API_URL, headers=headers, timeout=6)
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

            # --- CHECK B: FILIAL CHECK ---
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
