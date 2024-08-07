import discord
import os
import asyncio
from discord import FFmpegPCMAudio
import random
import numpy as np
from dotenv import load_dotenv
from pydub import AudioSegment, effects  


class AudioSelect(discord.ui.Select):
    def __init__(self, path):
        self.path = path
        # archivos = os.listdir(path)
        archivos_filtered = Archive.files(path)
        options = []
        
        for archivo in archivos_filtered: #Aquí el límite también es 25 creo
            nombre = Archive.nice_name(archivo)
            option = discord.SelectOption(label = nombre, value = archivo)
            options.append(option)
        
        super().__init__(placeholder="Elige una opcion...", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        audio_selected = self.values[0]

        await interaction.response.defer()
        AudioSound(audio_selected, self.path, interaction)
         
class AudioView(discord.ui.View):
    def __init__(self, timeout = 180):
        super().__init__(timeout = timeout)

    def select(self, path):
        self.add_item(AudioSelect(path))

    def button(self, path):
        carpetas = os.listdir(path)
        for carpeta in carpetas:
            self.add_item(AudioButton(f"{carpeta}", path))

class AudioBot:
    async def join (interaction: discord.Interaction, silent = False):
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            await channel.connect()
            await interaction.client.change_presence(status = discord.Status.online, activity = discord.CustomActivity(name = "Cocinando memes"))           
            data = InitEnv()
            path = os.path.join(data.simpsons_base_path, 'Saludos')
            saluditos = os.listdir(path)
            if(not silent):
                AudioSound(saluditos, path, interaction)
            return True
        else:
            await interaction.followup.send("Bot no se puede unir, metete en un canal de audio!")
            return False

    async def leave (interaction: discord.Interaction, silent = False):
        if interaction.guild.voice_client:
            data = InitEnv()
            path = os.path.join(data.simpsons_base_path, 'Despedidas')
            despediditas = os.listdir(path)
            if(not silent):
                AudioSound(despediditas, path, interaction)
                while interaction.guild.voice_client.is_playing():
                    await asyncio.sleep(1)
            await interaction.guild.voice_client.disconnect()
            await interaction.client.change_presence(status = discord.Status.idle, activity = discord.CustomActivity(name = "Hateando las nuevas temporadas"))
            return True
        else:
            return False
  
class Archive:
    def nice_name(file):
        file = os.path.basename(file)
        file = file.removesuffix(".mp3")
        file = list(file.split("-"))
        name = ' '.join(file)
        return name

    def directories(path):
        folders = []
        files = os.listdir(path)

        for file in files:
            if (file.rsplit('.', 1)[-1] == file):
                folders.append(file)
        return folders

    def files(path):
        output = []
        files = os.listdir(path)

        for file in files:
            if (file.rsplit('.', 1)[-1] != file):
                output.append(file)
            else:        
                second_files = os.listdir(os.path.join(path,file))
                for last_file in second_files:
                    if (last_file.rsplit('.', 1)[-1] != last_file):
                        output.append(os.path.join(file,last_file))
        return output

    def same(file, path):
        status = False
        if (file.rsplit('.', 1)[-1] == file):
            folders = Archive.directories(path)
            for my_folder in folders:
                if (os.path.basename(my_folder) == file):
                    status = True
            
            return status
        elif (file.rsplit('.', 1)[-1] != file):
            files = Archive.files(path) #se hace así?
            for my_file in files:
                if (os.path.basename(my_file) == file):
                    status = True
            
            return status

class AudioButton(discord.ui.Button):
    def __init__(self, label, path):
        super().__init__(label=label, style=discord.ButtonStyle.blurple)
        self.path = path

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await Clear.this_channel(interaction)
        if not interaction.guild.voice_client:
            connected = await AudioBot.join(interaction) 
            if not connected:
                return

        view = AudioView()
        view.select(self.path+"/"+self.label)
        await interaction.followup.send(view = view)

class FirstButton(discord.ui.Button):
    def __init__(self, label):
        if label == "Aleatorio":
            colour = discord.ButtonStyle.green
        if label == "Anteriores":
            colour = discord.ButtonStyle.grey
        super().__init__(label = label, style = colour)

    async def callback(self, interaction: discord.Interaction): #editar mensaje usando m_panel??
        await interaction.response.defer()
        await Clear.this_channel(interaction)
        if self.label == "Aleatorio":
            data = InitEnv()

            files = os.listdir(data.simpsons_base_path)
            audios = Archive.files(path = data.simpsons_base_path)
            if not interaction.guild.voice_client:
                connected = await AudioBot.join(interaction)
                if not connected:
                    return

                await interaction.followup.send("El siguiente prometo que será aleatorio")
            else:
                AudioSound(audios, data.simpsons_base_path, interaction)

class LastButton(discord.ui.Button): #Ponerle límite para que en la última iteración no salga
    def __init__(self):
        super().__init__(label = "Siguientes", style = discord.ButtonStyle.grey)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("¡Marge, no quedan más audios!")

class StopButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label = "Stop", style = discord.ButtonStyle.red)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await Clear.this_channel(interaction)
        await AudioBot.leave(interaction)

