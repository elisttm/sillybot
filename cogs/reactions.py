import discord
import pickle
from discord.ext import commands
import data.constants as tt

# 		========================

class reactions(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	# 		========================

	@commands.Cog.listener()
	async def on_message(self, message):
	#	if "doing stuff" in message.content:
	#		await ctx.send(message.channel, 'im stuff')
		if 'y/n' in message.content.lower():
			await message.add_reaction('👍')
			await message.add_reaction('👎')
#		if 'u/d' in message.content.lower():
#			try:
#				await message.add_reaction(self.bot.get_emoji(id))
#				await message.add_reaction(self.bot.get_emoji(id))
#			except:
#				pass
#		if message.author.id == 338292198866944002 and message.channel.id == 697587669051637760:
#				await message.add_reaction('😐')

	# 		========================

def setup(bot):
	bot.add_cog(reactions(bot))