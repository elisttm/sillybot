import discord
import urllib
from urllib import request
from discord.ext import commands
import data.constants as tt

# 		========================

cat_api = f"{tt.cat_site}/api"

def get_cat_url(name:str):
	return request.urlopen(f'{cat_api}/{name}').read().decode('utf8')

class cats(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
# 		========================

	@commands.command()
	async def cat(self, ctx):
		try:
			await ctx.trigger_typing()
			await ctx.send(get_cat_url(''))
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	async def tommy(self, ctx):
		try:
			await ctx.trigger_typing()
			await ctx.send(get_cat_url('tommy'))
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	async def floppa(self, ctx):
		try:
			await ctx.trigger_typing()
			await ctx.send(get_cat_url('floppa'))
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	async def gloop(self, ctx):
		try:
			await ctx.trigger_typing()
			await ctx.send(get_cat_url('gloop'))
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	async def nori(self, ctx):
		try:
			await ctx.trigger_typing()
			await ctx.send(get_cat_url('nori'))
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	async def mish(self, ctx):
		try:
			await ctx.trigger_typing()
			await ctx.send(get_cat_url('mish'))
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	async def lucas(self, ctx):
		try:
			await ctx.trigger_typing()
			await ctx.send(get_cat_url('lucas'))
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	async def marley(self, ctx):
		try:
			await ctx.trigger_typing()
			await ctx.send(get_cat_url('marley'))
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	async def spock(self, ctx):
		try:
			await ctx.trigger_typing()
			await ctx.send(get_cat_url('spock'))
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

# 		========================

def setup(bot):
	bot.add_cog(cats(bot))