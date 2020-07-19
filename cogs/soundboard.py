import discord
import re
import os
import random
from discord.ext import commands
from discord.utils import get
import data.constants as tt

# 		========================

class soundboard(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
# 		========================

	@commands.command(pass_context=True, aliases=['j', 'joi'])
	async def join(self, ctx):
		channel = ctx.message.author.voice.channel
		voice = get(self.bot.voice_clients, guild=ctx.guild)
		if voice and voice.is_connected():
			await voice.move_to(channel)
		else:
			voice = await channel.connect()
		await voice.disconnect()
		if voice and voice.is_connected():
			await voice.move_to(channel)

# 		========================

def setup(bot):
	bot.add_cog(soundboard(bot))
	