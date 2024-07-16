import discord
from discord import FFmpegPCMAudio
from discord.ui import Select, View
from discord import FFmpegPCMAudio
from discord.ext import commands
import random
import os

from src.utils import *

class SetupCommands():
    def setup_commands(bot):
        @bot.command()
        async def add(ctx, left: int, right: int):
            """Suma dos numeros (Ex: ?add 5 11)"""
            await ctx.send(left + right)

        @bot.command()
        async def roll(ctx, dice: str):
            """Tira N dados de N caras en este orden NdN (dados, caras) (Ex: ?roll 3d6)"""
            try:
                rolls, limit = map(int, dice.split('d'))
            except ValueError:
                await ctx.send('Formato incorrecto. Usa NdN!')
                return

            result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
            await ctx.send(result)

        @bot.command(description='Elige al azar entre varias opciones')
        async def choose(ctx, *choices: str):
            """Elige al azar entre varias opciones (Ex: ?choose Pizza Pasta Hamburguesa)"""
            await ctx.send(random.choice(choices))

        @bot.command()
        async def repeat(ctx, times: int, content='repeating...'):
            """Repite un mensaje varias veces"""
            for i in range(times):
                await ctx.send(content)

        @bot.command()
        async def joined(ctx, member: commands.MemberConverter):
            """Fecha de inclusion de un miembro"""
            await ctx.send(f'{member.name} se unió el {member.joined_at}')

        @bot.command(name='bot')
        async def _bot(ctx):
            """Dice si el bot es la pera limonera"""
            await ctx.send('Es la peripocha.')

        @bot.command(pass_context=True)
        async def join(ctx):
            """Agrega el bot al canal de voz"""
            connected = False
            if ctx.author.voice:
                channel = ctx.message.author.voice.channel
                await channel.connect()
                await ctx.send("Bot conectado al canal de voz.")
                connected = True
            else:
                await ctx.send("No estás en un canal de voz.")
            return connected

        @bot.command(pass_context=True)
        async def leave(ctx):
            """Saca el bot del canal de voz"""
            if ctx.voice_client:
                await ctx.guild.voice_client.disconnect()
                await ctx.send("Bot desconectado del canal de voz.")
            else:
                await ctx.send("El bot no está en un canal de voz.")

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
            """Interrumpe la reproducción de audio"""
            if ctx.voice_client:
                ctx.voice_client.stop()
                await ctx.send("Reproducción de audio interrumpida.")
            else:
                await ctx.send("No hay audio reproduciéndose.")

