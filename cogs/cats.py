import discord
import os
import random
import urllib
from urllib import request
from discord.ext import commands
import data.constants as tt

# 		========================

cat_site = "http://cat.elisttm.space:7777"
cat_api = f"{cat_site}/api"

def requesturl(name:str):
	return request.urlopen(f'{cat_api}/{name}').read().decode('utf8')

class cats(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
# 		========================

	@commands.command()
	async def cat(self, ctx, size = None):
		try:
			await ctx.trigger_typing()
			await ctx.send(requesturl(''))
		except Exception as e: await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def tommy(self, ctx, size = None):
		try:
			await ctx.trigger_typing()
			await ctx.send(requesturl('tommy'))
		except Exception as e: await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def floppa(self, ctx, size = None):
		try:
			await ctx.trigger_typing()
			await ctx.send(requesturl('floppa'))
		except Exception as e: await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def gloop(self, ctx, size = None):
		try:
			await ctx.trigger_typing()
			await ctx.send(requesturl('gloop'))
		except Exception as e: await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def nori(self, ctx, size = None):
		try:
			await ctx.trigger_typing()
			await ctx.send(requesturl('nori'))
		except Exception as e: await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def mish(self, ctx, size = None):
		try:
			await ctx.trigger_typing()
			await ctx.send(requesturl('mish'))
		except Exception as e: await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def lucas(self, ctx, size = None):
		try:
			await ctx.trigger_typing()
			await ctx.send(requesturl('lucas'))
		except Exception as e: await ctx.send(tt.msg_e.format(e))

# 		========================

def setup(bot):
	bot.add_cog(cats(bot))