## Bot Details

Just a bot that watches for and logs user name changes to the desired channel.

## Using the bot

clone the repo and install the necessary components. Then create and edit your .env file. You will need at the very least the DISCORD_BOT_TOKEN set in your .env

```
git clone https://github.com/atomriot/discord-user-evolution-bot.git
cd discord-user-evolution-bot/
pip install -r requirements.txt
cp .env.sample .env
nano .env
```

Now with everything in place you should be able to run the bot a few ways.

```
python ./bot/main.py
# or
python ./bot/main.py --debug 1 --cid 666
```

## To set this up as a service on a raspberry pi

Create a service file with your config:

```
sudo nano /etc/systemd/system/discord_evolution_bot.service
```

with the contents like

```
[Unit]
Description=UserEvolutionBot description
After=network.target

[Service]
User=YOUR_USER_NAME
WorkingDirectory=/home/YOUR_USER_NAME/discord-user-evolution-bot
ExecStart=/usr/bin/python3 /home/YOUR_USER_NAME/discord-user-evolution-bot/bot/main.py --debug 1 --cid 666
Restart=always

[Install]
WantedBy=multi-user.target
```

This is with the assumption that you cloned the repo into your home directory and your username is YOUR_USER_NAME. you will need to adjust your user name to be what you actually log in with as well as adjust the path.

This also runs the bot to chat to channel ID of 666 and sets debug to 1. This will enable debug logging and set the main channel. You can use command line to do this or you can set these values in the .env file. This way you an run the bot with a config for different servers if needed.

With that file in place, let enable and start the servive

```
sudo systemctl enable discord_evolution_bot.service
sudo system start discord_evolution_bot.service
```

To ensure its running you can use this to check status:

```
sudo systemctl status discord_evolution_bot.service
```
