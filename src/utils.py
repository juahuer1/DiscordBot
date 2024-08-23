import discord
import os
from src.thematic import *
from pydub import AudioSegment, effects  


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
        for first in files: #Primera tanda de archivos/carpetas, Ej: Audios
            if (first.rsplit('.', 1)[-1] != first):
                output.append(first)
            else:        
                second = os.listdir(os.path.join(path,first)) #Segunda tanda de archivos/subcarpetas, Ej: Audios/Simpsons
                for third in second:
                    if (third.rsplit('.', 1)[-1] != third):
                        output.append(os.path.join(first,third))
                    else:        
                        fourth = os.listdir(os.path.join(path,first,third)) #Tercera tanda de archivos/subsubcarpetas, Ej: Audios/Simpsons/Homer
                        for fifth in fourth:
                            if (fifth.rsplit('.', 1)[-1] != fifth):
                                output.append(os.path.join(first, third,fifth))
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
            files = Archive.files(path)
            for my_file in files:
                if (os.path.basename(my_file) == file):
                    status = True
            
            return status

class Clear():
    async def this_channel(interaction):
        messages = [message async for message in interaction.channel.history(oldest_first = True)]
        await interaction.channel.purge(after = messages[0])

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
        await interaction.response.defer(thinking=True)
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
        self.view.stop()
         
class FolderView(discord.ui.View):
    def __init__(self, timeout = 180):
        super().__init__(timeout = timeout)

    def select(self, original_path, base_path, audio):
        self.add_item(FolderSelect(original_path, base_path, audio))

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