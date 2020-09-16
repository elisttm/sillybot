import discord
import os
import json
from discord.ext import commands, tasks
from utils import checks
from utils.funcs import funcs
import data.constants as tt

# 		========================

toggleable_reactions = ['naemt']

reactions_list = {
	'y/n': [
		tt.e['thumbsup'], 
		tt.e['thumbsdown']
	],
	'u/d': [
		tt.e['up'], 
		tt.e['down']
	],
}

class events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.load_db = funcs.load_db
		self.dump_db = funcs.dump_db
		self.check_for_db = funcs.check_for_db
		self.send_log = funcs.send_log
		self.log_prefix = "[EVENTS]"

		self.toggleable_reactions_list = self.load_db(tt.reactions_db)
	
	def parse_event_msg(self, bot, message, user_id, guild_id):
		user = self.bot.get_user(user_id)
		guild = self.bot.get_guild(guild_id)
		message = message.replace('[server', '[guild').replace('[@user]', '[user-mention]')
		return message.replace('[user]', f'{user}').replace('[user-name]', user.name).replace('[user-discriminator]', user.discriminator).replace('[user-id]', str(user.id)).replace('[user-mention]', user.mention).replace('[guild]', guild.name)

	# 		========================

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.content.lower() in reactions_list:
			for reaction in reactions_list[message.content.lower()]: 
				await message.add_reaction(reaction)
		if self.toggleable_reactions_list['naemt'] == True:
			if (message.author.id == 338292198866944002) and (message.channel.id == 697587669051637760):
				await message.add_reaction(tt.e['neutral'])

	@commands.Cog.listener()
	async def on_member_join(self, user):
		if user == self.bot.user:
			pass
		guild_data_path = tt.guild_data_path.format(str(user.guild.id))
		if not os.path.exists(guild_data_path):
			return
		guild_data = self.load_db(guild_data_path)
		if ('messages' not in guild_data) or ('join' not in guild_data['messages']):
			return
		if ('roles' in guild_data) and ('default' in guild_data['roles']):
			await user.add_roles(user.guild.get_role(guild_data['roles']['default']))
		if ('channels' in guild_data) and ('msgchannel' in guild_data['channels']):
			channel = self.bot.get_channel(guild_data['channels']['msgchannel'])
		else:
			if user.guild.system_channel is not None:
				channel = user.guild.system_channel
			else:
				return
		await channel.send(self.parse_event_msg(self.bot, guild_data['messages']['join'], user.id, user.guild.id))

	@commands.Cog.listener()
	async def on_member_remove(self, user):
		if user == self.bot.user:
			pass
		guild_data_path = tt.guild_data_path.format(str(user.guild.id))
		if not os.path.exists(guild_data_path):
			return
		guild_data = self.load_db(guild_data_path)
		if ('messages' not in guild_data) or ('leave' not in guild_data['messages']):
			return
		if ('channels' in guild_data) and ('msgchannel' in guild_data['channels']):
			channel = self.bot.get_channel(guild_data['channels']['msgchannel'])
		else:
			if user.guild.system_channel is not None:
				channel = user.guild.system_channel
			else:
				return
		await channel.send(self.parse_event_msg(self.bot, guild_data['messages']['leave'], user.id, user.guild.id))

	@commands.Cog.listener()
	async def on_member_ban(self, guild, user):
		guild_data_path = tt.guild_data_path.format(str(guild.id))
		if not os.path.exists(guild_data_path):
			return
		guild_data = self.load_db(guild_data_path)
		if ('messages' not in guild_data) or ('ban' not in guild_data['messages']):
			return
		if ('channels' in guild_data) and ('msgchannel' in guild_data['channels']):
			channel = self.bot.get_channel(guild_data['channels']['msgchannel'])
		else:
			if user.guild.system_channel is not None:
				channel = user.guild.system_channel
			else:
				return
		await channel.send(self.parse_event_msg(self.bot, guild_data['messages']['ban'], user.id, user.guild.id))

	@commands.command()
	@checks.is_admin()
	async def togglereaction(self, ctx, name=None):
		if name == None:
			await ctx.send(str(self.toggleable_reactions_list))
			return
		if name not in toggleable_reactions:
			raise(commands.UserInputError)
			return
		if self.toggleable_reactions_list[name] == True: 
			self.toggleable_reactions_list[name] = False 
		else: 
			self.toggleable_reactions_list[name] = True 
		self.dump_db(tt.reactions_db, self.toggleable_reactions_list)
		await ctx.message.add_reaction(tt.e['check'])

	# 		========================

def setup(bot):
	bot.add_cog(events(bot))