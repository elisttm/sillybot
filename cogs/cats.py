import discord
import urllib
from urllib import request
from discord.ext import commands
import data.constants as tt

# 		========================

# rework these commands to invoke the cat command with cat_name queries

def get_cat_url(name:str):
	return request.urlopen(f'{tt.cat_site}/api/{name}').read().decode('utf8')

cat_dirs = str(request.urlopen(f'http://cat.elisttm.space:7777/directories/').read())
cat_dirs = str(cat_dirs.split(' '))

class cats(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
# 		========================

	@commands.command()
	async def cat(self, ctx, cat_name:str = None):
		await ctx.trigger_typing()
		try:
			if cat_name is None:
				cat_name = ''
			else:
				cat_name = cat_name.lower()
				if cat_name not in cat_dirs:
					await ctx.send("⚠️ ⠀invalid cat directory provided")
					return
			await ctx.send(get_cat_url(cat_name))
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	async def tommy(self, ctx): await ctx.invoke(self.bot.get_command('cat'), cat_name='tommy')
	@commands.command()
	async def floppa(self, ctx): await ctx.invoke(self.bot.get_command('cat'), cat_name='floppa')
	@commands.command()
	async def gloop(self, ctx): await ctx.invoke(self.bot.get_command('cat'), cat_name='gloop')
	@commands.command()
	async def nori(self, ctx): await ctx.invoke(self.bot.get_command('cat'), cat_name='nori')
	@commands.command()
	async def mish(self, ctx): await ctx.invoke(self.bot.get_command('cat'), cat_name='mish')
	@commands.command()
	async def lucas(self, ctx): await ctx.invoke(self.bot.get_command('cat'), cat_name='lucas')
	@commands.command()
	async def marley(self, ctx): await ctx.invoke(self.bot.get_command('cat'), cat_name='marley')
	@commands.command()
	async def spock(self, ctx): await ctx.invoke(self.bot.get_command('cat'), cat_name='spock')

# 		========================

def setup(bot):
	bot.add_cog(cats(bot))