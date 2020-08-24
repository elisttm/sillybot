import discord
import os
import random
from discord.ext import commands
import data.constants as tt

# 		========================

floppadir = 'media/floppas'
tommydir = 'media/tommy'
gloopdir = 'media/gloop'
noridir = 'media/nori'
mishdir = 'media/mish'
lucasdir = 'media/lucas'

def randpic(dir = ''):
	pic=random.choice(os.listdir(dir))
	return f"{dir}/{pic}"

def dirsize(dir = ''):
	path, dirs, files = next(os.walk(dir))
	size = 0
	for path, dirs, files in os.walk(dir):
		for f in files:
			fp = os.path.join(path, f)
			size += os.path.getsize(fp)
	size0 = round(size / 100000) / 10
	return f"{len(files)} ({size0} MB)"

class cats(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
# 		========================
	
	@commands.command()
	async def cat(self, ctx):
		try:
			await ctx.trigger_typing()
			catdir=random.choice(os.listdir("media"))
			catpic=random.choice(os.listdir(f"media/{catdir}"))
			await ctx.send(file=discord.File(f"media/{catdir}/{catpic}"))
		except Exception as e: 
			await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def tommy(self, ctx, size = None):
		try:
			await ctx.trigger_typing()
			if size == 'size': await ctx.send(dirsize(dir = tommydir))
			else: await ctx.send(file=discord.File(randpic(dir = tommydir)))
		except Exception as e: 
			await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def floppa(self, ctx, size = None):
		try:
			await ctx.trigger_typing()
			if size == 'size': await ctx.send(dirsize(dir = floppadir))
			else: await ctx.send(file=discord.File(randpic(dir = floppadir)))
		except Exception as e: 
			await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def gloop(self, ctx, size = None):
		try:
			await ctx.trigger_typing()
			if size == 'size': await ctx.send(dirsize(dir = gloopdir))
			else: await ctx.send(file=discord.File(randpic(dir = gloopdir)))
		except Exception as e: 
			await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def nori(self, ctx, size = None):
		try:
			await ctx.trigger_typing()
			if size == 'size': await ctx.send(dirsize(dir = noridir))
			else: await ctx.send(file=discord.File(randpic(dir = noridir)))
		except Exception as e: 
			await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def mish(self, ctx, size = None):
		try:
			await ctx.trigger_typing()
			if size == 'size': await ctx.send(dirsize(dir = mishdir))
			else: await ctx.send(file=discord.File(randpic(dir = mishdir)))
		except Exception as e: 
			await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def lucas(self, ctx, size = None):
		try:
			await ctx.trigger_typing()
			if size == 'size': await ctx.send(dirsize(dir = lucasdir))
			else: await ctx.send(file=discord.File(randpic(dir = lucasdir)))
		except Exception as e: 
			await ctx.send(tt.msg_e.format(e))

# 		========================

def setup(bot):
	bot.add_cog(cats(bot))