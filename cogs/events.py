import discord
import os
import json
import asyncio
from discord.ext import commands, tasks
from utils import checks
from utils.funcs import funcs
import data.constants as tt

# 		========================

toggleable_reactions = ['naemt']

reactions = {
	'y/n': [tt.e['thumbsup'], tt.e['thumbsdown']],
	'u/d': [tt.e['uparrow'], tt.e['downarrow']],
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
		#if message.content.lower() in reactions:
		for _reaction in reactions:
			if _reaction in message.content.lower():
				for reaction in reactions[_reaction]: 
					await message.add_reaction(reaction)
		if self.toggleable_reactions_list['naemt'] == True:
			if (message.author.id == 338292198866944002) and (message.channel.id == 697587669051637760):
				await message.add_reaction(tt.e['neutral'])

	def starboard_embed(self, message):
		e_sb = discord.Embed(description=f"{message.content}", color=tt.clr['yellow'])
		e_sb.add_field(name="jump to message", value=f"[click here]({message.jump_url})", inline=False)
		if len(message.attachments) > 0:
			e_sb.set_image(url=message.attachments[0].url)
		e_sb.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)
		e_sb.set_footer(text=f"{message.id} ⠀| ⠀{tt.curtime()}")
		return e_sb

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if payload.member.bot:
			pass
		channel = self.bot.get_channel(payload.channel_id)
		message = await channel.fetch_message(payload.message_id)
		if (payload.emoji.is_custom_emoji()) and (payload.emoji.id == 747278013091282945) and (payload.member.id in tt.admins):
			await message.remove_reaction(payload.emoji, payload.member)
			for emoji in self.bot.get_guild(747195327530139759).emojis:
				try:
					await message.add_reaction(emoji)
					await asyncio.sleep(0.21)
				except:
					return
			return
		guild_data_path = tt.guild_data_path.format(str(message.guild.id))
		if (payload.emoji.is_unicode_emoji()) and (payload.emoji.name == "U+2B50") and (message.reactions[payload.emoji.name].count >= 5):
			if not os.path.exists(guild_data_path):
				return
			guild_data = self.load_db(guild_data_path)
			if ('channels' not in guild_data) or ('starboard' not in guild_data['channels']):
				return
			guild_starboard_path = tt.guild_starboard_path.format(str(message.guild.id))
			self.check_for_db(guild_starboard_path)
			starboard_data = self.load_db(guild_starboard_path)
			if 'a' not in starboard_data:
				starboard_data['a'] = []
			if message.id in starboard_data['a']:
				return
			starboard_data['a'].append(message.id)
			self.dump_db(guild_starboard_path, starboard_data)
			starboard_channel = self.bot.get_channel(guild_data['channels']['starboard'])
			await starboard_channel.send(embed=self.starboard_embed(message))

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