class AudioPanel():
    def __init__(self): #voy a tener que añadir variable n para controlar cuántas iteraciones llevamos
                        #settear el de events en n = 0
        self.viewer = AudioView(timeout=None)

        data = InitEnv()

        files = os.listdir(data.simpsons_base_path)
        self.viewer.add_item(FirstButton("Aleatorio"))

        self.viewer.button(data.simpsons_base_path)

        self.viewer.add_item(StopButton())

        self.file = discord.File("./Imagenes/moe_al_habla.jpg", filename="moe_al_habla.jpg")

        self.embed = discord.Embed(title="Bar de Moe, Moe al habla", description="*Señor Reves? de nombre Stal*, \n Un momento, A VEEER STAL REVES, alguno de ustedes Stal Reves?", color=0x00ff00)
        self.embed.set_image(url="attachment://moe_al_habla.jpg")

class AudioSound():
    def __init__(self, file, path, interaction: discord.Interaction):
        if type(file) is list:
            playing = file[random.randint(0,len(file)-1)]
        else:
            playing = file
        interaction.guild.voice_client.play(FFmpegPCMAudio(path+"/"+playing))

class Clear():
    async def this_channel(interaction):
        data = InitEnv()
        this_channel = discord.utils.get(interaction.guild.channels, name = data.simpsons_channel_name) 
        messages = [message async for message in this_channel.history(oldest_first = True)]
        my_message = messages[0]
        await this_channel.purge(after = my_message)

class FolderSelect(discord.ui.Select):
    def __init__(self, original_path, base_path, audio):
        self.original_path = original_path
        self.base_path = base_path
        self.audio = audio
        folders = os.listdir(original_path)
        options = []

        for folder in folders:
            option = discord.SelectOption(label = folder, value = folder)
            options.append(option)

        super().__init__(placeholder="Elige una opcion...", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        folder_selected = self.values[0]
        audios_path = os.path.join(self.original_path, folder_selected, self.audio.filename)

        if(Archive.same(self.audio.filename, os.path.join(self.original_path, folder_selected)) or Archive.same(self.audio.filename, os.path.join(self.base_path, folder_selected))):
            await interaction.followup.send('Ya existe un archivo con ese nombre!')
            return

        await self.audio.save(fp=audios_path)

        full_base_path = os.path.join(self.base_path, folder_selected, self.audio.filename)
        rawsound = AudioSegment.from_file(audios_path, "mp3")  
        normalizedsound = effects.normalize(rawsound)
        normalizedsound.export(full_base_path, format="mp3")

        await interaction.followup.send(f'Archivo de audio {self.audio.filename} ha sido guardado exitosamente.')
         
class FolderView(discord.ui.View):
    def __init__(self, timeout = 180):
        super().__init__(timeout = timeout)

    def select(self, original_path, base_path, audio):
        self.add_item(FolderSelect(original_path, base_path, audio))

class InitEnv():
    def __init__(self):
        load_dotenv()
        self.simpsons_channel_name = os.getenv('SIMPSONSCHANNELNAME')
        self.offtopic_channel_name = os.getenv('OFFTOPICCHANNELNAME')

        self.simpsons_og_base_path = os.getenv('SIMPSONSORIGINALPATH')
        self.simpsons_base_path = os.getenv('SIMPSONSPATH')
        self.offtopic_og_base_path = os.getenv('SIMPSONSORIGINALPATH')
        self.offtopic_base_path = os.getenv('SIMPSONSPATH')

class IdentifyPanel():
    async def channel(interaction):
        data = InitEnv()
        result = {}

        if(interaction.channel.name == data.simpsons_channel_name):
            result['OriginalPath'] = data.simpsons_og_base_path
            result['BasePath'] = data.simpsons_base_path
            return result

        elif(interaction.channel.name == data.offtopic_channel_name):
            result['OriginalPath'] = data.offtopic_og_base_path
            result['BasePath'] = data.offtopic_base_path
            return result

        else:
            await interaction.response.send_message("No estás en ningún audio panel")
            return False
