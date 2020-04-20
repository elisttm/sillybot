import discord
from discord.ext import commands
import data.constants as tt

# 		========================

class fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
# 		========================



# 		========================

def setup(bot):
	bot.add_cog(fun(bot))
	