def check_smyths_stock():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # Zähler für den kontrollierten Testlauf
    gesendete_pings = 0

    for prod_id in PRODUCTS:
        print(f"🔍 Prüfe Bestände für Produkt-ID: {prod_id}...")
        
        target_url = f"https://smythstoys.com{prod_id}/pointOfServices"
        api_url = f"https://allorigins.win{urllib.parse.quote(target_url)}"
        
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
                        # Wir tun so, als ob wir einen Bestand von 0 als Treffer werten
                        stock_level = store.get("stockLevel", 0)
                        
                        if stock_level == 0:
                            store_name = store.get("name", "Smyths Filiale")
                            stock_display = "TEST-BESTAND"
                            
                            address_data = store.get("address", {})
                            full_address = f"{address_data.get('line1', '')}, {address_data.get('postalCode', '')} {address_data.get('town', '')}"
                            product_url = f"https://smythstoys.com{prod_id}"
                            maps_url = f"https://google.com{urllib.parse.quote(store_name)}"
                            
                            # Nachricht senden
                            send_discord_bot_message(prod_name, price, store_name, stock_display, full_address, product_url, maps_url)
                            gesendete_pings += 1
                            
                            # Wenn 2 Pings gesendet wurden, beenden wir das gesamte Skript komplett
                            if gesendete_pings >= 2:
                                print("✅ 2 Test-Pings gesendet. Beende Skript absichtlich.")
                                return
                            
        except Exception as e:
            continue

