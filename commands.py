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
        await ctx.send('ボタンを表示します', view=button)
    
    @bot.command(description="セレクトメニューを表示します")
    async def select(ctx):
        select = Select()
        await ctx.send('セレクトメニューを表示します', view=select)
