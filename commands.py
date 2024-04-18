import discord
from discord.ext import commands
from gtts import gTTS
import asyncio
import os

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
    
    @bot.command(description="ttsで突然しゃべります")
    async def tts(ctx, *, message):
        await ctx.send(message, tts=True)

    @bot.command(description="指定したユーザーをミュートします")
    async def mute(ctx, member: discord.Member):
        await member.edit(mute=True)
        await ctx.send(f"{member.mention}をミュートしました")
    
    @bot.command(description="指定したユーザーのミュートを解除します")
    async def unmute(ctx, member: discord.Member):
        await member.edit(mute=False)
        await ctx.send(f"{member.mention}のミュートを解除しました")

    class GTTSEngine:
        def save_speech(self, text, path):
            tts = gTTS(text=text, lang='ja', slow=False)  # 日本語で音声合成
            tts.save(path)

    async def play_speech(voice_client: discord.VoiceClient, path):
        if voice_client.is_playing():
            voice_client.stop()
        voice_client.play(discord.FFmpegPCMAudio(source=path))
        while voice_client.is_playing():
            await asyncio.sleep(1)

    @bot.command(description="ボイスチャット内で喋ります")
    async def say(ctx, *, message):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("ボイスチャンネルに参加してから再度試してください。")
                return

        tts = GTTSEngine()
        path = "speech.mp3"  # 音声ファイルの保存パス
        tts.save_speech(message, path)
        await play_speech(ctx.voice_client, path)
        os.remove(path)  # 再生後にファイルを削除