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

# CLASES

# Crear una vista personalizada con un menu de seleccion
class AudioSelect(discord.ui.Select):
    def __init__(self, audio_player, system_functions):
        self.audio_player = audio_player
        self.system_functions = system_functions
        archivos = system_functions.list_audios()

        options = [];
        
        for archivo in archivos:
            option = discord.SelectOption(label=f"{archivo}", description="Esta es la opcion 1")
            options.append(option)
        
        super().__init__(placeholder="Elige una opcion...", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        try:
            audio_selected = self.values[0]
            await interaction.response.defer()
            await self.audio_player.play_audio(audio_selected)
        except Exception as e:
            # En caso de error, enviar un mensaje de error al usuario
            await interaction.response.send_message(f'Ocurrio un error: {str(e)}', ephemeral=True)

class AudioView(discord.ui.View):
    def __init__(self, audio_player, system_functions):
        super().__init__()
        self.add_item(AudioSelect(audio_player, system_functions))
        
class AudioPlayer:
    def __init__(self, voice_client):
        self.voice_client = voice_client
        
    async def play_audio(self, audio_selected):
        if not self.voice_client or not self.voice_client.is_connected():
            raise RuntimeError("El bot no esta conectado a ningun canal de voz.")

        source = FFmpegPCMAudio('./Audios/'+audio_selected)
        self.voice_client.play(source)
      
class SystemFunctions:
    def __init__(self):
        self.list_audios()
        
    def list_audios(self):
        archivos = os.listdir("./Audios")
        return archivos


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

# Define un comando de barra (slash command)
@bot.tree.command(name="hello", description="Di hola")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hola {interaction.user.mention}!')

# Define otro comando de barra (slash command)
@bot.tree.command(name="goodbye", description="Di adi")
async def goodbye(interaction: discord.Interaction):
    await interaction.response.send_message(f's {interaction.user.mention}!')

# Define un tercer comando de barra (slash command)
@bot.tree.command(name="ping", description="Muestra el ping del bot")
async def ping(interaction: discord.Interaction):
    latency = bot.latency
    await interaction.response.send_message(f'Pong! Latencia: {latency * 1000:.2f}ms')
    
# Define un tercer comando de barra (slash command)
@bot.tree.command(name="peroseras", description="Muestra el ping del bot")
async def peroseras(interaction: discord.Interaction):
    latency = bot.latency
    await interaction.response.send_message(f'Pong! Latencia: {latency * 1000:.2f}ms')

bot.run(bottoken)
