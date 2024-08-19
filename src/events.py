from discord.ext import commands
import logging
from src.utils import *
from src.audios import *
import asyncio

logger = logging.getLogger(__name__)
logging.basicConfig(filename='error.log', encoding='utf-8', level=logging.DEBUG)

class Events:
    def __init__(self, bot):
        self.bot = bot
        # Registrar los eventos en el bot
        self.bot.event(self.on_ready)
        self.bot.event(self.on_command_error)
        self.bot.event(self.on_voice_state_update)

    async def on_ready(self):
        print(f'Bot conectado como {self.bot.user}')
        # Obtener el objeto del servidor usando su ID

        # Sincronizar los comandos en el servidor
        await self.bot.tree.sync()   

        await AudioPanel.start(self.bot, "simpsons")
        await AudioPanel.start(self.bot, "offtopic")

        print("Comandos de barra sincronizados en el servidor:")

    async def on_voice_state_update(self, member, before, after):
        if not member.guild.voice_client:
            return 

        if len(member.guild.voice_client.channel.members) == 1:
            await asyncio.sleep(20)
            if len(member.guild.voice_client.channel.members) == 1:
                await member.guild.voice_client.disconnect()
            return

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