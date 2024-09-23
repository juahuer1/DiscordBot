import discord
import os
import re
import shutil
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
            if os.path.isdir(os.path.join(path,file)):
                folders.append(file)
        return folders

    def files(path):
        output = []

        files = os.listdir(path)
        for first in files: #Primera tanda de archivos/carpetas, Ej: Audios
            if os.path.isfile(os.path.join(path,first)):
                output.append(first)
            else:       
                second = os.listdir(os.path.join(path,first)) #Segunda tanda de archivos/subcarpetas, Ej: Audios/Simpsons
                for third in second:
                    if os.path.isfile(os.path.join(path,first,third)):
                        output.append(os.path.join(first,third))
                    else:        
                        fourth = os.listdir(os.path.join(path,first,third)) #Tercera tanda de archivos/subsubcarpetas, Ej: Audios/Simpsons/Homer
                        for fifth in fourth:
                            if os.path.isfile(os.path.join(path,first,third,fifth)):
                                output.append(os.path.join(first, third,fifth))
        return output

    def same(file, path):
        status = False
        if os.path.isdir(os.path.join(path,file)):
            folders = Archive.directories(path)
            for my_folder in folders:
                if (os.path.basename(my_folder) == file):
                    status = True
            
            return status
        elif os.path.isfile(os.path.join(path,file)):
            files = Archive.files(path)
            for my_file in files:
                if (os.path.basename(my_file) == file):
                    status = True
            
            return status
        
    def es_nombre_valido(nombre_archivo):
        # Expresión regular para permitir letras (a-z, A-Z), números (0-9), y guion normal (-)
        patron = r'^[a-zA-Z0-9-.]+$'
        
        # Verificar si el nombre coincide con el patrón
        if re.match(patron, nombre_archivo):
            return True
        else:
            return False
        
    def info_audios(folder_paths):
        response =[]

        for path in folder_paths:
            folders = 0
            files = 0
            for ruta_actual, subdirectorios, archivos in os.walk(path):
                for subdirectorio in subdirectorios:
                    folders +=1
                for archivo in archivos:
                    files +=1
            value = {"folders": folders, "files": files}
            response.append(value)

        return response


class Clear():
    async def this_channel(interaction):
        messages = [message async for message in interaction.channel.history(oldest_first = True)]
        await interaction.channel.purge(after = messages[0])

class SelectFolder(discord.ui.Select):
    def __init__(self, original_path, base_path, audio, m):
        self.original_path = original_path
        self.base_path = base_path
        self.audio = audio
        self.m = m
        files = os.listdir(self.base_path)
        self.extended = SelectExtended(files, self.m)
        super().__init__(placeholder="Elige una opción...", max_values=1, min_values=1, options = self.extended.options)

    async def callback(self, interaction: discord.Interaction):
        go_next = await self.extended.go_next(interaction, self.values, self.base_path)
        if not go_next:
            folder_selected = self.values[0]
            audios_path = os.path.join(self.original_path, folder_selected, self.audio.filename)

            if(Archive.es_nombre_valido(self.audio.filename) == False):
                await interaction.followup.send('Hay un problema con el nombre del audio, recuerda que solo puede contener letras, números y guión alto (-), no introduzcas espacios!', silent = True)
                return

            if(Archive.same(self.audio.filename, os.path.join(self.original_path, folder_selected)) or Archive.same(self.audio.filename, os.path.join(self.base_path, folder_selected))):
                await interaction.followup.send('¡Ya existe un audio con ese nombre!', silent = True)
                return

            await self.audio.save(fp=audios_path)

            full_base_path = os.path.join(self.base_path, folder_selected, self.audio.filename)
            rawsound = AudioSegment.from_file(audios_path, "mp3")  
            normalizedsound = effects.normalize(rawsound)
            normalizedsound.export(full_base_path, format="mp3")

            await interaction.followup.send(f'Audio {self.audio.filename} ha sido guardado exitosamente.', silent = True)
            self.view.stop()

class IdentifyPanel():
    async def channel(interaction):
        if interaction.channel.name == InitEnv.simpsons_channel_name:
            return InitEnv.simpsons
        elif interaction.channel.name == InitEnv.offtopic_channel_name:
            return InitEnv.offtopic
        else:
            await interaction.response.send_message("No estás en ningún audio panel", silent = True)


