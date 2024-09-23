import discord
from dotenv import load_dotenv
import os
from discord.ext import commands
import logging
from src.events import Events
from src.utils import *
from src.slash_commands import SetupSlashCommands

description = '''Bot de Juan (con ayuda esporadica de Sergio), pa poder meter audios y lo que nos salga de ahi.

SE ACEPTAN SUGERENCIAS, SI ALGUIEN QUIERE METER SU AUDIO QUE ME LO PASE'''

intents = discord.Intents.all()
intents.members = True
intents.message_content = True

load_dotenv()
bottoken = os.getenv('BOTTOKEN')
applicationid = os.getenv('APPLICATIONID')

bot = commands.Bot(command_prefix='?', description=description, intents=intents, application_id=applicationid, status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.watching, name = "Los Simpson"))

logger = logging.getLogger(__name__)
logging.basicConfig(filename='pibot.log', encoding='utf-8', level=logging.DEBUG)

# EVENTOS y SLASH COMMANDS
SetupSlashCommands.setup_commands(bot)
Events(bot)

bot.run(bottoken)