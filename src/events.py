from discord.ext import commands
import logging
import discord

from src.utils import AudioBot, JoinBot, NiceNames
import ast
from src.audio_panel import AudioPanel2


logger = logging.getLogger(__name__)
logging.basicConfig(filename='error.log', encoding='utf-8', level=logging.DEBUG)

class Events:
    def __init__(self, bot, serverid):
        self.bot = bot
        self.serverid = serverid

        # Registrar los eventos en el bot
        self.bot.event(self.on_ready)
        self.bot.event(self.on_command_error)
        #self.bot.event(self.on_interaction)

    async def on_ready(self):
        print(f'Bot conectado como {self.bot.user}')
        # Obtener el objeto del servidor usando su ID
        
        await self.bot.change_presence(status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.watching, name = "Los Simpson"))

        # Sincronizar los comandos en el servidor
        await self.bot.tree.sync()   
        
        guild = self.bot.get_guild(705374640658317322)
        chanel = discord.utils.get(guild.channels, name = "audio-panel")
        panel = AudioPanel2()
        deleted = await chanel.purge()
        await chanel.send(view = panel.viewer, embed = panel.embed, file = panel.file)

        print("Comandos de barra sincronizados en el servidor:")


    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Comando no encontrado.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Faltan argumentos requeridos para este comando.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Se proporcionó un argumento inválido.")
        else:
            await ctx.send("Ha ocurrido un error al ejecutar el comando.")       
        logger.error(f'{error}')


    # async def on_interaction(self, interaction):
    #     if interaction.type == discord.InteractionType.component:
    #         data = interaction.data['custom_id']
    #         if "audio_panel_interaction" in data:
    #             data_array = ast.literal_eval(data)
    #             path = data_array[0] 
    #             await AudioBot.play_audio(interaction, path, self.bot)
