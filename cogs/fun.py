import discord
import re
from discord.ext import commands
import data.constants as tt

# 		========================

class fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
# 		========================

	@commands.command()
	async def say(self, ctx, *, botsay=None):
		if botsay is None:
			await ctx.send("> ⚠️ ⠀please specify what you want me to say!")
		else:
			botsay = botsay.replace("@everyone", "@\u200beveryone")
			botsay = botsay.replace("@here", "@\u200bhere")
			tt.l = f"[{tt._t()}] '{ctx.author}' in '{ctx.guild.name}' said '{botsay}'"
			await ctx.send(botsay)
			await self.bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)

# 		========================

def setup(bot):
	bot.add_cog(fun(bot))
	