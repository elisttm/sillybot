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

	@commands.command(pass_context=True, aliases=['j', 'joi'])
	async def join(self, ctx):
		channel = ctx.message.author.voice.channel
		voice = get(self.bot.voice_clients, guild=ctx.guild)
		await channel.connect()

	@commands.command()
	async def dc(self, ctx):
		await self.bot.voice_clients[0].disconnect()

	@commands.command()
	async def vine(self, ctx):
		try:
			channel = ctx.message.author.voice.channel
			voice = get(self.bot.voice_clients, guild=ctx.guild)
			await channel.connect()
		except:
			pass
		ctx.voice_client.play(discord.FFmpegPCMAudio(executable=FFMPEG_PATH, source='media/sounds/vineboom.mp3', use_avconv=False))
		print("k;gklekl;nsdfjzxsadfjkl;dscgkl;dcsvjkl;n")

# 		========================

def setup(bot):
	bot.add_cog(soundboard(bot))
	