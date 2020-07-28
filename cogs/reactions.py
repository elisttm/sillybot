import discord
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
		if 'homestuck' in message.content.lower():
			await message.add_reaction('🤮')
		if 'u/d' in message.content.lower():
			try:
				await message.add_reaction(bot.get_emoji(701102030529364170))
				await message.add_reaction(bot.get_emoji(704798029256982570))
			except:
				pass

# 		========================

def setup(bot):
	bot.add_cog(reactions(bot))
	