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

        source = FFmpegPCMAudio('./Audios/'+audio_selected)
        self.voice_client.play(source)

class AudioSelect(discord.ui.Select):
    def __init__(self, audio_player, system_functions):
        self.audio_player = audio_player
        self.system_functions = system_functions
        archivos = system_functions.list_audios()

        options = []
        
        for archivo in archivos:
            option = discord.SelectOption(label=f"{archivo}", description="Esta es la opcion 1")
            options.append(option)
        
        super().__init__(placeholder="Elige una opcion...", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        try:
            audio_selected = self.values[0]
            await interaction.response.defer()
            await self.audio_player.play_audio(audio_selected)
        except Exception as e:
            # En caso de error, enviar un mensaje de error al usuario
            await interaction.response.send_message(f'Ocurrio un error: {str(e)}', ephemeral=True)

class AudioView(discord.ui.View):
    def __init__(self, audio_player, system_functions):
        super().__init__()
        self.add_item(AudioSelect(audio_player, system_functions))

class SystemFunctions:
    def __init__(self):
        self.list_audios()
        
    def list_audios(self):
        archivos = os.listdir("./Audios")
        return archivos