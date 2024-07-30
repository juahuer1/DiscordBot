from discord.ext import commands
import logging
import discord
from src.utils import AudioBot, AudioPanel
import ast
from dotenv import load_dotenv
import os
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

        panel = AudioPanel()

        for guild in self.bot.guilds:
            if not discord.utils.get(guild.channels, name = "audio-panel"):
                overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=True), guild.me: discord.PermissionOverwrite(read_messages=True)}
                await guild.create_text_channel(name = "audio-panel", overwrites = overwrites, category = discord.utils.get(guild.categories, name = "Canales de texto"))
            chanel = discord.utils.get(guild.channels, name = "audio-panel")
            deleted = await chanel.purge()
            await chanel.send(view = panel.viewer, embed = panel.embed, file = discord.File("./Imagenes/moe_al_habla.jpg", filename="moe_al_habla.jpg"), silent = True)

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