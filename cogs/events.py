import discord, os, asyncio, re, datetime
from discord.utils import get
from discord.ext import commands#, tasks
from a import checks
from a.funcs import funcs
import a.configs as conf
import a.constants as tt

filetypes = ['.png','.jpg','.webp','.gif']
r_sb_img = r'http(.*?){}'
r_sb_tenor = r'https://tenor.com/view/(.*?)'

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

	# 		========================

	def starboard_header(self, message, star_count):
		if star_count >= 10: star = '💫'
		elif (star_count <= 10) and (star_count > 5): star = '🌟'
		elif star_count <= 5: star = '⭐'
		return f"{star} **{star_count}** {message.channel.mention}" 
			
	def starboard_embed(self, message):
		e_sb = discord.Embed(description=message.content, color=tt.clr['yellow'])
		e_sb.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)
		e_sb.set_footer(text=f"{message.id} ⠀| ⠀{message.created_at.strftime(tt.time0)} UDT")
		e_sb.add_field(name="\u200b", value=f"[jump to message]({message.jump_url})")
		if len(message.attachments) > 0:
			e_sb.set_image(url=message.attachments[0].url)
		else:
			message_attachements = []
			for filetype in filetypes:
				for image in re.findall(r_sb_img.format(filetype), message.content):
					message_attachements.append("http"+image+filetype)
			for tenor in re.findall(r_sb_tenor, message.content):
				message_attachements.append("https://tenor.com/view/"+tenor)
			if len(message_attachements) != 0:
				try:
					e_sb.set_image(url=message_attachements[0])
				except:
					pass
		return e_sb
		
	async def starboard_update(self, starboard_data, message, starboard_channel, star_count):
		embed = self.starboard_embed(message)
		header = self.starboard_header(message, star_count)
		try:
			starboard_message = await starboard_channel.fetch_message(starboard_data[str(message.id)])
		except:
			return
		if (header == starboard_message.content) and (embed == starboard_message.embeds[0]):
			return
		await starboard_message.edit(content=header, embed=embed)
		return
		
	async def send_event_message(self, guild_data, user, event):
		if 'msgchannel' not in guild_data or event not in guild_data:
			return
		channel = self.bot.get_channel(guild_data['msgchannel'])
		message = guild_data[event]
		replacements = {
			'[user]': f"{user.name}#{user.discriminator}",
			'[@user]': user.mention,
			'[user-name]': user.name,
			'[user-disc]': str(user.discriminator),
			'[user-id]': str(user.id),
			'[server]': user.guild.name
		}
		for x in replacements: message = message.replace(x, replacements[x])
		await channel.send(message)
	
	# 		========================
	
	@commands.Cog.listener()
	async def on_message(self, message):		
		for s_reaction in s_reactions:
			if s_reaction in message.content.lower():
				for reaction in s_reactions[s_reaction]: 
					await message.add_reaction(reaction)

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if (payload.member.bot):
			return
		channel = self.bot.get_channel(payload.channel_id)
		message = await channel.fetch_message(payload.message_id)
		if (datetime.datetime.now()-message.created_at).days >= 7:
			return
		guild_data_path = tt.guild_data_path.format(str(message.guild.id))

		# blackdude emoji spam lol
		if (payload.emoji.is_custom_emoji()) and (payload.emoji.id == 747278013091282945) and (payload.member.id in tt.admins):
			for emoji in self.bot.get_guild(747195327530139759).emojis:
				if emoji == payload.emoji:
					continue
				try:
					await message.add_reaction(emoji)
					await asyncio.sleep(0.21)
				except:
					return

		# starboard
		if payload.emoji.is_unicode_emoji() and os.path.exists(guild_data_path) and payload.emoji.name == '⭐':
			reaction = get(message.reactions, emoji=payload.emoji.name)
			reaction_count = reaction.count
			starboardcount = 5
			guild_data = self.load_db(guild_data_path)
			if 'starboardchannel' not in guild_data:
				return
			if 'starboardcount' in guild_data:
				starboardcount = int(guild_data['starboardcount'])
			if reaction.count >= starboardcount:
				starboard_channel = self.bot.get_channel(guild_data['starboardchannel'])
				guild_starboard_path = tt.guild_starboard_path.format(str(message.guild.id))
				self.check_for_db(guild_starboard_path)
				starboard_data = self.load_db(guild_starboard_path)
				if str(message.id) in starboard_data:
					await self.starboard_update(starboard_data, message, starboard_channel, reaction_count)
					return
				starboard_message = await starboard_channel.send(content=self.starboard_header(message, reaction_count), embed=self.starboard_embed(message))
				starboard_data[str(message.id)] = starboard_message.id
				self.dump_db(guild_starboard_path, starboard_data)

		# rolemenus
		
			# insert code for rolemenu reactions here

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
		channel = self.bot.get_channel(payload.channel_id)
		message = await channel.fetch_message(payload.message_id)
		if (datetime.datetime.now()-message.created_at).days > 7:
			return
		if payload.emoji.is_unicode_emoji() and payload.emoji.name == '⭐':
			reaction = get(message.reactions, emoji=payload.emoji.name)
			if reaction is None:
				reaction_count = 0
			else:
				reaction_count = reaction.count
			guild_starboard_path = tt.guild_starboard_path.format(str(message.guild.id))
			guild_data_path = tt.guild_data_path.format(str(message.guild.id))
			if (not os.path.exists(guild_starboard_path)) or (not os.path.exists(guild_starboard_path)):
				return
			guild_data = self.load_db(guild_data_path)
			if 'starboardchannel' not in guild_data:
				return
			starboard_data = self.load_db(guild_starboard_path)
			if str(payload.message_id) in starboard_data:
				starboard_channel = self.bot.get_channel(guild_data['starboardchannel'])
				await self.starboard_update(starboard_data, message, starboard_channel, reaction_count)
				return
	
	@commands.Cog.listener()
	async def on_member_join(self, user):
		if user == self.bot.user:
			return
		guild_data_path = tt.guild_data_path.format(str(user.guild.id))
		if not os.path.exists(guild_data_path):
			return
		guild_data = self.load_db(guild_data_path)
		await self.send_event_message(guild_data, user, 'joinmsg')
		if user.guild.me.guild_permissions.manage_roles:
			if 'defaultrole' in guild_data:
				await user.add_roles(user.guild.get_role(guild_data['defaultrole']))
			if 'stickyroles' in guild_data and guild_data['stickyroles'] == True:
				guild_stickyroles_path = tt.guild_stickyroles_path.format(str(user.guild.id))
				if not os.path.exists(guild_stickyroles_path):
					return
				guild_stickyroles = self.load_db(guild_stickyroles_path)
				if str(user.id) not in guild_stickyroles:
					return
				addroles = []
				bot_toprole = user.guild.get_member(self.bot.user.id).top_role.position
				for role_id in guild_stickyroles[str(user.id)]:
					if user.guild.get_role(role_id).position >= bot_toprole:
						continue
					addroles.append(user.guild.get_role(role_id))
				try:
					await self.bot.add_roles(user, *addroles)
				except:
					pass

	@commands.Cog.listener()
	async def on_member_remove(self, user):
		if user == self.bot.user:
			return
		guild_data_path = tt.guild_data_path.format(str(user.guild.id))
		if not os.path.exists(guild_data_path):
			return
		guild_data = self.load_db(guild_data_path)
		if 'stickyroles' in guild_data and guild_data['stickyroles'] == True:
			guild_stickyroles_path = tt.guild_stickyroles_path.format(str(user.guild.id))
			self.check_for_db(guild_stickyroles_path)
			guild_stickyroles = self.load_db(guild_stickyroles_path)
			guild_stickyroles[str(user.id)] = []
			for role in user.roles:
				guild_stickyroles[str(user.id)].append(role.id)
			self.dump_db(guild_stickyroles_path, guild_stickyroles)
		await self.send_event_message(guild_data, user, 'leavemsg')		

	# 		========================

def setup(bot):
	bot.add_cog(events(bot))