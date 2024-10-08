import discord
from src.utils import *
from src.thematic import *
import os
import asyncio
from discord import FFmpegPCMAudio
import random

class AudioBot:
    async def join (interaction: discord.Interaction, silent = False):
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            await channel.connect()
            await interaction.client.change_presence(status = discord.Status.online, activity = discord.CustomActivity(name = "Cocinando memes"))           
            path = os.path.join(InitEnv.simpsons_base_path, 'Saludos')
            saluditos = os.listdir(path)
            if(not silent):
                AudioSound(saluditos, path, interaction)
            return True
        else:
            await interaction.followup.send("¡Métete en un canal de audio!", silent = True)
            return False

    async def leave (interaction: discord.Interaction, silent = False):
        if interaction.guild.voice_client:
            path = os.path.join(InitEnv.simpsons_base_path, 'Despedidas')
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
        
class AudioPanel():
    def __init__(self, data, n):
        self.view = AudioView()
        self.view.add_item(FirstButton("Aleatorio", data))
        self.view.button(data["path"], data["silent"])
        if n < 1 and len(os.listdir(data["path"])) > 25:
            self.view.add_item(LastButton(data, n))
        self.view.add_item(StopButton(data))

        self.embed = discord.Embed(title=data["audio_panel_title"], description=data["audio_panel_description"][random.randint(0,len(data["audio_panel_description"])-1)], color=0x00ff00)
        self.embed.set_image(url=data["audio_panel_image_url"])

    async def start(guild, thematic):
        if thematic == "simpsons":
            data = InitEnv.simpsons
        elif thematic == "offtopic":
            data = InitEnv.offtopic
        else:
            raise

        panel = AudioPanel(data, 0)

        
        if not discord.utils.get(guild.channels, name = data["channel"]):
            overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=True), guild.me: discord.PermissionOverwrite(read_messages=True)}
            await guild.create_text_channel(name = data["channel"], overwrites = overwrites, category = discord.utils.get(guild.categories, name = "Canales de texto"))
        chanel = discord.utils.get(guild.channels, name = data["channel"])
        deleted = await chanel.purge()

        file = discord.File(data["audio_panel_image_path"], filename=data["audio_panel_image_name"])
        await chanel.send(view = panel.view, embed = panel.embed, file = file, silent = True)

    async def edit(interaction, data, n):
        messages = [message async for message in interaction.channel.history(oldest_first = True)]

        panel = AudioPanel(data, n)

        await messages[0].edit(view = panel.view, embed = panel.embed)

class HelpPanel():
    async def start(guild):
        data = InitEnv.helper
        embed1 = discord.Embed(title = data["title1"], description=data["comandos"], color=0x00ff00)
        embed1.set_image(url=data["help_panel_command_url"])
        embed2 = discord.Embed(title = data["title2"], description=data["paneles"], color=0x00ff00)
        embed2.set_image(url=data["help_panel_panel_url"])
        if not discord.utils.get(guild.channels, name = data["channel"]):
            overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=True), guild.me: discord.PermissionOverwrite(read_messages=True)}
            await guild.create_text_channel(name = data["channel"], overwrites = overwrites, category = discord.utils.get(guild.categories, name = "Canales de texto"))
        chanel = discord.utils.get(guild.channels, name = data["channel"])
        deleted = await chanel.purge()

        files = [discord.File(data["help_panel_command_path"], filename=data["help_panel_command_name"]), discord.File(data["help_panel_panel_path"], filename=data["help_panel_panel_name"])]
        await chanel.send(embeds = [embed1,embed2], files= files, silent = True)

class AudioView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

    def select(self, path, m):
        self.add_item(AudioSelect(path, m))

    def button(self, path, silent):
        carpetas = os.listdir(path)
        carpetas.sort()
        for carpeta in carpetas:
            self.add_item(AudioButton(f"{carpeta}", path, silent))
        
class FirstButton(discord.ui.Button):
    def __init__(self, label, data):
        self.data = data
        if label == "Aleatorio":
            colour = discord.ButtonStyle.green
        if label == "Anteriores":
            colour = discord.ButtonStyle.grey
        super().__init__(label = label, style = colour)

    async def callback(self, interaction: discord.Interaction): #editar mensaje usando m_panel??
        await interaction.response.defer()        
        await Clear.this_channel(interaction)
        if self.label == "Aleatorio":
            
            audios = Archive.files(path = self.data["path"])
            if not interaction.guild.voice_client:
                connected = await AudioBot.join(interaction, self.data["silent"])
                while interaction.guild.voice_client.is_playing():
                    await asyncio.sleep(1)
                if not connected:
                    return
            AudioSound(audios, self.data["path"], interaction)

class AudioButton(discord.ui.Button):
    def __init__(self, label, path, silent):
        super().__init__(label=label, style=discord.ButtonStyle.blurple)
        self.path = path
        self.silent = silent

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()        
        await Clear.this_channel(interaction)
        if not os.listdir(os.path.join(self.path, self.label)):
            await interaction.followup.send("La carpeta está vacía", silent = True)
            return

        if not interaction.guild.voice_client:
            connected = await AudioBot.join(interaction, self.silent) 
            if not connected:
                return

        view = AudioView()
        view.select(os.path.join(self.path, self.label), 0)
        await interaction.followup.send(view = view, silent = True)

class LastButton(discord.ui.Button): #Ponerle límite para que en la última iteración no salga
    def __init__(self, data, n):
        self.data = data
        self.n = n
        super().__init__(label = "Siguientes", style = discord.ButtonStyle.grey)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("La carpeta está vacía", silent = True)
        self.n = self.n + 1
        await AudioPanel.edit(interaction, self.data, self.n)

class StopButton(discord.ui.Button):
    def __init__(self, data):
        super().__init__(label = "Stop", style = discord.ButtonStyle.red)
        self.data = data

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()        
        await Clear.this_channel(interaction)
        await AudioPanel.edit(interaction, self.data, 0)
        await AudioBot.leave(interaction, self.data["silent"])
        
class AudioSelect(discord.ui.Select):
    def __init__(self, path, m):
        self.path = path
        self.m = m
        archivos_filtered = Archive.files(path)
        self.extended = SelectExtended(archivos_filtered, self.m)
        super().__init__(placeholder="Elige una opción...", max_values=1, min_values=1, options = self.extended.options)

    async def callback(self, interaction: discord.Interaction):
        go_next = await self.extended.go_next(interaction, self.values, self.path)
        if not go_next:
            audio_selected = self.values[0]
            AudioSound(audio_selected, self.path, interaction)

class AudioSound():
    def __init__(self, file, path, interaction: discord.Interaction):
        if type(file) is list:
            playing = file[random.randint(0,len(file)-1)]
        else:
            playing = file
        interaction.guild.voice_client.play(FFmpegPCMAudio(os.path.join(path, playing)))