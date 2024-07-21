import discord
from src.utils import AudioBot

# purple, green, gray

class AudioPanel(discord.ui.View):

    async def send_fixed_message(channel):
        embed = discord.Embed(title="Panel de Control", description="Pulsa un botón para interactuar.", color=0x00ff00)

        view = discord.ui.View()

        path = "./Audios/Homer"
        interaction_type = "audio_panel_interaction"
        data = [path,interaction_type]

        view.add_item(discord.ui.Button(label="Homer", style=discord.ButtonStyle.primary, custom_id=str(data)))

        return embed, view

class AudioPanel2(discord.ui.View):
    def __init__(self):
        #if discord.Guild.get_channel() == None
        super().__init__(timeout = None)
        buttons = discord.ui.Button(label = "A1", style = discord.ButtonStyle.primary)
        self.add_item(buttons)