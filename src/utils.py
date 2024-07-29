import discord
import os
from discord import FFmpegPCMAudio
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf


# CLASES
# Crear una vista personalizada con un menu de seleccion
class AudioSelect(discord.ui.Select):
    def __init__(self, voice_client, path):
        self.voice_client = voice_client
        self.path = path
        archivos = os.listdir(path)
        archivos_filtered = self.filter_directories(archivos, path)
        options = []
        
        for archivo in archivos_filtered:
            nombre = NiceNames(archivo)
            option = discord.SelectOption(label = nombre.name, value = archivo)
            options.append(option)
        
        super().__init__(placeholder="Elige una opcion...", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        audio_selected = self.values[0]
        audio_path = self.path+"/"+audio_selected
        await interaction.response.defer()
        source = FFmpegPCMAudio(audio_path)
        self.voice_client.play(source)

        #Aqui se puede hacer para que, si te cambias de canal el bot te pregunte si quieres que te siga o no
        #seguramente sea usando voice_client para el canal original e interaction.user.voice.channel.connect()
        #mas luego voice_client = interaction.guild.voice_client

    def filter_directories(self, files, path):
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
         
class AudioView(discord.ui.View):
    def __init__(self, timeout = 180):
        super().__init__(timeout = timeout)

    def select(self, voice_client, path):
        self.add_item(AudioSelect(voice_client, path))

    def button(self, path):
        carpetas = os.listdir(path)
        for carpeta in carpetas:
            self.add_item(AudioButton(f"{carpeta}", path))

class JoinBot: #cambiar nombre a AudioBot (controla si el audio se conecta o no) y añadir leave
    async def join_audio_channel(interaction: discord.Interaction): #cambiar a join solamente, aqui el bot ya no
    #hace falta
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            await channel.connect()

            await interaction.client.change_presence(status = discord.Status.online, activity = discord.CustomActivity(name = "Cocinando memes"))
            
            # voice_client = interaction.guild.voice_client
            # audio_selected = "./Audios/Saludos/Saludos-Hola-Holita-Vecinito.mp3"
            # source = FFmpegPCMAudio(audio_selected)
            # voice_client.play(source)
            return True
        else:
            await interaction.response.send_message("Bot no se puede unir, metete en un canal de audio!")
            return False
        
class AudioBot: # devolverle esto al comando /Audios
    async def display_select_audios(interaction: discord.Interaction, path):
        #voice_client = interaction.guild.voice_client
       #if not voice_client:
        connected = await JoinBot.join_audio_channel(interaction)
        if not connected:
            return
        voice_client = interaction.guild.voice_client  # Actualiza el cliente de voz

        view = AudioView() 
        view.select(voice_client, path) #Antes era audio_player = audio_player
        await interaction.response.send_message("Elige una opcion del menu:", view=view) #Sacarlo al command


#Esta funcion es lo mismo que hacer discord.utils.get(guild.channels, name = channel_name)
    def get_channel_by_name(guild, channel_name):
        for channel in guild.channels:
            if channel.name == channel_name:
                return channel
        return None

class NiceNames:
    def __init__(self, file):
        os.path.basename(file)
        file = file.removesuffix(".mp3")
        file = list(file.split("-"))
        self.folder = file [0]
        file.pop(0)
        self.name = ' '.join(file)

class AudioButton(discord.ui.Button):
    def __init__(self, label, path):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.path = path

    async def callback(self, interaction: discord.Interaction):
        if not interaction.guild.voice_client:
            connected = await JoinBot.join_audio_channel(interaction)

        view = AudioView()
        view.select(interaction.guild.voice_client, self.path + "/" + self.label)
        await interaction.response.send_message(view = view)

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
        sf.write(output_path, datos_np, sample_rate)