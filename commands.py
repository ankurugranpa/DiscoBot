from discord.ext import commands
from discord import app_commands
import discord
from ui import *


def setup(bot):
    
    bot.remove_command('help')

    @bot.command(description="pingを返します")
    async def ping(ctx):
        latency = bot.latency
        await ctx.send(f'Latency: {(latency * 1000):.2f}ms')

    @bot.command(description="これです")
    async def help(ctx):
        help_message = "```"
        sorted_commands = sorted(bot.commands, key=lambda x: x.name)
        for command in sorted_commands:
            help_message += f"!{command.name}: {command.description}\n"
        help_message += "```"
        embed = discord.Embed(title="コマンド一覧(アルファベット順)" ,color=0x00ff00 ,description=help_message)
        await ctx.send(embed=embed)

    @bot.command(description="ボタンを表示します")
    async def button(ctx):
        button = Button()
        await ctx.send('', view=button ,silent=True)  
    
    @bot.command(description="セレクトメニューを表示します")
    async def select(ctx):
        select = Select()
        await ctx.send('', view=select ,silent=True)

    @bot.command(description="ボイスチャンネルに入室します")
    async def join(ctx):
        if ctx.author.voice is None:
            await ctx.send("ボイスチャンネルに参加してから再度試してください。")
        else:
            channel = ctx.author.voice.channel
            if ctx.voice_client is not None:
                await ctx.send("既にボイスチャンネルに入室しています。")
            else:
                await channel.connect()

    @bot.command(description="ボイスチャンネルから退出します")
    async def leave(ctx):
        if ctx.voice_client is None:
            await ctx.send("ボイスチャンネルに参加していません。")
        else:
            await ctx.voice_client.disconnect()