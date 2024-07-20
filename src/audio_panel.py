import discord
from discord.ext import commands
from discord import Interaction
from src.utils import AudioBot

# purple, green, gray

class AudioPanel(discord.ui.View):
    # def __init__(self, bot):
    #     super().__init__(timeout=None)
    #     self.value = None
    #     self.bot = bot

    async def send_fixed_message(channel):
        embed = discord.Embed(title="Panel de Control", description="Pulsa un botón para interactuar.", color=0x00ff00)

        view = discord.ui.View()

        path = "./Audios/Homer"
        interaction_type = "audio_panel_interaction"
        data = [path,interaction_type]
#       await AudioBot.play_audio(interaction, path, self.bot)

        view.add_item(discord.ui.Button(label="Homer", style=discord.ButtonStyle.primary, custom_id=str(data)))
        # view.add_item(discord.ui.Button(label="Botón 2", style=discord.ButtonStyle.secondary, custom_id="button_2"))
         # await interaction.response.send_message('click...', ephemeral=False)  
        # Enviar el mensaje
        # message = await channel.send(embed=embed, view=view)
        # self.stop()
        return embed, view

    # @discord.ui.button(label="Homer", style=discord.ButtonStyle.blurple)
    # async def homer(self, interaction: discord.Interaction, button:discord.ui.Button):
    #     # await interaction.response.send_message('click...', ephemeral=False)    
          
    #     path = "./Audios/Homer"
    #     await AudioBot.play_audio(interaction, path, self.bot)

    #     self.value = True
    #     self.stop()

    # @discord.ui.button(label="Audios1", style=discord.ButtonStyle.grey)
    # async def audios1(self, interaction: discord.Interaction, button:discord.ui.Button):
    #     await interaction.response.send_message('click...', ephemeral=False)
    #     self.value = True
    #     self.stop()


    # @discord.ui.button(label="Audios3", style=discord.ButtonStyle.gray)
    # async def audios3(self, interaction: discord.Interaction, button:discord.ui.Button):
    #     await interaction.response.send_message('click...', ephemeral=False)
    #     self.value = True
    #     self.stop()

    
    # @discord.ui.button(label="Audios4", style=discord.ButtonStyle.green)
    # async def audios4(self, interaction: discord.Interaction, button:discord.ui.Button):
    #     await interaction.response.send_message('click...', ephemeral=False)
    #     self.value = True
    #     self.stop()

        
    # @discord.ui.button(label="Audios5", style=discord.ButtonStyle.red)
    # async def audios5(self, interaction: discord.Interaction, button:discord.ui.Button):
    #     await interaction.response.send_message('click...', ephemeral=False)
    #     self.value = True
    #     self.stop()