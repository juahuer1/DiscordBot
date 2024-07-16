import discord
from discord.ext import commands
import logging

class Events:
    def __init__(self,bot,serverid,logger):
        self.bot = bot
        self.serverid = serverid
        self.logger = logger

        self.bot.event(self.on_ready)
        self.bot.event(self.on_command_error)

    async def on_ready(self):
        print(f'Bot conectado como {self.bot.user}')
        try:
            # Sincroniza los comandos de barra en un servidor especico
            guild = discord.Object(id=self.serverid)  # Reemplaza YOUR_GUILD_ID con el ID de tu servidor
            commands = await self.bot.tree.sync(guild=None)
            print("Comandos de barra sincronizados en el servidor:")
        except Exception as e:
            print(f"Error al sincronizar comandos de barra: {e}")
        

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Comando no encontrado.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Faltan argumentos requeridos para este comando.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Se proporciono un argumento invalido.")
        else:
            self.logger.error(f'{error}')
            await ctx.send("Ha ocurrido un error al ejecutar el comando.")
