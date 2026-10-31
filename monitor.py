def send_discord_bot_message(prod_name, price, store_name, stock_display, full_address, product_url, maps_url):
    if not DISCORD_TOKEN:
        print("Fehler: Kein DISCORD_TOKEN gefunden!")
        return
        
    import http.client
    
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
    
    payload = json.dumps({"content": fancy_text})
    
    headers = {
        "Authorization": f"Bot {DISCORD_TOKEN.strip()}",
        "Content-Type": "application/json",
        "User-Agent": "DiscordBot (https://github.com, 1.0.0)"
    }
    
    try:
        # Direkte Verbindung zum Discord-Host ohne urlopen-Umweg
        conn = http.client.HTTPSConnection("discord.com")
        path = f"/api/v10/channels/{CHANNEL_ID}/messages"
        
        conn.request("POST", path, body=payload, headers=headers)
        response = conn.getresponse()
        data = response.read().decode("utf-8")
        
        if response.status in:
            print(f"Erfolg: Künstliche Nachricht für '{prod_name}' gesendet!")
        else:
            print(f"Discord API Fehler ({response.status}): {data}")
            
        conn.close()
    except Exception as e:
        print(f"Schwerwiegender Netzwerkfehler: {e}")
