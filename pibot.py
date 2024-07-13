# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from dotenv import load_dotenv
import os
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.ui import Select, View
from discord import FFmpegPCMAudio
import random
import logging

from src.utils import *

description = '''Bot de Juan (con ayuda esporadica de Sergio), pa poder meter audios y lo que nos salga de ahi.

SE ACEPTAN SUGERENCIAS, SI ALGUIEN QUIERE METER SU AUDIO QUE ME LO PASE'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

load_dotenv()
bottoken = os.getenv('BOTTOKEN')
applicationid = os.getenv('APPLICATIONID')
serverid = os.getenv('SERVERID')

bot = commands.Bot(command_prefix='?', description=description, intents=intents, application_id=applicationid)

logger = logging.getLogger(__name__)
logging.basicConfig(filename='pibot.log', encoding='utf-8', level=logging.DEBUG)


# EVENTOS
    
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    try:
        # Sincroniza los comandos de barra en un servidor especico
        guild = discord.Object(id=serverid)  # Reemplaza YOUR_GUILD_ID con el ID de tu servidor
        commands = await bot.tree.sync(guild=None)
        print("Comandos de barra sincronizados en el servidor:")
    except Exception as e:
        print(f"Error al sincronizar comandos de barra: {e}")
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Faltan argumentos requeridos para este comando.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Se proporciono un argumento invalido.")
    else:
        logger.error(f'{error}')
        await ctx.send("Ha ocurrido un error al ejecutar el comando.")

# GRUPOS Y SUBCOMANDOS
@bot.group()
async def cool(ctx):
    """Dice si un menda del server mola o no (Ex: ?cool Khrisleo)
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')

# COMANDOS
@bot.command()
async def add(ctx, left: int, right: int):
    """Suma dos numeros (Ex: ?add 5 11)"""
    await ctx.send(left + right)


@bot.command()
async def roll(ctx, dice: str):
    """Tira N dados de N caras en este orden NdN (dados, caras) (Ex: ?roll 3d6)"""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Elige al azar entre varias opciones (Ex: ?choose Pizza Pasta Hamburguesa)"""
    await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repite lo mismo muchas veces (Ex: ?repeat 5 Feo)"""
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Fecha de inclusion de un miembro (Ex: ?joined juanmingla)"""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


@bot.command(name='bot')
async def _bot(ctx):
    """Mola mi bot u que? (Ex: ?bot)"""
    await ctx.send('Es la peripocha.')
    
    
@bot.command(pass_context = True)
async def join(ctx):
    """Agrega el bot al chat (Ex: ?join)"""
    status = False   
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await ctx.send("Bot spawneando pa molestar a AiramariA")
        status = True
    else:
        await ctx.send("Bot no se puede unir, metete en un canal de audio!")
    return status
        
        
@bot.command(pass_context = True)
async def leave(ctx):
    """Elimina el bot del chat (Ex: ?leave)"""
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("El putisimo Bot se pira")
    else:
        await ctx.send("Bot no esta en el canal")


@bot.command(name='audios')
async def audios(ctx):
    """Reproduce audios en el canal en uso (Ex: ?audios)"""
    voice_client = ctx.guild.voice_client
    if not voice_client:
        connected = await join(ctx)
        if not connected:
            return
    
    # Importante actualizar objeto voice_client
    voice_client = ctx.guild.voice_client
    
    audio_player = AudioPlayer(voice_client)
    system_functions = SystemFunctions()
    view = AudioView(audio_player,system_functions)
    await ctx.send("Elige una opcion del menu:", view=view)
    
@bot.command(name='clearaudio')
async def clearaudio(ctx):
    """Interrumpimos audio en reproduccion (Ex: ?clearaudio)"""
    voice_client = ctx.guild.voice_client
    voice_client.stop()












    
# Define un comando de barra (slash command)
@bot.tree.command(name="add", description="Suma dos numeros (Ex: /add 5 11)")
async def add(interaction: discord.Interaction, left: int, right: int):
    result = left + right
    await interaction.response.send_message(str(result))

    
@bot.tree.command(name="roll", description="Tira N dados de N caras en este orden NdN (dados, caras) (Ex: /roll 3d6)")
async def roll(interaction: discord.Interaction, dice: str):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await interaction.response.send_message('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await interaction.response.send_message(result)


@bot.tree.command(name="choose",description='Elige al azar entre varias opciones (Ex: /choose Pizza Pasta Hamburguesa)')
async def choose(interaction: discord.Interaction, choices: str):
    chosen = random.choice(choices.split())
    await interaction.response.send_message(chosen)

# @bot.tree.command(name="repeat", description="Repite lo mismo muchas veces (Ex: /repeat 5 Feo)")
# async def repeat(interaction: discord.Interaction, times: int, content: str = 'repeating...'):
#     for i in range(times):
#         await interaction.response.send_message(content)
#         await interaction.followup.send(content)

@bot.tree.command(name="repeat", description="Repite lo mismo muchas veces (Ex: /repeat 5 Feo)")
async def repeat(interaction: discord.Interaction, times: int, content: str):
    # Respondemos con la primera instancia del contenido para cumplir con las reglas de interacción
    await interaction.response.send_message(content)
    
    # Luego usamos followup para enviar las repeticiones restantes
    for _ in range(times - 1):  # Ya hemos enviado el primer mensaje, por lo que restamos 1
        await interaction.followup.send(content)

@bot.tree.command(name="joined", description="Fecha de inclusion de un miembro (Ex: /joined juanmingla)")
async def joined(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


@bot.tree.command(name='bot', description="Mola mi bot u que? (Ex: /bot)")
async def _bot(interaction: discord.Interaction):
    await interaction.response.send_message('Es la peripocha.')


@bot.tree.command(name="join", description="Agrega el bot al chat (Ex: /join)")
async def join(interaction: discord.Interaction):
    if interaction.user.voice:
        channel = interaction.user.voice.channel
        await channel.connect()
        await interaction.response.send_message("Bot spawneando pa molestar a AiramariA")
    else:
        await interaction.response.send_message("Bot no se puede unir, metete en un canal de audio!")


@bot.tree.command(name="leave", description="Elimina el bot del chat (Ex: /leave)")
async def leave(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("El putisimo Bot se pira")
    else:
        await interaction.response.send_message("Bot no esta en el canal")

async def join_audio_channel(interaction: discord.Interaction): #   TEMPORALMENTE!!
    if interaction.user.voice:
        channel = interaction.user.voice.channel
        await channel.connect()
        return True
    else:
        await interaction.response.send_message("Bot no se puede unir, métete en un canal de audio!")
        return False

@bot.tree.command(name='audios', description="Reproduce audios en el canal en uso (Ex: /audios)")
async def audios(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if not voice_client:
        connected = await join_audio_channel(interaction)  # Llama a la función join_audio_channel si no está conectado
        if not connected:
            return
        voice_client = interaction.guild.voice_client  # Actualiza el cliente de voz

    audio_player = AudioPlayer(voice_client) 
    system_functions = SystemFunctions()  
    view = AudioView(audio_player, system_functions)  
    await interaction.response.send_message("Elige una opcion del menu:", view=view)


@bot.tree.command(name='clearaudio', description="Interrumpimos audio en reproduccion (Ex: /clearaudio)")
async def clearaudio(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client:
        voice_client.stop()
        await interaction.response.send_message("Audio interrumpido")
    else:
        await interaction.response.send_message("No hay audio reproduciendose")


# # Define un comando de barra (slash command)
# @bot.tree.command(name="hello", description="Di hola")
# async def hello(interaction: discord.Interaction):
    # await interaction.response.send_message(f'Hola {interaction.user.mention}!')

# # Define otro comando de barra (slash command)
# @bot.tree.command(name="goodbye", description="Di adi")
# async def goodbye(interaction: discord.Interaction):
    # await interaction.response.send_message(f's {interaction.user.mention}!')

# # Define un tercer comando de barra (slash command)
# @bot.tree.command(name="ping", description="Muestra el ping del bot")
# async def ping(interaction: discord.Interaction):
    # latency = bot.latency
    # await interaction.response.send_message(f'Pong! Latencia: {latency * 1000:.2f}ms')
    
# # Define un tercer comando de barra (slash command)
# @bot.tree.command(name="peroseras", description="Muestra el ping del bot")
# async def peroseras(interaction: discord.Interaction):
    # latency = bot.latency
    # await interaction.response.send_message(f'Pong! Latencia: {latency * 1000:.2f}ms')

bot.run(bottoken)
