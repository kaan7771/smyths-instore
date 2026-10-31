import os
import discord
from discord import File

# Deine übergebene Rules-Kanal-ID
CHANNEL_ID = 1565372653425008965

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Regel-Bot online als {client.user}")
    channel = client.get_channel(CHANNEL_ID)
    
    if channel:
        # Die Regeln sauber formatiert mit großem RULES und extra Abstand unten
        rules_text = (
            "# RULES\n\n" # Macht das "RULES" deutlich größer
            "Please follow all the rules listed below while participating in this server.\n\n"
            "1. **No harassment of others**\n"
            "Racism, sexism, xenophobia, transphobia, homophobia, misogyny, etc. are not allowed.\n\n"
            "2. **Keep all discussion civil and in the correct channels**\n"
            "Mods may asks you to move your conversation to the correct channel.\n\n"
            "3. **No inappropriate language**\n"
            "Remain respectful of others at all times.\n\n"
            "4. **Keep personal drama out of chat**\n"
            "Keep personal drama out of chat.\n\n"
            "5. **No impersonation**\n"
            "Do not impersonate other users, moderators, and/or famous personalities.\n\n"
            "6. **No spamming**\n"
            "Do not flood chat rooms with messages. Encouraging others to spam is also not allowed.\n\n"
            "7. **No NSFW content**\n"
            "Do not post or have conversations around NSFW content.\n\n"
            "8. **No inappropriate or offensive usernames, status's or profile pictures**\n"
            "You may be asked to change these if they violate our rules.\n\n"
            "9. **No politics**\n"
            "Talking about serious issues involving government officials, political parties, religions, or geo-political disagreements is not allowed. Even if these topics are approached in a civil manner, this is not the correct space for these conversations.\n\n"
            "10. **No self-promotion, soliciting, or advertising**\n"
            "This also includes user DMs.\n\n"
            "11. **No malicious links**\n"
            "Any link that track IP addresses, or lead to malicious websites that contain malware will be removed.\n\n"
            "12. **Don't evade filters**\n"
            "This applies to both words and links. If something is censored, it is censored for a reason!\n\n"
            "13. **Follow the Discord ToS and Community Guidelines**\n"
            "Terms of Service: https://discordapp.com\n"
            "Community Guidelines: https://discord.com\n\n"
            "14. **Moderators hold final say**\n"
            "Listen to and respect the volunteers that keep this server running.\n"
            "\n‎\n" # Unsichtbarer Zeilenumbruch für echten Abstand
            "**React once you have understood.**" # Fett gedruckt
        )
        
        embed = discord.Embed(
            description=rules_text,
            color=16753920 # Das schöne TCG-Orange
        )
        
        # JETZT KORRIGIERT: Der Bot sucht jetzt nach deiner Datei inklusive der .jfif Endung!
        image_path = "rules_banner.png.jfif"
        if os.path.exists(image_path):
            file = File(image_path, filename="rules_banner.png")
            embed.set_image(url="attachment://rules_banner.png")
            
            try:
                await channel.send(file=file, embed=embed)
                print("Erfolg: Regeln mit Banner wurden in Discord gepostet!")
            except Exception as e:
                print(f"Fehler beim Senden: {e}")
        else:
            print(f"Fehler: '{image_path}' wurde auf GitHub nicht gefunden!")
            try:
                await channel.send(embed=embed)
                print("Regeln wurden ohne Bild gesendet.")
            except Exception as e:
                print(f"Fehler beim Senden: {e}")
    else:
        print("Kanal nicht gefunden. Prüfe die ID.")
        
    await client.close()

token = os.getenv("BOT_TOKEN")
client.run(token)
