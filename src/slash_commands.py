import discord
from discord import FFmpegPCMAudio
from discord.ui import Select, View
from discord.ext import commands
import random
import os

from src.utils import *

class SetupSlashCommands():
    def setup_commands(bot):
        # Define un comando de barra (slash command)
        @bot.tree.command(name="add", description="Suma dos numeros (Ex: /add 5 11)")
        async def add(interaction: discord.Interaction, left: int, right: int):
            result = left + right
            await interaction.response.send_message(str(result))

            
        @bot.tree.command(name="roll", description="Tira N dados de N caras en este orden NdN (dados, caras) (Ex: /roll 3d6)")
        async def roll(interaction: discord.Interaction, dice: str):
            try:
                rolls, limit = map(int, dice.split('d'))
            except Exception:
                await interaction.response.send_message('Format has to be in NdN!')
                return

            result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
            await interaction.response.send_message(result)


        @bot.tree.command(name="choose",description='Elige al azar entre varias opciones (Ex: /choose Pizza Pasta Hamburguesa)')
        async def choose(interaction: discord.Interaction, choices: str):
            chosen = random.choice(choices.split())
            await interaction.response.send_message(chosen)


        @bot.tree.command(name="repeat", description="Repite lo mismo muchas veces (Ex: /repeat 5 Feo)")
        async def repeat(interaction: discord.Interaction, times: int, content: str):
            # Respondemos con la primera instancia del contenido para cumplir con las reglas de interacción
            await interaction.response.send_message(content)
            
            # Luego usamos followup para enviar las repeticiones restantes
            for _ in range(times - 1):  # Ya hemos enviado el primer mensaje, por lo que restamos 1
                await interaction.followup.send(content)


        @bot.tree.command(name="joined", description="Fecha de inclusion de un miembro (Ex: /joined juanmingla)")
        async def joined(interaction: discord.Interaction, member: discord.Member):
            await interaction.response.send_message(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


        @bot.tree.command(name='bot', description="Mola mi bot u que? (Ex: /bot)")
        async def _bot(interaction: discord.Interaction):
            await interaction.response.send_message('Es la peripocha.')


        @bot.tree.command(name="join", description="Agrega el bot al chat (Ex: /join)")
        async def join(interaction: discord.Interaction):
            if not interaction.guild.voice_client:
                connected = await JoinBot.join_audio_channel(interaction, bot)
                if(connected):
                    await interaction.response.send_message("Bot conectado al canal de voz.")
            else:
                await interaction.response.send_message("Bot ya en el canal")


        @bot.tree.command(name="leave", description="Elimina el bot del chat (Ex: /leave)")
        async def leave(interaction: discord.Interaction):
            if interaction.guild.voice_client:
                await interaction.guild.voice_client.disconnect()
                await bot.change_presence(status = discord.Status.idle, activity = discord.CustomActivity(name = "Hateando las nuevas temporadas"))
                await interaction.response.send_message("El putisimo Bot se pira")
            else:
                await interaction.response.send_message("Bot no esta en el canal")


        @bot.tree.command(name='audios', description="Reproduce audios en el canal en uso (Ex: /audios)")
        async def audios(interaction: discord.Interaction):
            voice_client = interaction.guild.voice_client
            if not voice_client:
                connected = await JoinBot.join_audio_channel(interaction,bot)
                if not connected:
                    return
                voice_client = interaction.guild.voice_client  # Actualiza el cliente de voz

            audio_player = AudioPlayer(voice_client) 
            path = "./Audios" 
            view = AudioView(audio_player, path)  
            await interaction.response.send_message("Elige una opcion del menu:", view=view)

        @bot.tree.command(name='cool',description="Dice si alguien chola (Ex: /cool Khrisleo)")
        async def cool(interaction: discord.Interaction, member: discord.Member):
            path = "./Imagenes"
            archivos = os.listdir(path=path)
            limit = len(archivos)
            result = archivos[random.randint(0, limit-1)]
            await interaction.response.send_message(file=discord.File(path+"/"+result))

        

        @bot.tree.command(name='clearaudio', description="Interrumpimos audio en reproduccion (Ex: /clearaudio)")
        async def clearaudio(interaction: discord.Interaction):
            voice_client = interaction.guild.voice_client
            if voice_client:
                voice_client.stop()
                await interaction.response.send_message("Audio interrumpido")
            else:
                await interaction.response.send_message("No hay audio reproduciendose") 
        return bot