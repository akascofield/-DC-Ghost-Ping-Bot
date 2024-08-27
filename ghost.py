import discord
from discord.ext import commands
from datetime import datetime, timezone, timedelta
from discord.utils import utcnow

# YOUR DISCORD BOT TOKEN
TOKEN = 'token'

# IMPORTANT INTENTS
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True 
intents.dm_messages = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

ALLOWED_USERS = ['YOUR_USER_ID_1', 'YOUR_USER_ID_2'] # USER IDs THAT WILL NOT BE AFFECTED BY GHOST PING DETECTION

GHOST_PING_LOG_CHANNEL_ID = 1277797921424933060  # CHANNEL ID WHERE GHOST PING LOGS WILL BE SENT

@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')

@bot.event
async def on_message_delete(message):
    if not message.author.bot and str(message.author.id) not in ALLOWED_USERS:
        if message.mentions: 
            log_channel = bot.get_channel(GHOST_PING_LOG_CHANNEL_ID)
            mentioned_users = ", ".join([user.mention for user in message.mentions])

            # DISCORD EMBED
            embed = discord.Embed(
                title="**Ghostping Detected**",
                description=f"{message.author.mention}'s message containing a ping was deleted.",
                color=discord.Color(int('0xFF2D00', 16))  # HEX COLOR CODE FOR EMBED
            )

            # INFORMATION OF THE PERSON SENDING GHOST PING
            embed.set_author(name=f"{message.author.name}", icon_url=message.author.avatar.url)

            # DELETED MESSAGE DETAILs
            embed.add_field(name="Message", value=message.content or "No content", inline=False)

            # PINGED USER's
            embed.add_field(name="Ping(s)", value=mentioned_users, inline=False)

            # TIMEOUT INFORMATIONs
            embed.add_field(name="Timeout", value="5 minutes", inline=False)

            # DATE/TIME INFORMATIONs
            embed.set_footer(text="")
            embed.timestamp = discord.utils.utcnow()

            # CUSTOM THUMBNAIL PICTURE
            thumbnail_url = "https://i.imgur.com/4CgA7rk.jpeg"  # REPLACE THIS WITH YOUR IMAGE LINK
            embed.set_thumbnail(url=thumbnail_url)

            await log_channel.send(embed=embed)

            try:
                # TIMEOUT
                await message.author.timeout(utcnow() + timedelta(minutes=5)) # TIMEOUT DURATION
            except Exception as e:
                print(f"Failed to apply timeout to {message.author}: {e}")

bot.run(TOKEN)