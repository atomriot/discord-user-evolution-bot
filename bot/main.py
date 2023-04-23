import argparse
import discord
import os
import logging
import sys
from dotenv import load_dotenv

async def send_it(server,message):
    logging.info(f"sending to server: {server}. message: {message}")
    channel_id = server_channels[int(server)]
    if channel_id is None:
        logging.info(f"Error sending to server, channel not found for server {server}")
        return False

    discord_server = bot.get_guild(int(server))
    if discord_server is None:
        logging.error(f"The bot does not have access to the server {server}")
        return False

    channel = discord_server.get_channel(channel_id)
    if channel is None:
        logging.info(f"Channel with ID {channel_id} not found.")
        return False

    bot_member = discord_server.get_member(bot.user.id)
    if bot_member is None:
        logging.info(f"bot is not a member of {server}")
        return False

    bot_permissions = channel.permissions_for(bot_member)
    if not bot_permissions.send_messages:
        print("Bot does not have the permission to send messages in the specified channel.")
        return False

    try:
        await channel.send(str(message))
        return True
    except Exception as e:
        logging.error(f"Error sending to {server}")
        logging.exception(e)

    return False

load_dotenv()

#configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter('%(levelname)s %(message)s')
console_handler.setFormatter(console_formatter)
logging.getLogger('').addHandler(console_handler)

#parse incoming commands or .env
parser = argparse.ArgumentParser()
parser.add_argument('--server_channels',help="This is a list of server id and channel id. Split server and chanel with : and to add multiple servers and channels use a comman like s1:c1,s2:c2 where s1 and s2 are the server IDs and c1 and c2 are the channel IDs. This will be used to ensure the member update goes to the correct server. If not used, the SERVER_ID_CHANNEL_IDS value in the .env will be used instead. This setting will override the .env")
args = parser.parse_args()

server_channels_string = args.server_channels or os.getenv('SERVER_ID_CHANNEL_IDS')
server_channels_list = server_channels_string.split(',')
server_channels = {}
if len(server_channels_list) > 0:
    for server_channel in server_channels_list:
        server, channel = server_channel.split(":")
        server_channels[int(server)] = int(channel)
        logging.info(f"adding config for {server}:{channel}")


logging.info(f"Configured for {len(server_channels)} servers")

intents = discord.Intents.default()
intents.members = True
bot = discord.Bot(intents=intents)

@bot.event
async def on_member_update(before, after):
    member_server = after.guild.id
    logging.info(f"member_change on server {member_server} for user {before.nick or after.nick}")
    message = ""
    if before.nick != after.nick:
        if before.nick is None:
            message = f"Member [{str(before.name)}] changed their nickname to [{str(after.nick)}]. "
        elif after.nick is None:
            message = f"Member [{str(before.name)}] removed their nickname. "
        else:
            message = f"Member [{str(before.nick)}] changed their nickname to [{str(after.nick)}]. "
    if before.name != after.name:
        message += f"Member [{str(before.name)}] changed their name to [{str(after.name)}]."
    if message != "":
        await send_it(member_server,message)

bot.run(os.getenv('DISCORD_BOT_TOKEN'))
