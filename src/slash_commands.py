import discord
import random
import os
from src.utils import *
from src.thematic import *
from src.audios import *

class SetupSlashCommands():
    def setup_commands(bot):

        @bot.tree.command(name="roll", description="Tira N dados de N caras en este orden NdN (dados, caras) (Ex: /roll 3d6)")
        async def roll(interaction: discord.Interaction, times: int, faces: int):

            result = ', '.join(str(random.randint(1, faces)) for r in range(times))
            await interaction.response.send_message(result, silent = True)

        @bot.tree.command(name="joined", description="Fecha de inclusion de un miembro (Ex: /joined juanmingla)")
        async def joined(interaction: discord.Interaction, member: discord.Member):
            await interaction.response.send_message(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}', silent = True)

        @bot.tree.command(name='bot', description="Dice si el bot mola (Ex: /bot)")
        async def _bot(interaction: discord.Interaction):
            await interaction.response.send_message('Es la peripocha.', silent = True)

        @bot.tree.command(name="join", description="Agrega el bot al chat silenciosamente (Ex: /join)")
        async def join(interaction: discord.Interaction):
            if not interaction.guild.voice_client:
                connected = await AudioBot.join(interaction, silent = True)
                if(connected):
                    await interaction.response.send_message("Bot conectado al canal de voz.", silent = True)
            else:
                await interaction.response.send_message("Bot ya en el canal", silent = True)

        @bot.tree.command(name="leave", description="Elimina el bot del chat de audio (Ex: /leave)")
        async def leave(interaction: discord.Interaction):
            disconnected = await AudioBot.leave(interaction, silent = True)
            if disconnected:
                await interaction.response.send_message("Me doy el piro!", silent = True)
            else:
                await interaction.response.send_message("Bot no esta en el canal", silent = True)

        @bot.tree.command(name='audios', description="Reproduce audios en el canal en uso (Ex: /audios)")
        async def audios(interaction: discord.Interaction):
            connected = await AudioBot.join(interaction)
            if not connected:
                return
            voice_client = interaction.guild.voice_client
            view = AudioView()
            view.select("./Audios", 0)
            await interaction.response.send_message("Elige una opcion del menu:", view=view, silent = True)

        @bot.tree.command(name='cool',description="Dice si alguien mola (Ex: /cool Khrisleo)")
        async def cool(interaction: discord.Interaction, member: discord.Member):
            path = "./Imagenes/Simpsons"
            archivos = os.listdir(path=path)
            limit = len(archivos)
            result = archivos[random.randint(0, limit-1)]
            await interaction.response.send_message(file=discord.File(path+"/"+result), silent = True)

        @bot.tree.command(name='upload',description="Subir audios al servidor(Ex: /upload)")
        async def upload(interaction: discord.Interaction, audio: discord.Attachment):
            channel_obj = await IdentifyPanel.channel(interaction)

            if not channel_obj:
                return

            original_path = channel_obj.get('OriginalPath')
            base_path = channel_obj.get('BasePath')

            view = FolderView() 
            view.select(original_path, base_path, audio)
            await interaction.response.send_message("Selecciona una carpeta:", view=view, silent = True)

        @bot.tree.command(name="createfolder", description="Crear una carpeta para almacenar audios, Simpsons u Offtopic (Ex: /createfolder)")
        async def createfolder(interaction: discord.Interaction, folder: str):
            if interaction.channel.name == InitEnv.simpsons_channel_name:
                data = InitEnv.simpsons
            elif interaction.channel.name == InitEnv.offtopic_channel_name:
                data = InitEnv.offtopic
            else:
                await interaction.response.send_message("No estás en ningún audio panel", silent = True)

            if(Archive.same(folder, data["og_path"]) or Archive.same(folder, data["path"])):
                await interaction.response.send_message("Esa carpeta ya existe!", silent = True)
            else:
                os.mkdir(os.path.join(data["og_path"], folder))
                os.mkdir(os.path.join(data["path"], folder))
                await interaction.response.send_message("Carpeta creada en el servidor", silent = True)
            await AudioPanel.edit(interaction, data, 0)     

        @bot.tree.command(name="delete", description="Elimina una carpeta o archivo del servidor de Offtopic (Ex: /delete)")
        async def delete(interaction: discord.Interaction):
            data = InitEnv.offtopic

            original_path = data["og_path"]
            base_path = data["path"]

            view = AuxView()
            view.select(base_path, original_path, 0)
            await interaction.response.send_message("Selecciona una carpeta:", view=view, silent = True)

        @bot.tree.command(name="links", description="Links de ayuda para obtener y procesar los audios, etc (Ex: /links)")
        async def links(interaction: discord.Interaction):
            embed = discord.Embed(title="Links relacionados: ", description="""
                Convertidor youtube: https://yt1s.de/youtube-to-mp3?l=en \n
                Recortar audio online: https://clideo.com/es/cut-audio \n
                Recortar audio en local (permite ser mas preciso seleccionando el fragmento): https://www.audacityteam.org/download/ \n
                Enlace GitHub bot: https://github.com/juahuer1/DiscordBot
            """, color=0x00ff00)
            await interaction.response.send_message(embed=embed)

        @bot.tree.command(name='clearaudio', description="Interrumpimos audio en reproduccion (Ex: /clearaudio)")
        async def clearaudio(interaction: discord.Interaction):
            voice_client = interaction.guild.voice_client
            if voice_client:
                voice_client.stop()
                await interaction.response.send_message("Audio interrumpido", silent = True)
            else:
                await interaction.response.send_message("No hay audio reproduciendose", silent = True)
        return bot