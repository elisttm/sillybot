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
		try:
			await ctx.trigger_typing()
			tommypic=random.choice(os.listdir("images/tommy"))
			await ctx.send(file=discord.File(f"images/tommy/{tommypic}"))
		except Exception as e:
			await ctx.send(f"> ⚠️ ⠀unable to fetch an image! {e}")

	@commands.command()
	async def floppa(self, ctx):
		try:
			await ctx.trigger_typing()
			floppapic=random.choice(os.listdir("images/floppas"))
			await ctx.send(file=discord.File(f"images/floppas/{floppapic}"))
		except Exception as e:
			await ctx.send(f"> ⚠️ ⠀unable to fetch an image! {e}")

	
	@commands.command()
	async def sex(self, ctx):
		sexmsg = random.choice(tt.sex)
		try:
			await ctx.author.send(sexmsg)
		except Exception as e:
			await ctx.send(f"nope ({e})")

# 		========================

def setup(bot):
	bot.add_cog(fun(bot))
	