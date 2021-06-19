import discord
import os
import json
from discord.ext import commands
from utils import checks
from utils.funcs import funcs
import data.constants as tt

# 		========================

class moderation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.load_db = funcs.load_db
		self.dump_db = funcs.dump_db
		self.check_for_db = funcs.check_for_db
		self.send_log = funcs.send_log
		self.log_prefix = "[MODERATION]"
	
# 		========================
	
	# theres nothing here anymore lol

# 		========================

def setup(bot):
	bot.add_cog(moderation(bot))