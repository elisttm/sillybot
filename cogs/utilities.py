import discord, time, datetime
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
		await ctx.send(tt.invite)

	@commands.command()
	async def error(self, ctx):
		await ctx.send(1/0)

	@commands.command()
	async def about(self, ctx):
		await ctx.trigger_typing()
		desc = '\n\n`note: trashbot is currently running under maintenance, so bugs, delays, and downtime are to be expected!`' if tt.testing else ''
		e_about = discord.Embed(title=f"trashbot", description=f"a simple discord.py bot by @elisttm; more info can be found on {tt.infosite}"+desc, color=tt.clr['pink'])
		e_about.add_field(name="stats", value=f"i am in `{len(list(self.bot.guilds))}` servers with a total of `{len(self.bot.users)}` users", inline=True)
		e_about.add_field(name=f"client uptime", value=str(datetime.timedelta(seconds=int(round(time.time()-tt.start_time)))), inline=True)
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
		user = ctx.author if not user else user
		perm = trashbot_tag = toprole = joined = ''
		if user.id == tt.admins[0]: trashbot_tag += '\n`trashbot owner`'
		if user.id in tt.admins: trashbot_tag += '\n`trashbot admin`'
		if user.id in tt.blacklist_list: trashbot_tag += '\n`trashbot blacklisted`'
		if user in ctx.guild.members:
			user = ctx.guild.get_member(user.id)
			if user.guild_permissions.administrator: perm = '(guild admin)'
			if ctx.guild.owner == user: perm = '(guild owner)'
			joined = f"\n**joined**: __{user.joined_at.strftime(tt.ti[0])}__ ({'%d days'%(datetime.datetime.now()-user.joined_at).days})"
			toprole = f"\n**top role**: {user.top_role} {perm}"
		e_user = discord.Embed(title=f"{user} {'('+{user.nick}+')' if user.nick is not None and user in ctx.guild.members else ''} {'[BOT]' if user.bot else ''}", description=f"`{user.id}`{toprole}{joined}\n**created**: __{user.created_at.strftime(tt.ti[0])}__ ({'%d days'%(datetime.datetime.now()-user.created_at).days})\n{trashbot_tag}", color=user.color)
		#e_user.set_author(name=f"user info", icon_url=tt.ico['info'])
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
		guild = ctx.guild; guild_boosts = ''
		if guild.premium_subscription_count > 0:
			guild_boosts = f"\n**boosts**: {guild.premium_subscription_count}{ '('+len(guild.premium_subscribers)+') boosters' if len(guild.premium_subscribers) != guild.premium_subscription_count else ''} (level {guild.premium_tier})"
		e_server = discord.Embed(title=f"{guild.name}", description=f"`{guild.id}`\n**owner**: {guild.owner}\n**members**: {len(guild.members)}{guild_boosts}\n**emojis**: {len(guild.emojis)}\n**roles**: {len(guild.roles)}\n**channels**: {len(guild.text_channels)} text, {len(guild.voice_channels)} voice\n**created**: __{guild.created_at.strftime(tt.ti[0])}__ ({'%d days' % (datetime.datetime.now() - guild.created_at).days})", color=tt.clr['pink'])
		e_server.set_thumbnail(url=ctx.guild.icon_url)
		await ctx.send(embed=e_server)

	@commands.command(aliases=['e','emoji'])
	async def emote(self, ctx, _emoji:discord.PartialEmoji):
		await ctx.trigger_typing()
		ext = "gif" if _emoji.animated else "png"
		url = f"https://cdn.discordapp.com/emojis/{_emoji.id}.{ext}?v=1"
		await ctx.send(url)

	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 300, commands.BucketType.user)
	async def report(self, ctx, *, report:str):
		await ctx.trigger_typing()
		if len(report) > 1000:
			await ctx.send(tt.w+"your report is too long! (1000 max)")
			ctx.command.reset_cooldown()
			return
		report = (f.sanitize(text = report)).replace('`', '\`')
		report_header = f"feedback recieved from '{ctx.author}' in '{ctx.guild.name}'"
		f.log(f"{report_header}\n{report}", '[REPORT]')
		await self.bot.get_user(tt.admins[0]).send(f"{report_header}\n> ```{report}```")
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
			if f.data(tt.storage, ctx.guild.id) is None or 'nicknames' not in f.data(tt.storage, ctx.guild.id):
				f.data_update(tt.storage, ctx.guild.id, 'nicknames', {})
			nicknames_list = f.data(tt.storage, ctx.guild.id)['nicknames']
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