import discord
import re
import os
import random
import ffmpeg
from discord.ext import commands
from discord.utils import get
from discord import opus
import data.constants as tt

FFMPEG_PATH = '/home/runner/trashbot/node_modules/ffmpeg-static/ffmpeg'
if not discord.opus.is_loaded():
	discord.opus.load_opus("libopus.so.0.8.0")

# 		========================

class soundboard(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
# 		========================

	@commands.command(pass_context=True, aliases=['j', 'joi'])
	async def join(self, ctx):
		channel = ctx.message.author.voice.channel
		voice = get(self.bot.voice_clients, guild=ctx.guild)
		if voice.is_connected():
			await voice.move_to(channel)
		else:
			voice = await channel.connect()

	@commands.command()
	async def dc(self, ctx):
		pass

	@commands.command()
	async def vine(self, ctx):
		voice = get(self.bot.voice_clients, guild=ctx.guild)
		print("vine boom sound")
		voice.play(discord.FFmpegPCMAudio(executable=FFMPEG_PATH, source='./media/sounds/vineboom.mp3'))

# 		========================

def setup(bot):
	bot.add_cog(soundboard(bot))
	