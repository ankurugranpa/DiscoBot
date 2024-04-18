import discord

class Button(discord.ui.View):
    def __init__(self):
        super().__init__()
        button = discord.ui.Button(label='Press Me', style=discord.ButtonStyle.primary, custom_id='button:press')
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
