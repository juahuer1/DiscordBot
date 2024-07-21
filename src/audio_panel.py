import discord
from src.utils import *

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

class AudioPanel2():
    def __init__(self):
        #self.viewer = discord.ui.View(timeout = None)
        # buttoner = AudioButtons("./Audios")
        # for button in buttoner.buttons:
        #     self.viewer.add_item(button)
        self.viewer = AudioView(timeout=None)
        self.viewer.button(path="./Audios")
        self.embed = discord.Embed(title="Panel de Control", description="Pulsa un botón para interactuar.", color=0x00ff00)

        # data = eval(self.custom_id)  # Evaluar el ID personalizado para obtener los datos originales
        # path, interaction_type = data

        # if interaction_type == "audio_panel_interaction":
        #    await interaction.response.send_message(f"Reproduciendo audio desde: {path}")