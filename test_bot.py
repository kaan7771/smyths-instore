import os
import discord

intents = discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("Bot ist online auf GitHub Actions")

    # WICHTIG: Ersetze die Nullen hier mit deiner echten Discord-Kanal-ID!
    channel_id = 1565663068695044187
    channel = client.get_channel(channel_id)

    if channel:
        try:
            await channel.send("Hallo Welt von GitHub")
            print("Nachricht erfolgreich gesendet!")
        except discord.Forbidden:
            print("Fehler: Keine Rechte in diesem Kanal!")
        except discord.HTTPException as e:
            print(f"Discord-Fehler: {e}")
    else:
        print("Kanal nicht gefunden!")

    # Schließt den Bot, damit der GitHub-Workflow fertig wird
    await client.close()


token = os.getenv("BOT_TOKEN")
client.run(token)
