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
            await interaction.response.send_message(result)

        @bot.tree.command(name="joined", description="Fecha de inclusion de un miembro (Ex: /joined juanmingla)")
        async def joined(interaction: discord.Interaction, member: discord.Member):
            await interaction.response.send_message(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


        @bot.tree.command(name='bot', description="Mola mi bot u que? (Ex: /bot)")
        async def _bot(interaction: discord.Interaction):
            await interaction.response.send_message('Es la peripocha.')


        @bot.tree.command(name="join", description="Agrega el bot al chat (Ex: /join)")
        async def join(interaction: discord.Interaction):
            if not interaction.guild.voice_client:
                connected = await AudioBot.join(interaction, silent = True)
                if(connected):
                    await interaction.response.send_message("Bot conectado al canal de voz.")
            else:
                await interaction.response.send_message("Bot ya en el canal")


        @bot.tree.command(name="leave", description="Elimina el bot del chat (Ex: /leave)")
        async def leave(interaction: discord.Interaction):
            disconnected = await AudioBot.leave(interaction, silent = True)
            if disconnected:
                await interaction.response.send_message("Maria excluida, Sergio excluido, PiBot, me gusta como juegas, por eso me cuesta tanto excluirte.")
            else:
                await interaction.response.send_message("Bot no esta en el canal")


        @bot.tree.command(name='audios', description="Reproduce audios en el canal en uso (Ex: /audios)")
        async def audios(interaction: discord.Interaction):
            connected = await AudioBot.join(interaction)
            if not connected:
                return
            voice_client = interaction.guild.voice_client
            view = AudioView()
            view.select("./Audios", 0)
            await interaction.response.send_message("Elige una opcion del menu:", view=view)


        @bot.tree.command(name='cool',description="Dice si alguien chola (Ex: /cool Khrisleo)")
        async def cool(interaction: discord.Interaction, member: discord.Member):
            path = "./Imagenes/Simpsons"
            archivos = os.listdir(path=path)
            limit = len(archivos)
            result = archivos[random.randint(0, limit-1)]
            await interaction.response.send_message(file=discord.File(path+"/"+result))


        @bot.tree.command(name='upload',description="Subir audios al servidor")
        async def upload(interaction: discord.Interaction, audio: discord.Attachment):
            
            channel_obj = await IdentifyPanel.channel(interaction)

            if not channel_obj:
                return

            original_path = channel_obj.get('OriginalPath')
            base_path = channel_obj.get('BasePath')

            view = FolderView() 
            view.select(original_path, base_path, audio)
            await interaction.response.send_message("Selecciona una carpeta:", view=view)


        @bot.tree.command(name="createfolder", description="Crear una carpeta para almacenar audios, Simpsons u Offtopic (Ex: /mkdir)")
        async def createfolder(interaction: discord.Interaction, folder: str):
            data = InitEnv()
            if interaction.channel.name == data.simpsons_channel_name:
                data = data.simpsons
            elif interaction.channel.name == data.offtopic_channel_name:
                data = data.offtopic
            else:
                await interaction.response.send_message("No estás en ningún audio panel")

            if(Archive.same(folder, data["og_path"]) or Archive.same(folder, data["path"])):
                await interaction.response.send_message("Esa carpeta ya existe!")
            else:
                os.mkdir(os.path.join(data["og_path"], folder))
                os.mkdir(os.path.join(data["path"], folder))
                await interaction.response.send_message("Carpeta creada en el servidor")
            await AudioPanel.edit(interaction, data, 0)     

        @bot.tree.command(name="deletefolder", description="Elimina una carpeta del servidor de Offtopic")
        async def deletefolder(interaction: discord.Interaction):
            data = InitEnv()
            data = data.offtopic

            original_path = data["og_path"]
            base_path = data["path"]

            view = FolderView()
            view.selectRemove(original_path, base_path)
            await interaction.response.send_message("Selecciona una carpeta:", view=view)

        @bot.tree.command(name='clearaudio', description="Interrumpimos audio en reproduccion (Ex: /clearaudio)")
        async def clearaudio(interaction: discord.Interaction):
            voice_client = interaction.guild.voice_client
            if voice_client:
                voice_client.stop()
                await interaction.response.send_message("Audio interrumpido")
            else:
                await interaction.response.send_message("No hay audio reproduciendose") 
        return bot