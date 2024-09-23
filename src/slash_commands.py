import discord
import random
import os
from src.utils import *
from src.thematic import *
from src.audios import *

class SetupSlashCommands():
    def setup_commands(bot):

        @bot.tree.command(name="roll", description="Tira *times* dados de *faces* caras (Ex: /roll 3 6)")
        async def roll(interaction: discord.Interaction, times: int, faces: int):

            result = ', '.join(str(random.randint(1, faces)) for r in range(times))
            await interaction.response.send_message(result, silent = True)

        @bot.tree.command(name="joined", description="Fecha de inclusión de un miembro (Ex: /joined juanmingla)")
        async def joined(interaction: discord.Interaction, member: discord.Member):
            await interaction.response.send_message(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}', silent = True)

        @bot.tree.command(name='bot', description="Dice si el bot mola (Ex: /bot)")
        async def _bot(interaction: discord.Interaction):
            await interaction.response.send_message('Es la peripocha.', silent = True)

        @bot.tree.command(name="join", description="Agrega el bot a la llamada silenciosamente (Ex: /join)")
        async def join(interaction: discord.Interaction):
            if not interaction.guild.voice_client:
                connected = await AudioBot.join(interaction, silent = True)
                if(connected):
                    await interaction.response.send_message("Bot conectado al canal de voz.", silent = True)
            else:
                await interaction.response.send_message("Bot ya en el canal", silent = True)

        @bot.tree.command(name="leave", description="Saca al bot de la llamada silenciosamente (Ex: /leave)")
        async def leave(interaction: discord.Interaction):
            disconnected = await AudioBot.leave(interaction, silent = True)
            if disconnected:
                await interaction.response.send_message("¡Me doy el piro!", silent = True)
            else:
                await interaction.response.send_message("Bot no está en el canal", silent = True)

        @bot.tree.command(name='audios', description="Reproduce audios en el canal en uso (Ex: /audios)")
        async def audios(interaction: discord.Interaction):
            data = await IdentifyPanel.channel(interaction)
            if data:
                await interaction.response.defer(thinking = True)

                if not interaction.guild.voice_client:
                    connected = await AudioBot.join(interaction, silent = data["silent"]) 
                    if not connected:
                        return
                
                voice_client = interaction.guild.voice_client
                view = AudioView()
                view.select(data["path"], 0)
                await interaction.followup.send("Elige una opción del menu:", view = view, silent = True)

        @bot.tree.command(name='cool',description="Dice si alguien mola (Ex: /cool Khrisleo)")
        async def cool(interaction: discord.Interaction, member: discord.Member):
            path = "./Imagenes/Simpsons"
            archivos = os.listdir(path)
            limit = len(archivos)
            result = archivos[random.randint(0, limit-1)]
            await interaction.response.send_message(file = discord.File(path+"/"+result), silent = True)

        @bot.tree.command(name='upload',description="Sube audios a Simpsons u Offtopic (Ex: /upload)")
        async def upload(interaction: discord.Interaction, audio: discord.Attachment):
            data = await IdentifyPanel.channel(interaction)
            if data:
                view = AuxView() 
                view.folder_select(data["og_path"], data["path"], audio, 0)
                await interaction.response.send_message(f"Selecciona una carpeta para subir {audio}:", view=view, silent = True)

        @bot.tree.command(name="create", description="Crea una carpeta en Simpsons u Offtopic (Ex: /create)")
        async def create(interaction: discord.Interaction, folder: str):
            data = await IdentifyPanel.channel(interaction)
            if data:
                if(Archive.same(folder, data["og_path"]) or Archive.same(folder, data["path"])):
                    await interaction.response.send_message("¡Esa carpeta ya existe!", silent = True)
                else:
                    os.mkdir(os.path.join(data["og_path"], folder))
                    os.mkdir(os.path.join(data["path"], folder))
                    await interaction.response.send_message("Carpeta creada en el servidor", silent = True)
                await AudioPanel.edit(interaction, data, 0)     

        @bot.tree.command(name="delete", description="Elimina una carpeta o audio (Ex: /delete)")
        async def delete(interaction: discord.Interaction):
            data = await IdentifyPanel.channel(interaction)
            if data:
                can = await Admin.developers(interaction, data)
                if can:
                    view = AuxView()
                    view.remove_select(data["path"], data["og_path"], 0)
                    await interaction.response.send_message("Selecciona una carpeta:", view=view, silent = True)

        @bot.tree.command(name="links", description="Colección de links de interés (Ex: /links)")
        async def links(interaction: discord.Interaction):
            embed = discord.Embed(title="Links relacionados:", description="""
                Convertidor youtube: https://yt1s.de/youtube-to-mp3?l=en\n
                Recortar audio online: https://clideo.com/es/cut-audio\n
                Recortar audio en local (permite ser mas preciso seleccionando el fragmento): https://www.audacityteam.org/download/\n
                Enlace GitHub bot: https://github.com/juahuer1/DiscordBot
            """, color=0x00ff00)
            await interaction.response.send_message(embed=embed, silent = True)

        @bot.tree.command(name="infoaudios", description="Proporciona algo de información acerca de los audios subidos (Ex: /infoaudios)")
        async def infoaudios(interaction: discord.Interaction):
            folder_paths = [InitEnv.simpsons_base_path, InitEnv.offtopic_base_path]
            data = Archive.info_audios(folder_paths)
            simpsons_data = data[0]
            offtopic_data = data[1]

            await interaction.response.send_message(f"Panel de Los Simpsons cuenta con {simpsons_data['folders']} carpetas y {simpsons_data['files']} audios, Panel de Offtopic cuenta con {offtopic_data['folders']} carpetas y {offtopic_data['files']} audios.", silent=True)

        @bot.tree.command(name='clearaudio', description="Interrumpimos audio en reproducción (Ex: /clearaudio)")
        async def clearaudio(interaction: discord.Interaction):
            voice_client = interaction.guild.voice_client
            if voice_client:
                voice_client.stop()
                await interaction.response.send_message("Audio interrumpido", silent = True)
            else:
                await interaction.response.send_message("No hay audio reproduciendose", silent = True)

        @bot.tree.command(name = "clear", description = "Limpia el canal (Ex: /clear)")
        async def clear(interaction: discord.Interaction):
            data = await IdentifyPanel.channel(interaction)
            if data:
                await interaction.response.defer(thinking = True)
                await Clear.this_channel(interaction)

        return bot #indica que se acabó esto de los comandos