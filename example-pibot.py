import discord
from discord.ext import commands
# from discord import Intents

intents = discord.Intents.default()  # Esto habilita todos los intents disponibles
intents.messages = True  # Habilita el intent para manejar mensajes
intents.reactions = True
intents.presences = True


bot = commands.Bot(command_prefix='>',intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run('')
