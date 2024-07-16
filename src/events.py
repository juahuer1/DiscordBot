# events.py

import discord
from discord.ext import commands
import logging
from src.slash_commands import SetupSlashCommands


logger = logging.getLogger(__name__)
logging.basicConfig(filename='events.log', encoding='utf-8', level=logging.DEBUG)

class Events:
    def __init__(self, bot, serverid):
        self.bot = bot
        self.serverid = serverid

        # Registrar los eventos en el bot
        self.bot.event(self.on_ready)
        self.bot.event(self.on_command_error)

    async def on_ready(self):
        print(f'Bot conectado como {self.bot.user}')
        try:
            # Obtener el objeto del servidor usando su ID
            guild = discord.Object(id=self.serverid)
            
            # Sincronizar los comandos en el servidor
            SetupSlashCommands.setup_commands(self.bot)
            # YA NO ES NECESARIO EL SYNC DEL TREE QUIZAS.........
            # commands = await self.bot.tree.sync(guild=guild)
            print("Comandos de barra sincronizados en el servidor:")
        
        except Exception as e:
            pass
            print(f"Error al sincronizar comandos de barra: {e}")

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
