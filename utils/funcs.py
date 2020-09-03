import discord
import os
import pickle
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