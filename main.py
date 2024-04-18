# This example requires the 'message_content' intent.

import discord
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

class Button(discord.ui.View):
    def __init__(self):
        super().__init__()
        button = discord.ui.Button(label='Press Me', style=discord.ButtonStyle.primary, custom_id='button:press')
        button.callback = self.on_button_press  # ボタンのコールバックを設定
        self.add_item(button)

    async def on_button_press(self, interaction):
        user = interaction.user
        await interaction.response.send_message(f"{user}さんがボタンを押しました",silent=True)  # ボタンが押されたときの応答



@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hello'):
        view = Button()
        await message.channel.send('Hello!',silent=True, view=view)
    


client.run(TOKEN)
