import discord
import os
import json
import asyncio, aiohttp
from io import BytesIO, StringIO
from discord.ext import commands
import data.constants as tt

# 		========================

class funcs():
	def __init__(self, bot):
		self.bot = bot

	async def send_log(self, log:str, prefix:str = '', show_prefix = True):
		if show_prefix == True: 
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
				if 'general' in guild_data:
					if 'prefix' in guild_data['general']:
						return guild_data['general']['prefix']
			return tt.p
		except:
			return tt.p

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