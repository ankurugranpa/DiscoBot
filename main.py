import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from typing import Mapping, Optional

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()  
intents.messages = True
intents.guilds = True



bot = commands.Bot(command_prefix="/", intents=intents, case_insensitive=True)

from commands import setup

setup(bot)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    await bot.tree.sync()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower().startswith("hello"):
        await message.channel.send("Hello!")

    await bot.process_commands(message)


bot.run(TOKEN)
