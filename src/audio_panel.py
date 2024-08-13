import discord
from src.utils import *

# purple, green, gray

class AudioPanel2():
    def __init__(self):
        self.viewer = AudioView(timeout=None)
        self.viewer.button(path="./Audios")
        self.file = discord.File("./Imagenes/moe_al_habla.jpg", filename="moe_al_habla.jpg")

        self.embed = discord.Embed(title="Bar de Moe, Moe al habla", description="*Señor Reves? de nombre Stal*, \n Un momento, A VEEER STAL REVES, alguno de ustedes Stal Reves?", color=0x00ff00)
        self.embed.set_image(url="attachment://moe_al_habla.jpg")
