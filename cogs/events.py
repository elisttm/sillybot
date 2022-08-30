from discord.ext import commands, tasks
from a.funcs import f
import a.constants as tt

autoreacts = {
	'y/n': [tt.e.thumbsup, tt.e.thumbsdown],
	'u/d': [tt.e.upvote, tt.e.downvote],
}

class events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.stats = {}
		self.send_log.start()
		if not tt.testing:
			self.update_stats.start()

	def cog_unload(self):
		self.update_stats.cancel()
		self.send_log.cancel()

	@tasks.loop(seconds=10.0)
	async def update_stats(self):
		await self.bot.wait_until_ready()
		if len(self.stats) >= 1:
			tt.misc.update_one({'_id':'stats'}, {"$inc":{'commands.'+x:self.stats[x] for x in self.stats.keys()}})
			self.stats.clear()

	@tasks.loop(seconds=10.0)
	async def send_log(self):
		await self.bot.wait_until_ready()
		log = 'trashbot' if not tt.testing else 'tbtest'
		logtxt = ('\n'.join(tt.misc.find_one({'_id':'logs'},{log:1}).get(log, [])))[:1990]
		if logtxt:
			await self.bot.get_channel(tt.channels.log).send(f"```{logtxt}```")
			tt.misc.update_one({'_id':'logs'}, {"$set":{log:[]}})
		
	@commands.Cog.listener()
	async def on_message(self, message):
		for r in autoreacts:
			if r in message.content.lower():
				for reaction in autoreacts[r]:
					await message.add_reaction(reaction)

	@commands.Cog.listener()
	async def on_command(self, ctx):
		cmd = ctx.command.qualified_name
		self.stats[cmd] = self.stats.get(cmd,0)+1
	
	async def send_event_message(self, config, user, event):
		if 'msgchannel' in config and event in config:
			rep = {
				'[user]': str(user), 
				'[@user]': user.mention, 
				'[username]': user.name, 
				'[server]': user.guild.name
			}
			msg = config[event]
			[msg := msg.replace(f'{x}', f'{y}') for x, y in rep.items()]
			await self.bot.get_channel(config['msgchannel']).send(msg)

	@commands.Cog.listener()
	async def on_member_join(self, user):
		if user == self.bot.user:
			f._list(tt.misc, 'misc', 'guilds', [user.guild.id], 'add')
			return
		config = tt.config.find_one({'_id':user.guild.id},{'msgchannel':1,'joinmsg':1,'autorole':1,'stickyroles':1})
		if not config:
			return
		await self.send_event_message(config, user, 'joinmsg')
		if user.guild.me.guild_permissions.manage_roles:
			if 'autorole' in config:
				autorole = user.guild.get_role(config['autorole'])
				if autorole < user.guild.me.top_role:
					await user.add_roles(autorole)
			if config.get('stickyroles') == True:
				storage = tt.storage.find_one({'_id':user.guild.id},{'stickyroles':1})
				if 'stickyroles' in storage and str(user.id) in storage['stickyroles']:
					addroles = []
					for roleid in storage['stickyroles'][str(user.id)]:
						role = user.guild.get_role(roleid)
						if role < user.guild.me.top_role and not role.managed:
							addroles.append(role)
					await user.add_roles(*addroles)

	@commands.Cog.listener()
	async def on_member_remove(self, user):
		if user == self.bot.user:
			f._list(tt.misc, 'misc', 'guilds', [user.guild.id], 'remove')
			return
		config = tt.config.find_one({'_id':user.guild.id},{'msgchannel':1,'leavemsg':1,'stickyroles':1})
		if not config:
			return
		await self.send_event_message(config, user, 'leavemsg')
		if config.get('stickyroles') == True:
			storageroles = [int(role.id) for role in user.roles if not role.managed and role.name != '@everyone']
			tt.storage.update_one({'_id':user.guild.id}, {"$set":{f'stickyroles.{user.id}':storageroles}})

async def setup(bot):
	await bot.add_cog(events(bot))
