import discord, time, datetime, re, urllib
from discord.ext import commands
from a import checks
from a.funcs import f
import a.constants as tt

class utilities(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.mn_in_progress = []

# 		========================

	@commands.command()
	async def help(self, ctx):
		await ctx.send(tt.help_list)

	@commands.command()
	async def invite(self, ctx):
		invite = 'https://discordapp.com/oauth2/authorize?client_id=439166087498825728&scope=bot&permissions='
		await ctx.send(embed=discord.Embed(title=f"invite trashbot", description=f"[invite with admin permissions]({invite+'8'})\n[invite with necessary permissions only]({invite+'1544416321'})", color=tt.color.pink))

	@commands.command()
	async def error(self, ctx):
		await ctx.send(1/0)

	@commands.command()
	async def about(self, ctx):
		await ctx.trigger_typing()
		e_about = discord.Embed(title=f"trashbot", description=f"a simple discord.py bot by @elisttm; more info can be found on {tt.infopage}", color=tt.color.pink)
		e_about.add_field(name="stats", value=f"`{len(list(self.bot.guilds))}` servers, `{len(self.bot.users)}` users", inline=True)
		e_about.add_field(name=f"uptime", value=str(f.timediff(f._t(False), tt.start_time, a=2)), inline=True)
		e_about.add_field(name=f"api version", value=discord.__version__, inline=True)
		e_about.set_thumbnail(url=self.bot.user.avatar_url)
		await ctx.send(embed=e_about)

	@commands.command()
	async def ping(self, ctx):
		ptime = time.time()
		message = await ctx.send("⌛ ⠀pinging...")
		ping = round((time.time() - ptime) * 1000)
		await message.edit(content=f'🏓 ⠀pong! `{ping}ms`')

	@commands.command()
	@commands.guild_only()
	async def user(self, ctx, user: discord.User=None):
		await ctx.trigger_typing()
		user = ctx.author if not user else user; extra_info = ''
		if user in ctx.guild.members:
			user = ctx.guild.get_member(user.id)
			extra_info += f"**joined**: __{user.joined_at.strftime(tt.ti.swag)}__ ({f.timediff(datetime.datetime.now(), user.joined_at, 2)})\n**top role**: {user.top_role} {'(owner)' if ctx.guild.owner == user else ''}{'(admin)' if user.guild_permissions.administrator and ctx.guild.owner != user else ''}\n\n"
		if user.id == tt.admins[0]: 
			extra_info += '\n`trashbot owner`'
		if user.id in tt.admins: 
			extra_info += '\n`trashbot admin`'
		if user.id in tt.blacklist_list: 
			extra_info += '\n`trashbot blacklisted`'
		e_user = discord.Embed(title=f"{user} {'('+{user.nick}+')' if user.nick != None and user in ctx.guild.members else ''} {'[BOT]' if user.bot else ''}", description=f"`{user.id}`\n**created**: __{user.created_at.strftime(tt.ti.swag)}__ ({f.timediff(datetime.datetime.now(), user.created_at, 2)})\n{extra_info}", color=user.color)
		e_user.set_thumbnail(url=user.avatar_url)
		await ctx.send(embed=e_user)

	@commands.command()
	@commands.guild_only()
	async def avatar(self, ctx, user: discord.User=None):
		await ctx.trigger_typing()
		user = ctx.author if not user else user
		await ctx.send(user.avatar_url)

	@commands.command()
	@commands.guild_only()
	async def server(self, ctx):
		await ctx.trigger_typing()
		guild = ctx.guild
		extra_stats = ''
		if len(guild.emojis) > 0: 
			extra_stats += f"**emojis**: {len(guild.emojis)}\n"
		if guild.premium_subscription_count > 0: 
			extra_stats += f"**boosts**: {guild.premium_subscription_count} {'('+len(guild.premium_subscribers)+' boosters)' if len(guild.premium_subscribers) != guild.premium_subscription_count else ''} (level {guild.premium_tier})\n"
		channels = (f'{len(guild.text_channels)} text' if len(guild.text_channels) > 0 else '')+(', ' if len(guild.text_channels) > 0 and len(guild.voice_channels) > 0 else '')+(f'{len(guild.voice_channels)} voice' if len(guild.voice_channels) > 0 else '')
		e_server = discord.Embed(title=f"{guild.name}", description=f"`{guild.id}`\n**owner**: {guild.owner}\n**created**: __{guild.created_at.strftime(tt.ti.swag)}__ ({f.timediff(datetime.datetime.now(), guild.created_at, 3)})\n**members**: {len(guild.members)}\n**channels**: {channels}\n{extra_stats}", color=(f.avgcolor(await guild.icon_url.read())))
		e_server.set_thumbnail(url=guild.icon_url)
		await ctx.send(embed=e_server)

	@commands.command(aliases=['e','emoji'])
	async def emote(self, ctx, pemoji):
		await ctx.trigger_typing()
		# https://twemoji.maxcdn.com/2/test/preview.html
		match = re.match(r'<(a?):([a-zA-Z0-9\_]+):([0-9]+)>$', pemoji)
		_emoji_ = 'nope'
		if match:
			_emoji_ = f"https://cdn.discordapp.com/emojis/{int(match.group(3))}.{'gif' if bool(match.group(1)) else 'png'}?v=1"
		else:
			if len(pemoji) > 1:
				url = '-'.join([f'{ord(e):X}' for e in pemoji])
			else: 
				url = f'{ord(pemoji):X}'
			_emoji_ = f"https://twemoji.maxcdn.com/v/latest/72x72/{url.lower()}.png"
			try: 
				urllib.request.urlopen(_emoji_).getcode()
			except:
				raise(commands.UserInputError)
				return
		await ctx.send(_emoji_)

	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 300, commands.BucketType.user)
	async def report(self, ctx, *, report:str):
		await ctx.trigger_typing()
		if len(report) > 500:
			ctx.command.reset_cooldown()
			await ctx.send(tt.w+"your report is too long! (max 500 characters)")
			return
		report = f"report from {ctx.author} in '{ctx.guild.name}'\n\"{report}\""
		f.log(report, '[REPORT]')
		await self.bot.get_user(tt.admins[0]).send(report)
		await ctx.send(tt.y+"your report has been submitted!")

	@commands.command()
	@commands.guild_only()
	@checks.is_guild_admin()
	@commands.bot_has_permissions(manage_nicknames=True)
	async def massnick(self, ctx, *, param:str):
		await ctx.trigger_typing()
		try:
			mn_users = mn_changed = 0; nickname = ''; mn_action = ['change','changing','changed']
			if len(param) > 32:
				await ctx.send(tt.w+"too many characters! (nicknames have a max of 32)")
				return
			if param == 'cancel':
				if ctx.guild.id not in self.mn_in_progress:
					await ctx.send(tt.x+"there is no massnick in progress!")
					return
				else:
					self.mn_in_progress.remove(ctx.guild.id)
					return
			elif ctx.guild.id in self.mn_in_progress:
				await ctx.send(tt.w+"there is already a massnick in progress!")
			else:
				self.mn_in_progress.append(ctx.guild.id) 
			storage = f.data(tt.storage, ctx.guild.id, 'nicknames', {})
			if 'nicknames' not in storage:
				f.data_update(tt.storage, ctx.guild.id, 'nicknames', {})
			nicknames_list = storage['nicknames']
			if param == 'revert':
				if 'lastnick' in nicknames_list and nicknames_list['lastnick'] == 'revert':
					await ctx.send(tt.x+"unable to revert nicknames! (last massnick was a revert)")
					return
				elif 'users' not in nicknames_list or len(nicknames_list['users']) == 0:
					await ctx.send(tt.x+"unable to revert nicknames! (nickname storage is empty)")
					return
				mn_action = ['revert','reverting','reverted']
			elif param == 'reset':
				nickname = None
				mn_action = ['reset','resetting','reset']
			else:
				nickname = param
			if param != 'cancel':
				f.data_update(tt.storage, ctx.guild.id, 'nicknames.lastnick', param)
			for member in ctx.guild.members: 
				if member.bot: continue
				mn_users += 1
			await ctx.send(tt.h+f"attempting to {mn_action[0]} `{mn_users}` nicknames, please wait...")
			f.log(f"{mn_action[1]} {mn_users} nicknames in {ctx.guild.name}", '[MASSNICK]')
			for member in ctx.guild.members:
				await ctx.trigger_typing()
				if ctx.guild.id not in self.mn_in_progress:
					await ctx.send(tt.y+"massnick cancelled!")
					return
				if member.bot or member.top_role >= ctx.guild.get_member(self.bot.user.id).top_role or member.nick == nickname:
					continue
				if param == 'revert':
					if str(member.id) not in nicknames_list['users']:
						nickname = None
					elif member.nick != nicknames_list['lastnick']:
						continue
					else:
						nickname = nicknames_list['users'][str(member.id)]
				try:
					oldnick = member.nick
					await member.edit(nick=nickname)
					if param != 'revert':
						f.data_update(tt.storage, ctx.guild.id, 'nicknames.users.'+str(member.id), oldnick)
					mn_changed += 1
				except:
					continue
			self.mn_in_progress.remove(ctx.guild.id)
			await ctx.send(tt.y+f"`{mn_changed}/{mn_users}` nicknames successfully {mn_action[2]}!")
			f.log(f"finished {mn_action[1]} {mn_changed}/{mn_users} nicknames in {ctx.guild.name}", '[MASSNICK]')
		except: 
			if ctx.guild.id in self.mn_in_progress:
				self.mn_in_progress.remove(ctx.guild.id)

	@commands.command(aliases=['purge'])
	@commands.guild_only()
	@commands.has_permissions(manage_messages=True)
	@commands.bot_has_permissions(manage_messages=True)
	async def clear(self, ctx, clear:int):
		await ctx.trigger_typing()
		if (clear == 0) or (clear > 100): 
			await ctx.send(tt.w+"invalid number of messages! (must be between 1 - 100)")
			return
		await ctx.message.delete()
		await ctx.channel.purge(limit=(clear))
		await ctx.send(tt.y+f"cleared `{clear}` messages!", delete_after=2)

# 		========================

def setup(bot):
	bot.add_cog(utilities(bot))