import os
import discord
from datetime import datetime

# Deine bereits hinterlegte Kanal-ID
CHANNEL_ID = 1565663068695044187

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Test-Bot online")
    channel = client.get_channel(CHANNEL_ID)
    
    if channel:
        prod_name = "One Piece TCG: Wings of the Captain Booster Display"
        price = "119,99 €"
        store_name = "Hamburg-Eidelstedt"
        stock_display = "3" 
        full_address = "Hörgensweg 5, 22523 Eimsbüttel"
        
        product_url = "https://smythstoys.com"
        
        # EXAKT WIE BEI TCGALERTS: Der saubere Google Maps API-Suchlink.
        # Ohne f-String kommt die URL jetzt zu 100% unbeschädigt durch!
        maps_url = "https://google.com"
        
        now = datetime.now()
        timestamp_str = now.strftime("%d.%m.%Y um %H:%M Uhr")
        
        # JETZT NEU: Normaler Text-String ohne f-String! Die Variablen werden am Ende sicher eingesetzt.
        raw_text = (
            "📝 **Product:** " + prod_name + "\n"
            "💰 **Price:** " + price + "\n\n"
            "📍 **Store:** " + store_name + "\n"
            "📦 **Stock:** " + stock_display + "\n"
            "🏠 **Address:** " + full_address + "\n\n"
            "🔗 **Links:**\n"
            "• [Product](" + product_url + ")\n"
            "• [Google Maps Navigation](" + maps_url + ")"
        )
        
        embed = discord.Embed(
            title="╔════════════════════════════════════════════╗\n        **SMYTHS TOYS INSTORE RESTOCK**\n╚════════════════════════════════════════════╝",
            description=raw_text,
            color=16753920
        )
        
        embed.set_footer(text="TCGAlarm • Live Pings • Smyths Monitor • heute um " + timestamp_str)
        
        try:
            await channel.send(embed=embed)
            print("Erfolg: Embed wurde gesendet!")
        except Exception as e:
            print("Fehler beim Senden: ", e)
            
    else:
        print("Kanal-ID nicht gefunden!")
        
    await client.close()

token = os.getenv("BOT_TOKEN")
client.run(token)
