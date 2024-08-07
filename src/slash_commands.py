import discord
import random
import os
from src.utils import *
from dotenv import load_dotenv


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
            view.select("./Audios")
            await interaction.response.send_message("Elige una opcion del menu:", view=view)


        @bot.tree.command(name='cool',description="Dice si alguien chola (Ex: /cool Khrisleo)")
        async def cool(interaction: discord.Interaction, member: discord.Member):
            path = "./Imagenes"
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
            await interaction.response.send_message("Selecciona una carpeta:", view=view) #Sacarlo al command


        @bot.tree.command(name="mkdir", description="Crear una carpeta para almacenar audios, Simpsons u Offtopic (Ex: /mkdir)")
        async def mkdir(interaction: discord.Interaction, folder: str):
            
            channel_obj = await IdentifyPanel.channel(interaction)

            if not channel_obj:
                return
            
            original_path = channel_obj.get('OriginalPath')
            base_path = channel_obj.get('BasePath')

            og_full_path = os.path.join(original_path,folder)
            base_full_path = os.path.join(base_path,folder)

            if(not Archive.same(folder, original_path) or not Archive.same(folder, base_path)):
                os.mkdir(og_full_path)
                os.mkdir(base_full_path)
                await interaction.response.send_message("Carpeta creada en el servidor")
            else:
                await interaction.response.send_message("Esa carpeta ya existe!")       


        @bot.tree.command(name='clearaudio', description="Interrumpimos audio en reproduccion (Ex: /clearaudio)")
        async def clearaudio(interaction: discord.Interaction):
            voice_client = interaction.guild.voice_client
            if voice_client:
                voice_client.stop()
                await interaction.response.send_message("Audio interrumpido")
            else:
                await interaction.response.send_message("No hay audio reproduciendose") 
        return bot