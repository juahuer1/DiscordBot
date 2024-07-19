import discord
from discord.ext import commands
from discord import Interaction
from src.utils import AudioBot

# purple, green, gray

class AudioPanel(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="Homer", style=discord.ButtonStyle.blurple)
    async def homer(self, interaction: discord.Interaction, button:discord.ui.Button):
        # await interaction.response.send_message('click...', ephemeral=False)    
          
        path = "./Audios/Homer"
        await AudioBot.play_audio(interaction, path, self.bot)

        self.value = True
        self.stop()

    @discord.ui.button(label="Audios1", style=discord.ButtonStyle.grey)
    async def audios1(self, interaction: discord.Interaction, button:discord.ui.Button):
        await interaction.response.send_message('click...', ephemeral=False)
        self.value = True
        self.stop()


    @discord.ui.button(label="Audios3", style=discord.ButtonStyle.gray)
    async def audios3(self, interaction: discord.Interaction, button:discord.ui.Button):
        await interaction.response.send_message('click...', ephemeral=False)
        self.value = True
        self.stop()

    
    @discord.ui.button(label="Audios4", style=discord.ButtonStyle.green)
    async def audios4(self, interaction: discord.Interaction, button:discord.ui.Button):
        await interaction.response.send_message('click...', ephemeral=False)
        self.value = True
        self.stop()

        
    @discord.ui.button(label="Audios5", style=discord.ButtonStyle.red)
    async def audios5(self, interaction: discord.Interaction, button:discord.ui.Button):
        await interaction.response.send_message('click...', ephemeral=False)
        self.value = True
        self.stop()