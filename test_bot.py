import os
import discord
from datetime import datetime

# Deine bereits hinterlegte Kanal-ID
CHANNEL_ID = 1565663068695044187

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Test-Bot online als {client.user}")
    channel = client.get_channel(CHANNEL_ID)
    
    if channel:
        prod_name = "One Piece TCG: Wings of the Captain Booster Display"
        price = "119,99 €"
        store_name = "Hamburg-Eidelstedt"
        stock_display = "3" 
        full_address = "Hörgensweg 5, 22523 Eimsbüttel"
        
        product_url = "https://smythstoys.com"
        
        # JETZT GENAU WIE BEI TCGALERTS:
        # Ein reiner Text-Pfad ohne jegliche "?" oder "&" oder "%2C". Das kann Discord unmöglich beschneiden!
        maps_url = "https://google.com"
        
        now = datetime.now()
        timestamp_str = now.strftime("%d.%m.%Y um %H:%M Uhr")
        
        embed = discord.Embed(
            title="╔════════════════════════════════════════════╗\n        **SMYTHS TOYS INSTORE RESTOCK**\n╚════════════════════════════════════════════╝",
            color=16753920
        )
        
        embed.description = (
            f"📝 **Product:** `{prod_name}`\n"
            f"💰 **Price:** `{price}`\n\n"
            f"📍 **Store:** `{store_name}`\n"
            f"📦 **Stock:** `{stock_display}`\n"
            f"🏠 **Address:** `{full_address}`\n\n"
            f"🔗 **Links:**\n"
            f"• [Product]({product_url})\n"
            f"• [Google Maps Navigation]({maps_url})"
        )
        
        embed.set_footer(text=f"TCGAlarm • Live Pings • Smyths Monitor • heute um {timestamp_str}")
        
        try:
            await channel.send(embed=embed)
            print("Erfolg: Das professionelle Embed wurde gesendet!")
        except Exception as e:
            print(f"Fehler beim Senden: {e}")
            
    else:
        print("Kanal-ID nicht gefunden!")
        
    await client.close()

token = os.getenv("BOT_TOKEN")
client.run(token)
