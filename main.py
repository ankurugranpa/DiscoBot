import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from typing import Mapping, Optional
from bot_actions import *

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
    if message.author != bot.user:
        print(f"{message.author.display_name}: {message.content}")
    if message.author.bot or message.content.startswith(bot.command_prefix):
        return
    await get_suffix_channel(message) # 語尾DBチャンネルを取得

    await bot.process_commands(message)

# VCの滞在時間を記録
@bot.event 
async def on_voice_state_update(member, before, after):
    await record_time(member, before, after)

bot.run(TOKEN)
