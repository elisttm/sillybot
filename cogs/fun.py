import discord
import re
import os
import random
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

	@commands.command()
	async def tommy(self, ctx):
		await ctx.trigger_typing()
		tommypic=random.choice(os.listdir("tommy"))
		await ctx.send(file=discord.File(f"tommy/{tommypic}"))


# 		========================

def setup(bot):
	bot.add_cog(fun(bot))
	