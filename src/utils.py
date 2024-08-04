import discord
import os
import asyncio
from discord import FFmpegPCMAudio
import random
import numpy as np
import soundfile as sf

class AudioSelect(discord.ui.Select):
    def __init__(self, path):
        self.path = path
        archivos = os.listdir(path)
        archivos_filtered = NiceNames.directories(archivos, path)
        options = []
        
        for archivo in archivos_filtered: #Aquí el límite también es 25 creo
            nombre = NiceNames.file(archivo)
            option = discord.SelectOption(label = nombre[1], value = archivo)
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
    async def join (interaction: discord.Interaction):
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            await channel.connect()
            await interaction.client.change_presence(status = discord.Status.online, activity = discord.CustomActivity(name = "Cocinando memes"))
            
            saluditos = os.listdir("./Audios/Saludos")
            AudioSound(saluditos, "./Audios/Saludos", interaction)
            return True
        else:
            await interaction.response.send_message("Bot no se puede unir, metete en un canal de audio!")
            return False

    async def leave (interaction: discord.Interaction):
        if interaction.guild.voice_client:
            despediditas = os.listdir("./Audios/Despedidas")
            AudioSound(despediditas, "./Audios/Despedidas", interaction)
            while interaction.guild.voice_client.is_playing():
                await asyncio.sleep(1)
            await interaction.guild.voice_client.disconnect()
            await interaction.client.change_presence(status = discord.Status.idle, activity = discord.CustomActivity(name = "Hateando las nuevas temporadas"))
            return True
        else:
            return False

class NiceNames:
    def file(file):
        os.path.basename(file)
        file = file.removesuffix(".mp3")
        file = list(file.split("-"))
        folder = file [0]
        # file.pop(0)
        name = ' '.join(file)
        return [folder, name]

    def directories(files, path):
        output = []
        folders = []

        for file in files:
            if (file.rsplit('.', 1)[-1] != file):
                output.append(file)
            else:
                folders.append(file)
        
        for folder in folders:
            files = os.listdir(path+"/"+folder)
            for file in files:
                if (file.rsplit('.', 1)[-1] != file):
                    output.append(folder+"/"+file)
        return output

class AudioButton(discord.ui.Button):
    def __init__(self, label, path):
        super().__init__(label=label, style=discord.ButtonStyle.blurple)
        self.path = path

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await Clear.this_channel(interaction)
        if not interaction.guild.voice_client:
            connected = await AudioBot.join(interaction)

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
            files = os.listdir("./Audios")
            audios = NiceNames.directories(files = files, path = "./Audios")
            if not interaction.guild.voice_client:
                await AudioBot.join(interaction)
                await interaction.followup.send("El siguiente prometo que será aleatorio")
            else:
                interaction.guild.voice_client.play(FFmpegPCMAudio("./Audios/" + audios[random.randint(0,len(audios)-1)])) #dice que no hay voice_client

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

        files = os.listdir("./Audios")
        self.viewer.add_item(FirstButton("Aleatorio"))

        self.viewer.button(path="./Audios")

        #if n>len(files)/22 or len(files)<23
        # self.viewer.add_item(LastButton())

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
        this_channel = discord.utils.get(interaction.guild.channels, name = "audio-panel") 
        messages = [message async for message in this_channel.history(oldest_first = True)]
        my_message = messages[0]
        await this_channel.purge(after = my_message)

class NormalizeAudios:
    def __init__(self, directory) -> None:
        self.process_directory(directory)

    def process_directory(self, directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.mp3'):
                    file_path = os.path.join(root, file)
                    output_path = os.path.join(root, file)
                    print(f"Normalizando {file_path}")
                    self.normalice(file_path, output_path)

    def normalice(self, file_path, output_path):
        audio, sample_rate = sf.read(file_path)
        datos_np = np.array(audio)
        max_value = np.max(datos_np)
        datos_np = datos_np/max_value
        datos_np = datos_np*0.5
        sf.write(output_path, datos_np, sample_rate)


class FolderSelect(discord.ui.Select):
    def __init__(self, path, audio):
        self.path = path
        self.audio = audio
        folders = os.listdir(path)
        options = []

        for folder in folders:
            option = discord.SelectOption(label = folder, value = folder)
            options.append(option)

        super().__init__(placeholder="Elige una opcion...", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        folder_selected = self.values[0]
        complete_path = os.path.join(self.path, folder_selected, self.audio.filename)
        await self.audio.save(fp=complete_path)
        await interaction.response.send_message(f'Archivo de audio {self.audio.filename} ha sido guardado exitosamente.')
         
class FolderView(discord.ui.View):
    def __init__(self, timeout = 180):
        super().__init__(timeout = timeout)

    def select(self, path, audio):
        self.add_item(FolderSelect(path, audio))
