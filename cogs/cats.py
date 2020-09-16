import discord
import json
import urllib, urllib.request
import random
from discord.ext import commands
from utils import checks
from utils.funcs import funcs
import data.constants as tt

# 		========================

cat_url = 'http://cat.elisttm.space:7777'

cat_json = json.loads(tt.get_url(cat_url+'/api/all'))
cat_dirs = (str(tt.get_url(cat_url+'/directories/'))).split(' ')

def get_cat_url(cat_name:str):
	if cat_name == '':
		cat_name = random.choice(cat_dirs)
	label = 'cats' + cat_name
	return f'{cat_url}/static/cat/{cat_name}/{funcs.smart_random(cat_json[cat_name], label)}'

class cats(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
# 		========================

	@commands.command()
	async def cat(self, ctx, cat_name:str = ''):
		await ctx.trigger_typing()
		try:
			cat_name = cat_name.lower()
			if cat_name == 'list':
				await ctx.send(tt.i+f"valid cat directories: {', '.join(cat_dirs)}")
				return
			if (cat_name not in cat_dirs) and (cat_name != ''):
				await ctx.send(tt.w+f"invalid cat directory provided! ({', '.join(cat_dirs)})")
				return
			await ctx.send(get_cat_url(cat_name))
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	async def tommy(self, ctx): 
		await ctx.invoke(self.bot.get_command('cat'), cat_name='tommy')
	@commands.command()
	async def floppa(self, ctx): 
		await ctx.invoke(self.bot.get_command('cat'), cat_name='floppa')
	@commands.command()
	async def gloop(self, ctx): 
		await ctx.invoke(self.bot.get_command('cat'), cat_name='gloop')
	@commands.command()
	async def nori(self, ctx): 
		await ctx.invoke(self.bot.get_command('cat'), cat_name='nori')
	@commands.command()
	async def mish(self, ctx): 
		await ctx.invoke(self.bot.get_command('cat'), cat_name='mish')
	@commands.command()
	async def lucas(self, ctx): 
		await ctx.invoke(self.bot.get_command('cat'), cat_name='lucas')
	@commands.command()
	async def marley(self, ctx): 
		await ctx.invoke(self.bot.get_command('cat'), cat_name='marley')
	@commands.command()
	async def spock(self, ctx): 
		await ctx.invoke(self.bot.get_command('cat'), cat_name='spock')
	@commands.command()
	async def thomas(self, ctx): 
		await ctx.invoke(self.bot.get_command('cat'), cat_name='thomas')

# 		========================

def setup(bot):
	bot.add_cog(cats(bot))