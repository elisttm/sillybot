import discord, re, datetime
from discord.utils import get
from discord.ext import commands, tasks
from a.funcs import f
import a.constants as tt

s_reactions = {
	'y/n': [tt.e.thumbsup, tt.e.thumbsdown],
	'u/d': [tt.e.upvote, tt.e.downvote],
}

class events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.stats = {}
		if not tt.testing:
			self.update_stats.start()

	def cog_unload(self):
		self.update_stats.cancel()

	@tasks.loop(seconds=10.0)
	async def update_stats(self):
		await self.bot.wait_until_ready()
		if len(self.stats) > 1:
			f.data_update(tt.misc, 'stats', ['commands.'+x for x in self.stats.keys()], [self.stats[x] for x in self.stats], 'inc')
			self.stats = {}

	async def starboard_content(self, message, star_count):
		e_sb = discord.Embed(description=f"{message.content}\n\n[jump to message]({message.jump_url})", color=tt.color.yellow)
		e_sb.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)
		e_sb.set_footer(text=f"{message.created_at.strftime(tt.ti.swag)} UDT | {message.id}")
		if len(message.attachments) != 0: 
			attachments_ = ''
			for attachment in message.attachments:
				attachments_ += f'[{attachment.filename}]({attachment.url})\n'
			e_sb.description = f"{message.content}\n\n{attachments_}[jump to message]({message.jump_url})"
			if any(filetype in message.attachments[0].url for filetype in ['.png','.jpg','.jpeg','.gif','.webp']):
				e_sb.set_image(url=message.attachments[0].url)		
		else:
			img = re.search(r'http(.*?)(.png|.jpg|.jpeg|.gif|.webp)', message.content)
			if img != None:
				e_sb.set_image(url="http"+img.group(1)+img.group(2))					
		return [f"{tt.e.star3 if star_count >= 10 else tt.e.star2 if star_count > 5 else tt.e.star} **{star_count}** {message.channel.mention}", e_sb]
		
	async def send_event_message(self, config, user, event):
		if 'msgchannel' in config and event in config:
			replacements = {
				'[user]': f"{user.name}#{user.discriminator}",
				'[@user]': user.mention,
				'[username]': user.name,
				'[server]': user.guild.name,
			}
			message = config[event]
			for x in replacements: 
				message = message.replace(x, replacements[x])
			await self.bot.get_channel(config['msgchannel']).send(message)
		
	@commands.Cog.listener()
	async def on_message(self, message):
		for s_reaction in s_reactions:
			if s_reaction in message.content.lower():
				for reaction in s_reactions[s_reaction]:
					await message.add_reaction(reaction)

	@commands.Cog.listener()
	async def on_command(self, ctx):
		command = ctx.command.qualified_name
		if command not in self.stats:
			self.stats[command] = 1
		else:
			self.stats[command] += 1

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if payload.member.bot:
			return
		channel = self.bot.get_channel(payload.channel_id)
		message = await channel.fetch_message(payload.message_id)
		config = f.data(tt.config, message.guild.id, ['starboard','starboardcount'], {})
		if (datetime.datetime.now()-message.created_at).days < 7 and 'starboard' in config and payload.emoji.name == '⭐':
			reaction = get(message.reactions, emoji=payload.emoji.name)
			starboardcount = config['starboardcount'] if 'starboardcount' in config else 5
			if reaction.count >= starboardcount:
				starboard_channel = self.bot.get_channel(config['starboard'])
				starboard_content = await self.starboard_content(message, reaction.count)
				starboard_data = f.data(tt.storage, message.guild.id, 'starboard', {'starboard':{}})['starboard']
				if str(message.id) in starboard_data:
					try:
						starboard_message = await starboard_channel.fetch_message(starboard_data[str(message.id)])
						if starboard_content[0] != starboard_message.content and starboard_content[1] != starboard_message.embeds[0]:
							await starboard_message.edit(content=starboard_content[0], embed=starboard_content[1])
					except:
						f.data_update(tt.storage, message.guild.id, 'starboard.'+str(message.id), 0, 'unset')
				else:
					starboard_message = await starboard_channel.send(content=starboard_content[0], embed=starboard_content[1])
					f.data_update(tt.storage, message.guild.id, 'starboard.'+str(message.id), starboard_message.id)

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
		channel = self.bot.get_channel(payload.channel_id)
		message = await channel.fetch_message(payload.message_id)
		if (datetime.datetime.now()-message.created_at).days > 7:
			return
		if payload.emoji.name == '⭐':
			config = f.data(tt.config, message.guild.id)
			storage = f.data(tt.storage, message.guild.id)
			reaction = get(message.reactions, emoji=payload.emoji.name)
			if reaction is None or config is None or 'starboard' not in storage or 'starboard' not in config:
				return
			if str(payload.message_id) in storage['starboard']:
				starboard_channel = self.bot.get_channel(config['starboard'])
				starboard_content = await self.starboard_content(message, reaction.count)
				try:
					starboard_message = await starboard_channel.fetch_message(storage['starboard'][str(message.id)])
					if starboard_content[0] != starboard_message.content and starboard_content[1] != starboard_message.embeds[0]:
						await starboard_message.edit(content=starboard_content[0], embed=starboard_content[1])
				except:
					f.data_update(tt.storage, message.guild.id, 'starboard.'+str(message.id), 0, 'unset')
	
	@commands.Cog.listener()
	async def on_member_join(self, user):
		if user == self.bot.user:
			f.data_update(tt.misc, 'misc', 'guilds', [user.guild.id], 'append')
			return
		config = f.data(tt.config, user.guild.id, ['joinmsg','autorole','stickyroles'], {})
		await self.send_event_message(config, user, 'joinmsg')
		if user.guild.me.guild_permissions.manage_roles:
			if 'autorole' in config:
				autorole = user.guild.get_role(config['autorole'])
				if autorole < user.guild.me.top_role:
					await user.add_roles(autorole, "autorole")
			if 'stickyroles' in config and config['stickyroles'] == True:
				storage = f.data(tt.storage, user.guild.id, 'stickyroles', {})
				if 'stickyroles' in storage and str(user.id) in storage['stickyroles']:
					addroles = []
					for role in storage['stickyroles'][str(user.id)]:
						role = user.guild.get_role(role)
						if role >= user.guild.me.top_role:
							continue
						addroles.append(role)
					f.data_update(tt.storage, user.guild.id, 'stickyroles.'+str(user.id), 0, 'unset')
					await user.add_roles(*addroles, "stickyroles")

	@commands.Cog.listener()
	async def on_member_remove(self, user):
		if user == self.bot.user:
			f.data_update(tt.misc, 'misc', 'guilds', [user.guild.id], 'remove')
			return
		config = f.data(tt.config, user.guild.id, ['leavemsg','stickyroles'], {})
		if 'leavemsg' in config:
			await self.send_event_message(config, user, 'leavemsg')
		if 'stickyroles' in config and config['stickyroles'] == True:
			f.data_update(tt.storage, user.guild.id, 'stickyroles.'+str(user.id), [role.id for role in user.roles if not role.managed])

def setup(bot):
	bot.add_cog(events(bot))