class AuxView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

    def remove_select(self, base_path, original_path, m):
        self.add_item(SelectToRemove(base_path, original_path, m))

    def folder_select(self, original_path, base_path, audio, m):
        self.add_item(SelectFolder(original_path, base_path, audio, m))

    def filebutton(self, base_path, original_path, folder):
        self.add_item(FileButton(base_path, original_path, folder))

    def confirmbutton(self, base_path, original_path, file):
        self.add_item(ConfirmButton(base_path, original_path, file))


class SelectToRemove(discord.ui.Select):
    def __init__(self, base_path, original_path, m):
        self.original_path = original_path
        self.base_path = base_path
        self.m = m
        files = os.listdir(self.base_path)
        self.extended = SelectExtended(files, self.m)
        super().__init__(placeholder="Elige una opción...", max_values=1, min_values=1, options = self.extended.options)

    async def callback(self, interaction: discord.Interaction):
        go_next = await self.extended.go_next(interaction, self.values, self.base_path)
        if not go_next:
            file_selected = self.values[0]
            path = os.path.join(self.base_path ,file_selected)

            reply = f"Has seleccionado borrar {file_selected}, ¿estás seguro?"

            view = AuxView()
            view.confirmbutton(self.base_path, self.original_path, file_selected)
            if os.path.isdir(path):
                archives = [item for item in os.listdir(path) if os.path.isfile(os.path.join(path, item))]
                reply = reply + f", la carpeta continene {len(archives)} audios"
                view.filebutton(self.base_path, self.original_path, file_selected)

            await interaction.followup.send(content = reply,view = view, silent = True)
            self.view.stop()

class FileButton(discord.ui.Button):
    def __init__(self, base_path, original_path, folder):
        self.base_path = os.path.join(base_path, folder)
        self.original_path = os.path.join(original_path, folder)
        super().__init__(label="Elegir audio", style=discord.ButtonStyle.grey)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking = True)
        if not os.listdir(self.base_path):
            await interaction.followup.send("La carpeta está vacía", silent = True)
            return
        view = AuxView()
        view.remove_select(self.base_path, self.original_path, 0)
        await interaction.followup.send(content = "Elige audio a borrar", view = view, silent = True)
        self.view.stop()

class ConfirmButton(discord.ui.Button):
    def __init__(self, base_path, original_path, file):
        self.base_path = os.path.join(base_path, file)
        self.original_path = os.path.join(original_path, file)
        self.file = file
        super().__init__(label="Borrar", style=discord.ButtonStyle.red)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking = True)

        if os.path.isdir(self.base_path):
            shutil.rmtree(self.base_path)
            shutil.rmtree(self.original_path)
            await interaction.followup.send(f'Carpeta {self.file} eliminada correctamente', silent = True)
            
            data = await IdentifyPanel.channel(interaction)

            from src.audios import AudioPanel
            await AudioPanel.edit(interaction, data, 0)

        elif os.path.isfile(self.base_path):
            os.remove(self.base_path) 
            os.remove(self.original_path) 
            await interaction.followup.send(f'Audio {self.file} eliminado correctamente', silent = True)

        else:
            await interaction.followup.send("???", silent = True)

        self.view.stop()

class SelectExtended():
    def __init__(self, files, m):
        self.m = m
        files.sort()
        self.options = []

        if len(files) > 25 and self.m >= 1:
            self.options.append(discord.SelectOption(label = "Menos...", value = "Extra,-1"))

        for archivo in files[self.m*25:(self.m+1)*25-1]:
            nombre = Archive.nice_name(archivo)
            option = discord.SelectOption(label = nombre, value = archivo)
            self.options.append(option)
        if len(files)>25 and self.m<(len(files)/25)-1:
            self.options.append(discord.SelectOption(label = "Más...", value = "Extra,1"))

    async def go_next(self, interaction, values, path):
        await interaction.response.defer()        
        my_values = list(values[0].split(","))
        if my_values[0] == "Extra":
            self.m = self.m + int(my_values[1])

            from src.audios import AudioView
            view = AudioView()
            view.select(path, self.m)

            messages = [message async for message in interaction.channel.history()]
            await messages[0].edit(view = view)
            return True
        else:
            return False

class Admin():
    async def developers(interaction, data):
        if data == InitEnv.simpsons and interaction.user.id not in InitEnv.devs:
            devs = []
            for dev in InitEnv.devs:
                devs.append(interaction.guild.get_member(dev).mention)
            disp_devs = " ".join(devs)
            await interaction.response.send_message(f"Contacta con: {disp_devs}", silent = True)
            return False
        else:
            return True