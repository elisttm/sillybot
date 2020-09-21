import discord
import os
import json
import asyncio
import re
import time, datetime
from discord.utils import get
from discord.ext import commands, tasks
from utils import checks
from utils.funcs import funcs
import data.constants as tt

# 		========================

t_reactions = {
	'naemt'
}
s_reactions = {
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

	# 		========================

	def starboard_header(self, message):
		star_count = message.reactions['⭐'].count
		if star_count < 5: star = '⭐'
		if star_count >= 5: star = '🌟'
		if star_count >= 10: star = '💫'
		return f"{star}{star_count} {message.channel.mention}" 
			
	def starboard_embed(self, message):
		e_sb = discord.Embed(description=message.content, color=tt.clr['yellow'])
		e_sb.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)
		e_sb.set_footer(text=f"{message.id} ⠀| ⠀{tt.curtime()}")
		e_sb.add_field(name="jump to message", value=f"[click here]({message.jump_url})")
		if len(message.attachments) > 0:
			e_sb.set_image(url=message.attachments[0].url)
		return e_sb
				
	async def starboard(self, guild_data, message, channel, payload):
		starboard_channel = self.bot.get_channel(guild_data['channels']['starboard'])
		guild_starboard_path = tt.guild_starboard_path.format(str(message.guild.id))
		self.check_for_db(guild_starboard_path)
		starboard_data = self.load_db(guild_starboard_path)
		if str(message.id) in starboard_data:
			await self.starboard_update(starboard_data, message, starboard_channel)
			return
		starboard_message = await starboard_channel.send(content=self.starboard_header(message), embed=self.starboard_embed(message))
		starboard_data[str(message.id)] = starboard_message.id
		self.dump_db(guild_starboard_path, starboard_data)
		return
		
	async def starboard_update(self, data, message, starboard_channel):
		embed = self.starboard_embed(message)
		header = self.starboard_header(message)
		starboard_message = await starboard_channel.fetch_message(data[str(message.id)])
		if (header == starboard_message.content) and (embed == starboard_message.embeds[0]):
			return
		await starboard_message.edit(content=header, embed=embed)
		return

	async def blackdude_reactions(self, message, channel, member, emoji):
		await message.remove_reaction(emoji, member)
		for emoji in self.bot.get_guild(747195327530139759).emojis:
			try:
				await message.add_reaction(emoji)
				await asyncio.sleep(0.21)
			except:
				return
		
	async def send_event_message(self, user, event):
		if user == self.bot.user:
			pass
		guild_data_path = tt.guild_data_path.format(str(user.guild.id))
		if not os.path.exists(guild_data_path):
			return
		guild_data = self.load_db(guild_data_path)
		if (('channels' not in guild_data) or ('msgchannel' not in guild_data['channels'])) or (('messages' not in guild_data) or (event not in guild_data['messages'])):
			return
		if (event == 'join') and (user.guild.me.guild_permissions.manage_roles):
			roles_to_assign = []
			if ('roles' not in guild_data) or ('defaultrole' not in guild_data['roles']):
				await user.add_roles(user.guild.get_role(guild_data['roles']['default']))
			if ('general' in guild_data) and ('stickyroles' in guild_data['general']) and (guild_data['general']['stickyroles'] == True):
				guild_stickyroles_path = tt.guild_stickyroles_path.format(str(user.guild.id))
				if os.path.exists(guild_stickyroles_path):
					guild_stickyroles = self.load_db(guild_stickyroles_path)
					if str(user.id) in guild_stickyroles:
						for role_id in guild_stickyroles[str(user.id)]:
							role = user.guild.get_role(role_id)
							if role in user.roles:
								continue
							roles_to_assign.append(role)
						await user.add_roles(roles_to_assign)
		channel = self.bot.get_channel(guild_data['channels']['msgchannel'])
		message = guild_data['messages'][event]
		replacements = {
			'[user]': f"{user.name}#{user.discriminator}",
			'[@user]': user.mention,
			'[user-name]': user.name,
			'[user#]': str(user.discriminator),
			'[user-id]': str(user.id),
			'[server]': user.guild.name
		}
		for x in replacements:
			message = message.replace(x, replacements[x])
		await channel.send(message)
	
	# 		========================
	
	@commands.Cog.listener()
	async def on_message(self, message):		
		for s_reaction in s_reactions:
			if s_reaction in message.content.lower():
				for reaction in s_reactions[s_reaction]: 
					await message.add_reaction(reaction)
		if (self.toggleable_reactions_list['naemt'] == True) and (message.author.id == 338292198866944002) and (message.channel.id == 697587669051637760):
			await message.add_reaction(tt.e['neutral'])

	@commands.Cog.listener()
	async def on_raw_message_delete(self, payload):
		guild_starboard_path = tt.guild_starboard_path.format(str(payload.guild_id))
		if not os.path.exists(guild_starboard_path):
			return
		starboard_data = self.load_db(guild_starboard_path)
		if (payload.message_id in starboard_data) or (payload.message_id in starboard_data.values()):
			del starboard_data[payload.message_id]
			self.dump_db(guild_starboard_path, starboard_data)

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if (payload.member.bot):
			return
		channel = self.bot.get_channel(payload.channel_id)
		message = await channel.fetch_message(payload.message_id)
		if (datetime.datetime.now()-message.created_at).days >= 7:
			return
		if (payload.emoji.is_custom_emoji()) and (payload.emoji.id == 747278013091282945) and (payload.member.id in tt.admins):
			await self.blackdude_reactions(message, channel, payload.member, payload.emoji)
			return
		guild_data_path = tt.guild_data_path.format(str(message.guild.id))
		reaction = get(message.reactions, emoji=payload.emoji.name)
		if payload.emoji.is_unicode_emoji() and os.path.exists(guild_data_path) and payload.emoji.name == "⭐" and reaction.count >= 5:
			print('b')
			guild_data = self.load_db(guild_data_path)
			print('aslk;jasdgjklsadfgkjldfgskj')
			if ('channels' not in guild_data) or ('starboard' not in guild_data['channels']):
				return
			await self.starboard(guild_data, message, channel, payload.member)
			return

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
		channel = self.bot.get_channel(payload.channel_id)
		message = await channel.fetch_message(payload.message_id)
		if (datetime.datetime.now()-message.created_at).days > 7:
			return
		guild_starboard_path = tt.guild_starboard_path.format(str(message.guild.id))
		guild_data_path = tt.guild_data_path.format(str(message.guild.id))
		if (not os.path.exists(guild_starboard_path)) or (not os.path.exists(guild_starboard_path)):
			return
		guild_data = self.load_db(guild_data_path)
		if ('channels' not in guild_data) or ('starboard' not in guild_data['channels']):
			return
		starboard_data = self.load_db(guild_starboard_path)
		if payload.message_id in starboard_data:
			starboard_channel = self.bot.get_channel(guild_data['channels']['starboard'])
			await self.starboard_update(message, starboard_channel)
			return
			
	#@commands.Cog.listener()
	#async def on_guild_channel_delete(self, channel):
	#	guild_data_path = tt.guild_data_path.format(str(channel.guild_id))
	#	if not os.path.exists(guild_data_path):
	#		return
	#	guild_data = self.load_db(guild_data_path)
	#	if 'channels' not in guild_data:
	#		return
	#	for channel_type in guild_data['channels']:
	#		if guild_data['channels'][channel_type] == channel.id:
	#			del guild_data['channels'][channel_type]
	#			self.dump_db(guild_data_path, guild_data)
	#			return
	
	@commands.Cog.listener()
	async def on_member_join(self, user):
		await self.send_event_message(user, 'join')

	@commands.Cog.listener()
	async def on_member_remove(self, user):
		await self.send_event_message(user, 'leave')		

	@commands.Cog.listener()
	async def on_member_ban(self, guild, user):
		await self.send_event_message(user, 'ban')

	# 		========================

	@commands.command()
	@checks.is_admin()
	async def togglereaction(self, ctx, name=None):
		if (name == None) or (name not in t_reactions):
			await ctx.send(str(self.toggleable_reactions_list))
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