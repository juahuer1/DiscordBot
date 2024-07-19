# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from dotenv import load_dotenv
import os
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.ui import Select, View
import random
import logging

from src.events import Events
from src.utils import *
from src.commands import SetupCommands  # Importa la función para cargar los comandos
from src.slash_commands import SetupSlashCommands


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

# EVENTOS y SLASH COMMANDS
SetupSlashCommands.setup_commands(bot)

Events(bot, serverid)

# ? COMMANDS
SetupCommands.setup_commands(bot)


bot.run(bottoken)