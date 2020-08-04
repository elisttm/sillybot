import discord
import re
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

class fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
# 		========================

	@commands.command()
	async def say(self, ctx, *, botsay=None):
		try:
			if botsay is None:
				await ctx.send("```⚠️ ⠀please specify what you want me to say!```")
			else:
				botsay = botsay.replace("@everyone", "@\u200beveryone")
				botsay = botsay.replace("@here", "@\u200bhere")
				tt.l = f"[{tt._t()}] '{ctx.author}' in '{ctx.guild.name}' said '{botsay}'"
				await ctx.send(botsay)
				await self.bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)
		except Exception as e: await ctx.send(tt.msg_e.format(e))

	@commands.command(aliases=['cat'])
	async def randomcat(self, ctx):
		try:
			await ctx.trigger_typing()
			catdir=random.choice(os.listdir("media"))
			catpic=random.choice(os.listdir(f"media/{catdir}"))
			await ctx.send(file=discord.File(f"media/{catdir}/{catpic}"))
		except Exception as e: await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def tommy(self, ctx, size = None):
		try:
			await ctx.trigger_typing()
			if size == 'size': await ctx.send(dirsize(dir = tommydir))
			else: await ctx.send(file=discord.File(randpic(dir = tommydir)))
		except Exception as e: await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def floppa(self, ctx, size = None):
		try:
			await ctx.trigger_typing()
			if size == 'size': await ctx.send(dirsize(dir = floppadir))
			else: await ctx.send(file=discord.File(randpic(dir = floppadir)))
		except Exception as e: await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def gloop(self, ctx, size = None):
		try:
			await ctx.trigger_typing()
			if size == 'size': await ctx.send(dirsize(dir = gloopdir))
			else: await ctx.send(file=discord.File(randpic(dir = gloopdir)))
		except Exception as e: await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def nori(self, ctx, size = None):
		try:
			await ctx.trigger_typing()
			if size == 'size': await ctx.send(dirsize(dir = noridir))
			else: await ctx.send(file=discord.File(randpic(dir = noridir)))
		except Exception as e: await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def mish(self, ctx, size = None):
		try:
			await ctx.trigger_typing()
			if size == 'size': await ctx.send(dirsize(dir = mishdir))
			else: await ctx.send(file=discord.File(randpic(dir = mishdir)))
		except Exception as e: await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def lucas(self, ctx, size = None):
		try:
			await ctx.trigger_typing()
			if size == 'size': await ctx.send(dirsize(dir = lucasdir))
			else: await ctx.send(file=discord.File(randpic(dir = lucasdir)))
		except Exception as e: await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def android(self, ctx):
		await ctx.send('https://cdn.discordapp.com/attachments/697587669051637760/738170761193324584/android.mp4')

	@commands.command()
	async def iphone(self, ctx):
		await ctx.send("https://www.youtube.com/watch?v=S_IAqwrvEuU")

	@commands.command()
	async def sex(self, ctx):
		try: await ctx.author.send("Rawr x3 nuzzles how are you pounces on you you're so warm o3o notices you have a bulge o: someone's happy ;) nuzzles your necky wecky~ murr~ hehehe rubbies your bulgy wolgy you're so big :oooo rubbies more on your bulgy wolgy it doesn't stop growing ·///· kisses you and lickies your necky daddy likies (; nuzzles wuzzles I hope daddy really likes $: wiggles butt and squirms I want to see your big daddy meat~ wiggles butt I have a little itch o3o wags tail can you please get my itch~ puts paws on your chest nyea~ its a seven inch itch rubs your chest can you help me pwease squirms pwetty pwease sad face I need to be punished runs paws down your chest and bites lip like I need to be punished really good~ paws on your bulge as I lick my lips I'm getting thirsty. I can go for some milk unbuttons your pants as my eyes glow you smell so musky :v licks shaft mmmm~ so musky drools all over your cock your daddy meat I like fondles Mr. Fuzzy Balls hehe puts snout on balls and inhales deeply oh god im so hard~ licks balls punish me daddy~ nyea~ squirms more and wiggles butt I love your musky goodness bites lip please punish me licks lips nyea~ suckles on your tip so good licks pre of your cock salty goodness~ eyes role back and goes balls deep mmmm~ moans and suckles")
		except Exception as e: await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def fq(self, ctx):
		user = ctx.author
		await user.send_friend_request()

#	@commands.command()
#	async def isaac(self, ctx):
#		if ctx.message.author.id == 503351101236576276:
#			await ctx.guild.kick(self.bot.get_user(503351101236576276), reason="isaac")
#			await ctx.send("XD")

# 		========================

def setup(bot):
	bot.add_cog(fun(bot))
	