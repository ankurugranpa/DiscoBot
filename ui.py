import discord
from discord.ext  import commands

class Button(discord.ui.View):
    def __init__(self,label,style):# Button(label='ボタン', style=discord.ButtonStyle.primary)
        super().__init__()
        button = discord.ui.Button(label=label, style=style, custom_id='button:press')
        button.callback = self.on_button_press
        self.add_item(button)

    async def on_button_press(self, interaction):
        user = interaction.user.mention
        await interaction.response.send_message(f"{user}さんがボタンを押しました", silent=True)

class Select(discord.ui.View):
    def __init__(self):
        super().__init__()
        select = discord.ui.Select(placeholder='選択してください', min_values=1, max_values=1)
        select.add_option(label='選択肢1', value='1')
        select.add_option(label='選択肢2', value='2')
        select.add_option(label='選択肢3', value='3')
        select.callback = self.on_select
        self.add_item(select)

    async def on_select(self, interaction):
        user = interaction.user.mention
        await interaction.response.send_message(f"{user}さんが{interaction.data['values'][0]}を選択しました", silent=True)


class ConfirmButton(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None  

        yes_button = discord.ui.Button(
            label="YES", style=discord.ButtonStyle.success, custom_id="yes"
        )
        yes_button.callback = self.yes
        self.add_item(yes_button)

        no_button = discord.ui.Button(
            label="NO", style=discord.ButtonStyle.danger, custom_id="no"
        )
        no_button.callback = self.no
        self.add_item(no_button)

    async def yes(self, interaction):
        self.value = "YES"
        await interaction.response.defer() 
        self.stop()

    async def no(self, interaction):
        self.value = "NO"
        await interaction.response.defer()  
        self.stop()

