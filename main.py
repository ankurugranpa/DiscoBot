import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents ,help_command=None)

class Button(discord.ui.View):
    def __init__(self):
        super().__init__()
        button = discord.ui.Button(label='Press Me', style=discord.ButtonStyle.primary, custom_id='button:press')
        button.callback = self.on_button_press
        self.add_item(button)

    async def on_button_press(self, interaction):
        user = interaction.user
        await interaction.response.send_message(f"{user}さんがボタンを押しました", silent=True)

@bot.event
async def on_ready():
    bot.tree.clear_commands(guild=None)
    await bot.tree.sync(guild=None)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('hello'):
        view = Button()
        await message.channel.send('Hello!', silent=True, view=view)

    await bot.process_commands(message)

# commands.pyからコマンドを読み込む
from commands import setup
setup(bot)

bot.run(TOKEN)
