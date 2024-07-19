import discord
import os
from discord import FFmpegPCMAudio
from dotenv import load_dotenv, find_dotenv
import json

#list_audios = os.system("find ./Audios -type f") #esto ejecuta el comando en la terminal, pero "no" en el script
#file = os.path.basename(list_audios[1])
#print(type(list_audios))
#print(file)

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
            option = discord.SelectOption(label=f"{archivo}", description="")
            options.append(option)
        # print(options)
        
        super().__init__(placeholder="Elige una opcion...", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        load_dotenv()
        #root_path = os.getenv("ROOTPATH")
        audio_selected = self.values[0]
        print(self.values)
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

class JoinBot():
    async def join_audio_channel(interaction: discord.Interaction, bot):
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            await channel.connect()

            await bot.change_presence(status = discord.Status.online, activity = discord.CustomActivity(name = "Cocinando memes"))
            
            voice_client = interaction.guild.voice_client
            audio_player = AudioPlayer(voice_client)
            audio_selected = "./Saludos/ned_flanders_hola_holita_vecinito.mp3"
            await audio_player.play_audio(audio_selected)
            return True
        else:
            await interaction.response.send_message("Bot no se puede unir, metete en un canal de audio!")
            return False