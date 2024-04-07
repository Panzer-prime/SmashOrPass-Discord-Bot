import os
import requests
from dotenv import load_dotenv
from discord import Intents, Message, Client

from discord.ext import commands
from discord.emoji import Emoji
load_dotenv()

TOKEN: str = os.getenv('DISCORD_TOKEN') 

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)
bot = commands.Bot(command_prefix='?', intents=intents)


async def get_waifu_image():
    """Fetches a random waifu image from the waif.im API."""
    url = 'https://api.waifu.im/search'
    params = {
        "is_nsfw": "False",
        'height': '>=2000',
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status() 
        data = response.json()
        return data['images'][0]['url']  
    except requests.exceptions.RequestException as e:
        print(f"Error fetching waifu image: {e}")
        return None

@client.event
async def on_message(message):
   
    if message.author == client.user:
        return  

    if message.content.lower() == "hello":
      await message.channel.send(f"Hello, {message.author}!")  # Send response message

@bot.command()
async def waifu(ctx):
    emoji = '\N{THUMBS UP SIGN}'
    pass_emoji = '\N{THUMBS DOWN SIGN}'
    image_url = await get_waifu_image()
    print(image_url)
    if image_url:
        message = await ctx.send(image_url)  # Send message and store it
        await message.add_reaction(emoji) 
        await message.add_reaction(pass_emoji)
    else:
        await ctx.send("Failed to retrieve a waifu image.")


# Removed button command as interactive buttons are not supported
bot.run(TOKEN)
client.run(TOKEN)  # Run the bot using the token
