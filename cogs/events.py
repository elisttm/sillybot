import discord, asyncio, re, datetime
from discord.utils import get
from discord.ext import commands#, tasks
from a.funcs import f
import a.constants as tt

s_reactions = {
	'y/n': [tt.e.thumbsup, tt.e.thumbsdown],
	'u/d': [tt.e.uparrow, tt.e.downarrow],
}

class events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# 		========================

	def starboard_header(self, message, star_count):
		if star_count >= 10: 
			star = tt.e.star3
		elif star_count > 5: 
			star = tt.e.star2
		elif star_count <= 5: 
			star = tt.e.star
		return f"{star} **{star_count}** {message.channel.mention}" 
			
	def starboard_embed(self, message):
		e_sb = discord.Embed(description=message.content, color=tt.color.yellow)
		e_sb.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)
		e_sb.set_footer(text=f"{message.id} | {message.created_at.strftime(tt.ti.swag)} UDT")
		e_sb.add_field(name="source", value=f"[jump to message]({message.jump_url})")
		if len(message.attachments) > 0:
			for filetype in ['.png','.jpg','.webp','.gif']:
				if message.attachments[0].url.endswith(filetype):
					e_sb.set_image(url=message.attachments[0].url)
			attachments_ = ''
			for attachment in message.attachments:
				attachments_ += f'[{attachment.filename}]({attachment.url})\n'
			e_sb.add_field(name="attachments", value=attachments_)
		else:
			message_attachements = []
			for filetype in ['.png','.jpg','.webp','.gif']:
				for image in re.findall(r'http(.*?){}'.format(filetype), message.content):
					message_attachements.append("http"+image+filetype)
				if len(message_attachements) != 0:
					e_sb.set_image(url=message_attachements[0])
					break
		return e_sb
		
	async def starboard_update(self, starboard_data, message, starboard_channel, star_count):
		embed = self.starboard_embed(message)
		header = self.starboard_header(message, star_count)
		try:
			starboard_message = await starboard_channel.fetch_message(starboard_data[str(message.id)])
		except:
			return
		if header == starboard_message.content and embed == starboard_message.embeds[0]:
			return
		await starboard_message.edit(content=header, embed=embed)
		return
		
	async def send_event_message(self, config, user, event):
		if 'msgchannel' not in config or event not in config:
			return
		message = config[event]
		replacements = {
			'[user]': f"{user.name}#{user.discriminator}",
			'[@user]': user.mention,
			'[username]': user.name,
			'[userid]': str(user.id),
			'[server]': user.guild.name
		}
		for x in replacements: 
			message = message.replace(x, replacements[x])
		await self.bot.get_channel(config['msgchannel']).send(message)
	
	# 		========================
	
	@commands.Cog.listener()
	async def on_message(self, message):		
		for s_reaction in s_reactions:
			if s_reaction in message.content.lower():
				for reaction in s_reactions[s_reaction]: 
					await message.add_reaction(reaction)

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if payload.member.bot:
			return
		channel = self.bot.get_channel(payload.channel_id)
		message = await channel.fetch_message(payload.message_id)
		config = f.data(tt.config, message.guild.id)
		if not config:
			return
		if 'starboard' in config and payload.emoji.is_unicode_emoji() and payload.emoji.name == '⭐':
			if (datetime.datetime.now()-message.created_at).days >= 7:
				return
			reaction = get(message.reactions, emoji=payload.emoji.name)
			reaction_count = reaction.count
			starboardcount = 5
			if 'starboardcount' in config:
				starboardcount = int(config['starboardcount'])
			if reaction.count >= starboardcount:
				starboard_channel = self.bot.get_channel(config['starboard'])
				storage = f.data(tt.storage, message.guild.id, 'starboard', {'starboard':{}})
				starboard_data = storage['starboard']
				if str(message.id) in starboard_data:
					await self.starboard_update(starboard_data, message, starboard_channel, reaction_count)
					return
				starboard_message = await starboard_channel.send(content=self.starboard_header(message, reaction_count), embed=self.starboard_embed(message))
				f.data_update(tt.storage, message.guild.id, 'starboard.'+str(message.id), starboard_message.id)

		# rolemenus
		
			# insert code for rolemenu reactions here

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
		channel = self.bot.get_channel(payload.channel_id)
		message = await channel.fetch_message(payload.message_id)
		if (datetime.datetime.now()-message.created_at).days > 7:
			return
		if payload.emoji.is_unicode_emoji() and payload.emoji.name == '⭐':
			config = f.data(tt.config, message.guild.id)
			if config == None:
				return
			reaction = get(message.reactions, emoji=payload.emoji.name)
			if reaction is None:
				return
			if 'starboard' not in f.data(tt.storage, message.guild.id):
				f.data_update(tt.storage, message.guild.id, 'starboard', {})
				starboard_data = f.data(tt.storage, message.guild.id)['starboard']
			if starboard_data is None or 'starboard' not in config:
				return
			if str(payload.message_id) in starboard_data:
				starboard_channel = self.bot.get_channel(config['starboard'])
				await self.starboard_update(starboard_data, message, starboard_channel, reaction.count)
				return
	
	@commands.Cog.listener()
	async def on_member_join(self, user):
		if user == self.bot.user:
			f.data_update(tt.yeah, 'misc', 'guilds', [user.guild.id], a='append')
			return
		config = f.data(tt.config, user.guild.id)
		if config == None:
			return
		await self.send_event_message(config, user, 'joinmsg')
		if user.guild.me.guild_permissions.manage_roles:
			if 'autorole' in config:
				await user.add_roles(user.guild.get_role(config['autorole']))
			if 'stickyroles' in config and config['stickyroles'] == True:
				if f.data(tt.storage, user.guild.id) is None or 'stickyroles' not in f.data(tt.storage, user.guild.id):
					f.data_update(tt.storage, user.guild.id, 'stickyroles', {})
					return
				stickyroles = f.data(tt.storage, user.guild.id)['stickyroles']
				if str(user.id) not in stickyroles:
					return
				addroles = []
				bot_toprole = user.guild.get_member(self.bot.user.id).top_role.position
				for role in stickyroles[str(user.id)]:
					if user.guild.get_role(role).position >= bot_toprole:
						continue
					addroles.append(user.guild.get_role(role))
				f.data_update(tt.tags, user.guild.id, 'stickyroles.'+str(user.id), None, 'unset')
				try:
					await self.bot.add_roles(user, *addroles)
				except:
					pass

	@commands.Cog.listener()
	async def on_member_remove(self, user):
		if user == self.bot.user:
			f.data_update(tt.yeah, 'misc', 'guilds', [user.guild.id], a='remove')
			return
		config = f.data(tt.config, user.guild.id)
		if config == None:
			return
		if 'stickyroles' in config and config['stickyroles'] == True:
			if f.data(tt.storage, user.guild.id) is None or 'stickyroles' not in f.data(tt.storage, user.guild.id):
				f.data_update(tt.storage, user.guild.id, 'stickyroles', {})
			stickyroles = []
			for role in user.roles:
				stickyroles.append(role.id)
			f.data_update(tt.storage, user.guild.id, 'stickyroles.'+str(user.id), stickyroles)
		await self.send_event_message(config, user, 'leavemsg')

	# 		========================

def setup(bot):
	bot.add_cog(events(bot))