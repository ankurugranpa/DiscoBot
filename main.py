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
    print(f"{message.author.display_name}: {message.content}")
    if message.author.bot or message.content.startswith(bot.command_prefix):
        return

    # 語尾DBチャンネルを取得
    suffix_channel = discord.utils.get(message.guild.text_channels, name="語尾db")
    print (suffix_channel)
    if suffix_channel:
        # チャンネルのメッセージを取得して語尾情報を検索
        async for msg in suffix_channel.history(limit=200):
            user_id, suffix = msg.content.split(maxsplit=1)
            print(f"ユーザーID: {user_id}, 語尾: {suffix}")
            if str(message.author.id) == user_id:
                print("登録されたユーザーが発言しました")
                new_content = f"{message.content}{suffix}"
                quote = f"> {message.content}\n{message.author.mention}: {new_content}"
                await message.channel.send(quote)
                break
    else:
        print("語尾データなし")
    # 他のコマンドも正常に動作させる
    await bot.process_commands(message)


bot.run(TOKEN)
