import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()  # 必要なIntentのみを有効化
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="/", intents=intents, help_command=None)

# commands.pyからapp_commandsを使ったコマンドを読み込む
from commands import setup

setup(bot)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    # 全てのサーバーに対してコマンドを同期する
    await bot.tree.sync()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower().startswith("hello"):
        await message.channel.send("Hello!")

    # app_commandsと従来のコマンドを正しく処理
    await bot.process_commands(message)


bot.run(TOKEN)
