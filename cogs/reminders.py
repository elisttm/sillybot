import discord
import json
import random 
import time, datetime
from pytz import timezone
from discord.ext import commands
from utils import checks
from utils.funcs import funcs
import data.constants as tt

# 		========================

class reminders(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.load_db = funcs.load_db
		self.dump_db = funcs.dump_db
		self.check_for_db = funcs.check_for_db
		self.reminders_list = self.load_db(tt.reminders_db)

# 		========================


# 		========================

def setup(bot):
  bot.add_cog(reminders(bot))