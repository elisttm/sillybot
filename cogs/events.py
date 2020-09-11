import discord
import os
import json
from discord.ext import commands
from utils import checks
from utils.funcs import funcs
import data.constants as tt

# 		========================

class events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.load_db = funcs.load_db
		self.dump_db = funcs.dump_db
		self.check_for_db = funcs.check_for_db
	
	def parse_event_msg(self, bot, message, user_id, guild_id):
		user = self.bot.get_user(user_id)
		guild = self.bot.get_guild(guild_id)
		message = message.replace('[server', '[guild').replace('[@user]', '[user-mention]')
		return message.replace('[user]', f'{user}').replace('[user-name]', user.name).replace('[user-discriminator]', user.discriminator).replace('[user-id]', str(user.id)).replace('[user-mention]', user.mention).replace('[guild]', guild.name)

	# 		========================

	@commands.Cog.listener()
	async def on_member_join(self, user):
		if user == self.bot.user:
			pass
		guild_data_path = tt.guild_data_path.format(str(user.guild.id))
		if not os.path.exists(guild_data_path):
			return
		guild_data = self.load_db(guild_data_path)
		if ('events' not in guild_data) or ('join' not in guild_data['events']):
			return
		if ('roles' in guild_data) and ('default' in guild_data['roles']):
			await user.add_roles(user.guild.get_role(guild_data['roles']['default']))
		await self.bot.get_channel(guild_data['channels']['msgchannel']).send(self.parse_event_msg(self.bot, guild_data['events']['join'], user.id, user.guild.id))

	@commands.Cog.listener()
	async def on_member_remove(self, user):
		if user == self.bot.user:
			pass
		guild_data_path = tt.guild_data_path.format(str(user.guild.id))
		if not os.path.exists(guild_data_path):
			return
		guild_data = self.load_db(guild_data_path)
		if ('events' not in guild_data) or ('leave' not in guild_data['events']):
			return
		await self.bot.get_channel(guild_data['channels']['msgchannel']).send(self.parse_event_msg(self.bot, guild_data['events']['leave'], user.id, user.guild.id))

	@commands.Cog.listener()
	async def on_member_ban(self, guild, user):
		guild_data_path = tt.guild_data_path.format(str(guild.id))
		if not os.path.exists(guild_data_path):
			return
		guild_data = self.load_db(guild_data_path)
		if ('events' not in guild_data) or ('ban' not in guild_data['events']):
			return
		await self.bot.get_channel(guild_data['channels']['msgchannel']).send(self.parse_event_msg(self.bot, guild_data['events']['ban'], user.id, user.guild.id))

	# 		========================

def setup(bot):
	bot.add_cog(events(bot))