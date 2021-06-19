import discord
import json
import urllib, urllib.request
import random
from discord.ext import commands
from utils import checks
from utils.funcs import funcs
import data.constants as tt

# 		========================

cat_dirs = []

class cats(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
		self.cat_json = json.loads(tt.get_url(tt.cat_url+'/api/all'))
		self.cat_dirs = json.loads(tt.get_url(tt.cat_url+'/directories/'))
		self.smart_random = funcs.smart_random
		
		cat_dirs = self.cat_dirs
		
	async def get_cat_url(self, cat_name:str):
		if cat_name == '':
			cat_name = random.choice(self.cat_dirs)
		label = 'cat' + cat_name
		return f'{tt.cat_url}/static/cat/{cat_name}/{self.smart_random(self.cat_json[cat_name], label)}'

# 		========================

	@commands.command()
	async def cat(self, ctx, cat_name:str = ''):
		await ctx.trigger_typing()
		cat_name = cat_name.lower()
		try:
			if (cat_name == 'list') or ((cat_name not in self.cat_dirs) and (cat_name != '')):
				await ctx.send(tt.i+f"list of valid cat directories: {', '.join(self.cat_dirs)}")
				return
			cat_image = await self.get_cat_url(cat_name)
			await ctx.send(cat_image)
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	# i want it to be known this is the stupidest workaround i have ever made and the fact it works baffles me
	@commands.command(aliases=['floppa','tommy','gloop','mish','spock','marley','lucas','nori','thomas', 'max', 'jim', 'gupitaro', 'mona', 'xena'])
	async def _cat_name(self, ctx):
		await ctx.invoke(self.bot.get_command('cat'), cat_name=ctx.invoked_with)

# 		========================

def setup(bot):
	bot.add_cog(cats(bot))
