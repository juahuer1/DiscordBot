import discord
import os
from discord import FFmpegPCMAudio

# CLASES
# Crear una vista personalizada con un menu de seleccion
class AudioPlayer:
    def __init__(self, voice_client):
        self.voice_client = voice_client
        
        
    async def play_audio(self, audio_selected):
        if not self.voice_client or not self.voice_client.is_connected():
            raise RuntimeError("El bot no esta conectado a ningun canal de voz.")

        source = FFmpegPCMAudio(audio_selected)
        self.voice_client.play(source)

class AudioSelect(discord.ui.Select):
    def __init__(self, audio_player, path):
        self.audio_player = audio_player
        self.path = path
        archivos = os.listdir(path)
        archivos_filtered = self.filter_directories(archivos, path)
        options = []
        
        for archivo in archivos_filtered:
            nombre = NiceNames(archivo)

            #Este if es necesario porque, por algun motivo, existe un primer nombre.name vacio
            #investigar si el problema reside en la clase NiceNames o filter_directories
            if nombre.name != "":
                option = discord.SelectOption(label = nombre.name, value = archivo)
                options.append(option)
        # print(options)
        
        super().__init__(placeholder="Elige una opcion...", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        audio_selected = self.values[0]
        audio_path = self.path+"/"+audio_selected
        await interaction.response.defer()
        await self.audio_player.play_audio(audio_path)

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
    def __init__(self, audio_player, path):
        super().__init__()
        self.add_item(AudioSelect(audio_player, path))

class JoinBot:
    async def join_audio_channel(interaction: discord.Interaction, bot):
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            await channel.connect()

            await bot.change_presence(status = discord.Status.online, activity = discord.CustomActivity(name = "Cocinando memes"))
            
            voice_client = interaction.guild.voice_client
            audio_player = AudioPlayer(voice_client)
            audio_selected = "./Audios/Saludos/ned_flanders_hola_holita_vecinito.mp3"
            await audio_player.play_audio(audio_selected)
            return True
        else:
            await interaction.response.send_message("Bot no se puede unir, metete en un canal de audio!")
            return False
        
class AudioBot:
    async def play_audio(interaction: discord.Interaction, path, bot):
        voice_client = interaction.guild.voice_client
        if not voice_client:
            connected = await JoinBot.join_audio_channel(interaction,bot)
            if not connected:
                return
            voice_client = interaction.guild.voice_client  # Actualiza el cliente de voz

        audio_player = AudioPlayer(voice_client) 
        view = AudioView(audio_player, path)  
        await interaction.response.send_message("Elige una opcion del menu:", view=view)

    def get_channel_by_name(guild, channel_name):
        for channel in guild.channels:
            if channel.name == channel_name:
                return channel
        return None

class NiceNames:
    def __init__(self, file):
        self.file = file
        os.path.basename(file)
        file_name = file.removesuffix(".mp3")
        nice_file = file_name.split("-")
        self.folder = nice_file [0]
        nice_file.pop(0)
        self.name = ' '.join(nice_file)