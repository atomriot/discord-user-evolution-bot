import discord
import os
from dotenv import load_dotenv

async def send_it(message):
    print(f"sending message: {message}")
    await bot.get_channel(int(os.getenv('DISCORD_REPORTING_CHANNEL_ID'))).send(str(message))
    return True

load_dotenv()

intents = discord.Intents.default()
intents.members = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    if(os.getenv("DEBUG") is not None and os.getenv("DEBUG") == "1"):
        await send_it("UserEvolutionBot initialized")

@bot.event
async def on_user_update(before, after):
    print("user_change")
    if before.name != after.name:
        await send_it(f"User [ {str(before.name)} ] changed their name to [{str(after.name)}].")

@bot.event
async def on_member_update(before, after):
    print("member_change")
    if before.nick != after.nick:
        if before.nick is None:
            await send_it(f"Member [{str(before.name)}] changed their nickname to [{str(after.nick)}].")
        elif after.nick is None:
            await send_it(f"Member [{str(before.name)}] removed their nickname.")
        else:
            await send_it(f"Member [{str(before.nick)}] changed their nickname to [{str(after.nick)}].")
    if before.name != after.name:
        await send_it(f"Member [{str(before.name)}] changed their name to [{str(after.name)}].")


bot.run(os.getenv('DISCORD_BOT_TOKEN'))
