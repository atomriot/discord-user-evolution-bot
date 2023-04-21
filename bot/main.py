import argparse
import discord
import os
from dotenv import load_dotenv

async def send_it(message):
    print(f"sending message: {message}")
    await bot.get_channel(int(channelId)).send(str(message))
    return True

async def log_it(message):
    # send logs to the channel
    print(f"logging message: {message}")
    if(DEBUG_LOG == "1"):
        await send_it("UserEvolutionBot initialized")

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument('--cid', help="Channel ID to send logs to. If not used, the DISCORD_REPORTING_CHANNEL_ID value in the .env will be used instead. This setting will override the .env")
parser.add_argument('--debug', help="Whether or not to have debug logs get sent, set this to 1 to send debug logs. If not used, the DEBUG value in the .env will be used instead. This setting will override the .env")
args = parser.parse_args()

channelId = args.cid or os.getenv('DISCORD_REPORTING_CHANNEL_ID')
DEBUG_LOG = args.debug or os.getenv('DEBUG')

print(f"sending to {channelId} and debug set to {DEBUG_LOG}")

intents = discord.Intents.default()
intents.members = True
bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    log_it("UserEvolutionBot initialized")

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
