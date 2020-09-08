import discord
import json
from discord.ext import commands
from utils import checks
from utils.funcs import funcs
import data.constants as tt

# 		========================

toggleable_reactions = ['naemt']

class reactions(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.load_db = funcs.load_db
		self.dump_db = funcs.dump_db
	
	# 		========================

	@commands.Cog.listener()
	async def on_message(self, message):
		reactions_list = self.load_db(tt.reactions_db)
		if 'y/n' in message.content.lower():
			await message.add_reaction('👍')
			await message.add_reaction('👎')
		if 'u/d' in message.content.lower():
			await message.add_reaction('🔼')
			await message.add_reaction('🔽')
		if reactions_list['naemt'] == True:
			if (message.author.id == 338292198866944002) and (message.channel.id == 697587669051637760):
				await message.add_reaction('😐')

	@commands.command()
	@checks.is_admin()
	async def reaction(self, ctx, param = None, name = None):
		reactions_list = self.load_db(tt.reactions_db)
		if (param == None) and (name == None):
			await ctx.send(str(reactions_list))
			return
		if name == None:
			raise(commands.UserInputError)
			return
		if name not in toggleable_reactions:
			raise(commands.UserInputError)
			return
		elif param == 'enable':
			reactions_list[name] = True 
		elif param == 'disable':
			reactions_list[name] = False
		else:
			raise(commands.UserInputError)
			return
		self.dump_db(tt.reactions_db, reactions_list)
		await ctx.message.add_reaction('✅')

	# 		========================

def setup(bot):
	bot.add_cog(reactions(bot))