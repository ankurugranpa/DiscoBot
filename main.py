import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents ,help_command=None)

# commands.pyからコマンドを読み込む
from commands import setup
setup(bot)

@bot.event
async def on_ready():
    print(f'Bot Name: {bot.user}')
    for server in bot.guilds:
        await bot.tree.sync(guild=discord.Object(id=server.id))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('hello'):
        await message.channel.send('Hello!', silent=True)

    await bot.process_commands(message)



bot.run(TOKEN)
