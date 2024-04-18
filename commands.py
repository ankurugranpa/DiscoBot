from discord.ext import commands
from discord import app_commands
import discord

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