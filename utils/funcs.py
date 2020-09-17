import discord
import os
import json
import random
from io import BytesIO, StringIO
from discord.ext import commands
import data.constants as tt

# 		========================

class funcs():
	def __init__(self, bot):
		self.bot = bot

# 		========================

	async def send_log(self, log:str, prefix:str = '', show_prefix = True):
		if show_prefix == True: 
			if prefix != '': 
				prefix = prefix + ' '
			log_msg = f"[{tt._t()}] {prefix}{log}"
		else: 
			log_msg = log
		print(log_msg)
		await self.bot.get_channel(tt.logs).send(f"```{log_msg}```")

	def determine_prefix(self, message):
		try:
			guild_data_path = tt.guild_data_path.format(str(message.guild.id))
			if os.path.exists(guild_data_path):
				guild_data = funcs.load_db(guild_data_path)
				if ('general' in guild_data) and ('prefix' in guild_data['general']):
					return guild_data['general']['prefix']
			return tt.p
		except:
			return tt.p

	def user_num(self, bot):
		user_num = 0
		for user in self.bot.users:
			if user.bot is True: 
				continue 
			else: 
				user_num += 1
		return user_num

	def smart_random(_list, label:str, max_per:int=None):
		if max_per is None:
			max_per = ((round(len(_list)/2))+1)
		if label not in tt.smart_random_dict:
			tt.smart_random_dict[label] = []
		choice = random.choice(_list)
		while choice in tt.smart_random_dict[label]:
			choice = random.choice(_list)
		tt.smart_random_dict[label].append(choice)
		if len(tt.smart_random_dict[label]) > max_per:
			tt.smart_random_dict[label].pop(0)
		return choice

#			-----  DATABASE MANAGEMENT  -----

	def load_db(path:str):
		with open(path) as data_json: 
			return json.load(data_json)

	def dump_db(path:str, data):
		with open(path, 'w') as outfile: 
			json.dump(data, outfile)

	def check_for_db(path:str):
		if not os.path.exists(path):
			os.mknod(path)	
			data = {}
			with open(path, 'w') as outfile: 
				json.dump(data, outfile)
			print(f"[{tt._t()}] created file '{path}'")

# 		========================
