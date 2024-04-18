import discord
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio
from dateutil.parser import parse
from gtts import gTTS ,lang
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
            help_message += f"!{command.name}: {command.description}\n\n"
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
        def save_speech(self, text, lang_code, path):
            tts = gTTS(text=text, lang=lang_code, slow=False)
            tts.save(path)

    async def play_speech(voice_client: discord.VoiceClient, path):
        if voice_client.is_playing():
            voice_client.stop()
        voice_client.play(discord.FFmpegPCMAudio(source=path))
        while voice_client.is_playing():
            await asyncio.sleep(1)

    @bot.command(description="ボイスチャンネル内で言語に応じて喋ります")
    async def say(ctx, lang_code: str, *, message: str):
        was_connected = ctx.voice_client is not None  # ボットが既に接続されているかをチェック
        supported_langs = lang.tts_langs()  # gttsがサポートする言語のリストを取得

        if not was_connected:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("ボイスチャンネルに参加してから再度試してください。")
                return

        if lang_code not in supported_langs:
            await ctx.send("サポートされていない言語です。")
            return

        tts = GTTSEngine()
        path = f"speech_{lang_code}.mp3"  # 言語ごとにファイル名を設定
        tts.save_speech(message, lang_code, path)
        await play_speech(ctx.voice_client, path)
        os.remove(path)  # 再生後にファイルを削除

        if not was_connected:
            await ctx.voice_client.disconnect()  # ボットが元々接続されていなかった場合、切断します
    
    @bot.command(description="VC対応言語の一覧を表示します")
    async def langlist(ctx):
        with open('languagelist.txt', 'rb') as file:
            await ctx.send("対応言語一覧\nSupported Languages", file=discord.File(file, 'languagelist.txt'))

    @bot.command(description="指定したメッセージに指定したリアクションをつけます")
    async def react(ctx, message_id: int, reaction: str):
        message = await ctx.fetch_message(message_id)
        await message.add_reaction(reaction)

    # !vote 5 と入力すると、5種類のリアクションがついたメッセージが生成されます
    @bot.command(description="N個の選択肢がある投票を作成します !vote N")
    async def vote(ctx, num: str):
        try:
            num = int(num)
            if num < 2 or num > 10:
                await ctx.send("選択肢は2〜10個までです😡")
                return
            message = await ctx.send("投票")
            for i in range(1, num + 1):
                await message.add_reaction(f"{i}\u20e3")
        except ValueError:
            await ctx.send("選択肢の数は整数で指定してください😡")
        except Exception as e:
            await ctx.send(e)

    @bot.command(description="指定したユーザーにDMを送信します")
    async def dm(ctx, member: discord.Member, *, message):
        await member.send(message)
        await ctx.send("DMを送信しました")

    @bot.command(description="イベントを作成します YYYY-MM-DD HH:MM イベント名 ?VC名")
    async def event(ctx, date: str, time: str, event_name: str, channel_name: str = None):
        if ctx.author.voice is None and channel_name is not None:
            channel_id = discord.utils.get(ctx.guild.voice_channels, name=channel_name).id
        elif ctx.author.voice is not None:
            channel_id = ctx.author.voice.channel.id
        else:
            await ctx.send("ボイスチャンネル名を指定するか、ボイスチャンネルに参加してください。")
            return
        date_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M").astimezone()
        channel = ctx.guild.get_channel(channel_id)
        print(date_time, channel)
        try:
            await ctx.guild.create_scheduled_event(name=event_name,description="Botにより作成",start_time=date_time,entity_type=discord.EntityType.voice,channel=channel,privacy_level=discord.PrivacyLevel.guild_only)
            await ctx.send("イベントを作成しました")

        except Exception as e:
            await ctx.send(e)


