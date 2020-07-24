import discord
import re
import os
import random
import ffmpeg
from discord.ext import commands
from discord.utils import get
from discord import opus
from discord import voice_client
import data.constants as tt

FFMPEG_PATH = '/home/runner/trashbot/node_modules/ffmpeg-static/ffmpeg'
os.system(f'chmod +777 {FFMPEG_PATH}')
if not discord.opus.is_loaded():
	discord.opus.load_opus("libopus.so.0.8.0")

# 		========================

class soundboard(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
# 		========================

#	@commands.command()
#	async def join(self, ctx):
#		channel = ctx.message.author.voice.channel
#		voice = get(self.bot.voice_clients, guild=ctx.guild)
#		await channel.connect()

#	@commands.command()
#	async def dc(self, ctx):
#		await self.bot.voice_clients[0].disconnect()

	@commands.command()
	async def connect(self, ctx):
		player = self.bot.get_channel(ctx.author.voice.channel.id)
		await player.connect()
	
	@commands.command()
	async def disconnect(self, ctx):
		player = ctx.guild.voice_client
		await player.disconnect()

	@commands.command(hidden=True)
	async def vine(self, ctx):
		player = ctx.guild.voice_client
		player.play(discord.FFmpegPCMAudio(executable=FFMPEG_PATH, source='media/sounds/vineboom.mp3'))

# 		========================

def setup(bot):
	bot.add_cog(soundboard(bot))
	