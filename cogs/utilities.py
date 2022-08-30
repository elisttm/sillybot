import discord, time, datetime, dateutil.relativedelta
from discord.ext import commands
from a import checks
from a.funcs import f
import a.constants as tt

class utilities(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.mn_in_progress = []
		self.mn_storage = {}

	@commands.command()
	async def help(self, ctx):
		await ctx.send(tt.site+'commands')

	@commands.command()
	async def invite(self, ctx):
		invite = f'https://discordapp.com/oauth2/authorize?client_id={ctx.bot.user.id}&scope=bot&permissions='
		await ctx.send(embed=discord.Embed(title=f"invite sillybot", description=f"[invite with admin permissions]({invite+'8'})\n[invite with minimal permissions]({invite+'1544416321'})", color=tt.dcolor))

	@commands.command()
	async def error(self, ctx):
		await ctx.send(1/0)

	@commands.command()
	async def about(self, ctx):
		await ctx.channel.typing()
		appinfo = await self.bot.application_info()
		diff = dateutil.relativedelta.relativedelta(datetime.datetime.utcnow(), tt.start_time) 
		e_about = discord.Embed(title=appinfo.name, description=appinfo.description, color=tt.dcolor)
		e_about.add_field(name="stats", value=f"`{len(list(self.bot.guilds))}` servers, `{len(self.bot.users)}` users", inline=False)
		e_about.add_field(name=f"uptime", value=(', ').join([f"{x}" for x in [f'{diff.years}yr',f'{diff.months}mo',f'{diff.days}d',f'{diff.hours}hr',f'{diff.minutes}m',f'{diff.seconds}s'] if x[0] != '0']), inline=False)
		e_about.add_field(name=f"wrapper version", value=discord.__version__, inline=False)
		e_about.set_thumbnail(url=self.bot.user.avatar.url)
		await ctx.send(embed=e_about)

	@commands.command()
	async def ping(self, ctx):
		etime = time.time()
		msg = await ctx.send(f"{tt.h}pinging...")
		etime = round((time.time()-etime)*1000)
		await msg.edit(content=f'{tt.e.pingpong}{tt.s}pong! `{etime}ms / {round((self.bot.latency)*1000)}ms`')

	@commands.command()
	@commands.guild_only()
	async def user(self, ctx, user:discord.User=None):
		await ctx.channel.typing()
		user = ctx.author if not user else user
		extra_info = ''
		if user in ctx.guild.members:
			user = ctx.guild.get_member(user.id)
			extra_info += f"**joined**: __<t:{int(user.joined_at.timestamp())}:D>__ (<t:{int(user.joined_at.timestamp())}:R>)\n**top role**: {user.top_role} {'(owner)' if ctx.guild.owner == user else ''}{'(admin)' if user.guild_permissions.administrator and ctx.guild.owner != user else ''}\n"
		if user.id == tt.admins[0]: 
			extra_info += '\n`bot owner`'
		if user.id in tt.admins: 
			extra_info += '\n`bot admin`'
		if user.id in tt.blacklist: 
			extra_info += '\n`blacklisted`'
		e_user = discord.Embed(title=f"{user}"+(f" ({user.nick})" if user in ctx.guild.members and user.nick != None else '')+(' [BOT]' if user.bot else ''), description=f"`{user.id}`\n**created**: __<t:{int(user.created_at.timestamp())}:D>__ (<t:{int(user.created_at.timestamp())}:R>)\n{extra_info}", color=user.color)
		e_user.set_thumbnail(url=user.display_avatar.url)
		await ctx.send(embed=e_user)

	@commands.command()
	async def avatar(self, ctx, user:discord.User=None):
		user = ctx.author if not user else user
		await ctx.send(user.display_avatar.replace(static_format='png', size=1024).url)

	@commands.command()
	@commands.guild_only()
	async def server(self, ctx):
		await ctx.channel.typing()
		guild = ctx.guild
		extra_stats = ''
		if len(guild.emojis) > 0: 
			extra_stats += f"**emojis**: {len(guild.emojis)}\n"
		if guild.premium_subscription_count > 0: 
			extra_stats += f"**boosts**: {guild.premium_subscription_count} {'('+str(len(guild.premium_subscribers))+' boosters)' if len(guild.premium_subscribers) != guild.premium_subscription_count else ''} (level {guild.premium_tier})\n"
		channels = (f'{len(guild.text_channels)} text' if len(guild.text_channels) > 0 else '')+(', ' if len(guild.text_channels) > 0 and len(guild.voice_channels) > 0 else '')+(f'{len(guild.voice_channels)} voice' if len(guild.voice_channels) > 0 else '')
		e_server = discord.Embed(title=f"{guild.name}", description=f"`{guild.id}`\n**owner**: {guild.owner}\n**created**: __<t:{int(guild.created_at.timestamp())}:D>__ (<t:{int(guild.created_at.timestamp())}:R>)\n**members**: {len(guild.members)}\n**channels**: {channels}\n{extra_stats}", color=(f.avgcolor(await guild.icon.read())))
		e_server.set_thumbnail(url=guild.icon.url)
		await ctx.send(embed=e_server)

	@commands.command(aliases=['purge'])
	@commands.guild_only()
	@commands.has_permissions(manage_messages=True)
	@commands.bot_has_permissions(manage_messages=True)
	async def clear(self, ctx, limit:int, user:discord.User=None):
		await ctx.channel.typing()
		if limit == 0 or limit > 100: 
			await ctx.send(tt.w+"invalid amount! (must be between 1-100)")
			return
		await ctx.message.delete()
		self.c = 0
		def ucheck(msg):
			if user == None or msg.author == user:
				self.c += 1
				return True
		await ctx.channel.purge(limit=limit, check=ucheck)
		await ctx.send(tt.y+f"purged `{self.c}` messages{' by '+str(user) if user != None else ''}!", delete_after=3)

	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 300, commands.BucketType.user)
	async def report(self, ctx, *, report:str):
		await ctx.channel.typing()
		if len(report) > 1000:
			ctx.command.reset_cooldown()
			await ctx.send(tt.w+"your report is too long! (max 1000 characters)")
			return
		report = f"report from {ctx.author} in '{ctx.guild.name}'\n\"{report}\" {' '.join([a.url for a in ctx.message.attachments])}"
		f.log(report, '[REPORT]')
		await self.bot.get_user(tt.admins[0]).send(report)
		await ctx.send(tt.y+"your report has been submitted!")

	@commands.command()
	@commands.guild_only()
	@checks.is_guild_admin()
	@commands.bot_has_permissions(manage_nicknames=True)
	async def massnick(self, ctx, *, param:str):
		await ctx.channel.typing()
		stupid = {'change':['changing','changed'],'clear':['clearing','cleared'],'undo':['reverting','reverted']}
		try:
			if len(param) > 32:
				await ctx.send(tt.w+"maximum of 32 characters for nicknames!")
				return
			if ctx.guild.id in self.mn_in_progress:
				if param == 'cancel':
					self.mn_in_progress.remove(ctx.guild.id)
					return
				await ctx.send(tt.w+"there is already a massnick in progress!")
				return
			elif param == 'cancel':
				await ctx.send(tt.x+"no massnick in progress!")
				return
			nicknames_list = f.data(tt.storage, ctx.guild.id, 'nicknames', {'nicknames':{}})['nicknames']
			if param == 'undo':
				if 'users' not in nicknames_list or len(nicknames_list['users']) == 0:
					await ctx.send(tt.x+"no nickname history found for this server!")
					return
				nickname = param
			elif param == 'clear':
				nickname = None
			else:
				nickname = param
				param = 'change'
			mn_users = [member for member in ctx.guild.members if not member.bot and member.top_role < ctx.guild.me.top_role and member.nick != nickname]
			if len(mn_users) == 0:
				await ctx.send(tt.w+"role hierarchy is preventing me from nicknaming anyone!")
				return
			self.mn_in_progress.append(ctx.guild.id)
			await ctx.send(tt.h+f"attempting to {param} {len(mn_users)} of {ctx.guild.member_count} nicknames, please wait...")
			f.log(f"{stupid[param][0]} {len(mn_users)} nicknames in {ctx.guild.name}", '[MASSNICK]')
			mn_changed = 0
			self.mn_storage[ctx.guild.id] = {}
			async with ctx.channel.typing():
				for member in mn_users:
					if ctx.guild.id not in self.mn_in_progress:
						await ctx.send(tt.y+"massnick cancelled!")
						break
					if param != 'undo':
						self.mn_storage[ctx.guild.id].update({str(member.id):member.nick})
					elif member.nick == nicknames_list['lastnick'] and str(member.id) in nicknames_list['users']:
						nickname = nicknames_list['users'][str(member.id)]						
					try:
						await member.edit(nick=nickname)
						mn_changed += 1
					except:
						continue
			f._set(tt.storage, ctx.guild.id, {"$set":{"nicknames.users":self.mn_storage[ctx.guild.id],"nicknames.lastnick":nickname if param != 'undo' else 'undo'}})
			self.mn_in_progress.remove(ctx.guild.id)
			await ctx.send(tt.y+f"`{mn_changed}/{len(mn_users)}` nicknames successfully {stupid[param][1]}!")
			f.log(f"{stupid[param][1]} {mn_changed}/{len(mn_users)} nicknames in {ctx.guild.name}", '[MASSNICK]')
		except Exception as error: 
			if ctx.guild.id in self.mn_in_progress:
				self.mn_in_progress.remove(ctx.guild.id)
			raise(error)

async def setup(bot):
	await bot.add_cog(utilities(bot))
