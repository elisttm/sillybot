import discord
import json
import random 
import time, datetime
from pytz import timezone
from discord.ext import commands, tasks
from discord.utils import sleep_until
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
		
	def load_reminders(self):
		reminders_list = self.load_db(tt.reminders_db)
		reminders_list = sorted(reminders_list)
		return reminders_list
		
		self.reminders_list = self.load_reminders(self)

# 		========================

	# create loop that uses sleep_until or something based off datetime object to send a message

	@tasks.loop(seconds=1)
	async def send_reminder(self):
		reminder = self.reminders_list[0]
		sleep_until(self.reminders_list[reminder]['end_time'])
		channel = self.bot.get_channel(self.reminders_list[reminder]['channel'])
		await channel.send('reminder: '+self.reminders_list[reminder]['content'])

# 		========================

def setup(bot):
  bot.add_cog(reminders(bot))