import discord, urllib, urllib.request, time, datetime
from discord.ext import commands
from a import checks
from a.funcs import funcs
import a.constants as tt

class utilities(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.load_db = funcs.load_db
		self.dump_db = funcs.dump_db
		self.check_for_db = funcs.check_for_db
		self.send_log = funcs.send_log

		self.mn_cancelled = []
		self.mn_in_progress = []

# 		========================

	@commands.command()
	async def about(self, ctx):
		await ctx.trigger_typing()
		try:
			guild_num = len(list(self.bot.guilds))
			user_num = 0
			for user in self.bot.users:
				if user.bot: 
					continue 
				else: 
					user_num += 1
			e_about = discord.Embed(title=f"trashbot", url=tt.website, description=f"{tt.desc}\n", color=tt.clr['pink'])
			e_about.add_field(name="stats", value=f"servers: `{guild_num}`, users: `{user_num}`", inline=True)
			e_about.add_field(name=f"client uptime", value=f"{tt.uptime()}", inline=True)
			e_about.add_field(name=f"api version", value=discord.__version__, inline=True)
			#e_about.set_author(name=f"about trashbot", icon_url=tt.ico['info'])
			e_about.set_thumbnail(url=self.bot.user.avatar_url)
			await ctx.send(embed=e_about)
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	async def ping(self, ctx):
		await ctx.trigger_typing()
		try:
			ptime = time.time()
			message = await ctx.send("⌛ ⠀pinging...")
			ping = round((time.time() - ptime) * 1000)
			await message.edit(content=f'🏓 ⠀pong! `{ping}ms`')
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	async def invite(self, ctx):
		await ctx.trigger_typing()
		await ctx.send(tt.invite)

	@commands.command()
	async def help(self, ctx):
		await ctx.trigger_typing()
		await ctx.send(tt.help_list)

	@commands.command()
	@commands.guild_only()
	async def user(self, ctx, user: discord.User=None):
		await ctx.trigger_typing()
		user = ctx.author if not user else user
		blacklist_list = self.load_db(tt.blacklist_db)
		try:
			perm = trashbot_tag = toprole = joined = ''
			if user.id == tt.owner_id: trashbot_tag += '\n`trashbot owner`'
			if user.id in tt.admins: trashbot_tag += '\n`trashbot admin`'
			if user.id in blacklist_list: trashbot_tag += '\n`trashbot blacklisted`'
			if user in ctx.guild.members:
				user = ctx.guild.get_member(user.id)
				if user.guild_permissions.administrator: perm = '(guild admin)'
				if ctx.guild.owner == user: perm = '(guild owner)'
				joined = f"\n**joined**: __{user.joined_at.strftime(tt.time0)}__ ({'%d days' % (datetime.datetime.now() - user.joined_at).days})"
				toprole = f"\n**top role**: {user.top_role} {perm}"
			e_user = discord.Embed(
				title=f"{user} {'('+{user.nick}+')' if user.nick is not None and user in ctx.guild.members else ''} {'[BOT]' if user.bot else ''}", 
				description=f"`{user.id}`{toprole}{joined}\n**created**: __{user.created_at.strftime(tt.time0)}__ ({'%d days' % (datetime.datetime.now() - user.created_at).days})\n{trashbot_tag}", 
				color=user.color)
			#e_user.set_author(name=f"user info", icon_url=tt.ico['info'])
			e_user.set_thumbnail(url=user.avatar_url)
			#e_user.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url_as(format='png'))
			await ctx.send(embed=e_user)
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@commands.guild_only()
	async def avatar(self, ctx, user: discord.User=None):
		await ctx.trigger_typing()
		user = ctx.author if not user else user
		try:
			await ctx.send(user.avatar_url)
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@commands.guild_only()
	async def server(self, ctx):
		await ctx.trigger_typing()
		if ctx.invoked_subcommand is None:
			if ctx.subcommand_passed is not None:
				raise(commands.UserInputError)
				return 
			guild = ctx.guild; guild_boosts = ''
			if guild.premium_subscription_count > 0:
				guild_boosts = f"\n**boosts**: {guild.premium_subscription_count}{ '('+len(guild.premium_subscribers)+') boosters' if len(guild.premium_subscribers) != guild.premium_subscription_count else ''} (level {guild.premium_tier})"
			try:
				e_server = discord.Embed(title=f"{guild.name}", description=f"`{guild.id}`\n**owner**: {guild.owner}\n**members**: {len(guild.members)}{guild_boosts}\n**emojis**: {len(guild.emojis)}\n**roles**: {len(guild.roles)}\n**channels**: {len(guild.text_channels)} text, {len(guild.voice_channels)} voice\n**created**: __{guild.created_at.strftime(tt.time0)}__ ({'%d days' % (datetime.datetime.now() - guild.created_at).days})", color=tt.clr['pink'])
				#e_server.set_author(name="server info", icon_url=tt.ico['info'])
				e_server.set_thumbnail(url=ctx.guild.icon_url)
				await ctx.send(embed=e_server)
			except Exception as e: 
				await ctx.send(tt.msg_e.format(e))

	@commands.command(aliases=['e','emoji'])
	async def emote(self, ctx, _emoji:discord.PartialEmoji):
		await ctx.trigger_typing()
		try:
			ext = "gif" if _emoji.animated else "png"
			url = f"https://cdn.discordapp.com/emojis/{_emoji.id}.{ext}?v=1"
			await ctx.send(url)
		except Exception as e: 
			await ctx.send(tt.msg_e.format(e))

	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 300, commands.BucketType.user)
	async def report(self, ctx, *, report:str):
		await ctx.trigger_typing()
		try:
			if len(report) > 1000:
				await ctx.send(tt.w+"your report is too long! (1000 max)")
				ctx.command.reset_cooldown()
				return
			report = (tt.sanitize(text = report)).replace('`', '\`')
			report_header = f"feedback recieved from '{ctx.author}' in '{ctx.guild.name}'"
			await self.send_log(self, f"{report_header}\n{report}", '[REPORT]')
			await self.bot.get_user(tt.owner_id).send(f"{report_header}\n> ```{report}```")
			await ctx.send(tt.y+"your report has been submitted!")
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@commands.guild_only()
	@checks.is_guild_admin()
	@commands.bot_has_permissions(manage_nicknames=True)
	async def massnick(self, ctx, *, param:str):
		await ctx.trigger_typing()
		try:
			mn_users = mn_changed = 0; nickname = to_ = ''; mn_action = ['change','changing','changed']
			if len(param) > 32:
				await ctx.send(tt.w+"too many characters! (nicknames have a max of 32)")
				return
			if param == 'cancel':
				if ctx.guild.id not in self.mn_in_progress:
					await ctx.send(tt.x+"there is no massnick in progress!")
					return
				else:
					self.mn_cancelled.append(ctx.guild.id)
					self.mn_in_progress.remove(ctx.guild.id)
					return
			elif ctx.guild.id in self.mn_in_progress:
				await ctx.send(tt.w+"there is already a massnick in progress!")
			else:
				self.mn_in_progress.append(ctx.guild.id)
			guild_nicknames_path = tt.guild_nicknames_path.format(str(ctx.guild.id))
			self.check_for_db(guild_nicknames_path)
			nicknames_list = self.load_db(guild_nicknames_path)
			if 'users' not in nicknames_list:
				nicknames_list['users'] = {}
			if param == 'revert':
				if 'no_revert' in nicknames_list and nicknames_list['no_revert'] == True:
					await ctx.send(tt.x+"unable to revert nicknames! (last massnick was a revert)")
					return
				elif 'users' not in nicknames_list or len(nicknames_list['users']) == 0:
					await ctx.send(tt.x+"unable to revert nicknames! (nickname storage is empty)")
					return
				else:
					nicknames_list['no_revert'] = True
				mn_action = ['revert','reverting','reverted']
			elif param == 'reset':
				nickname = None
				mn_action = ['reset','resetting','reset']
				nicknames_list['no_revert'] = False
			else:
				nickname = param
				nicknames_list = {'users':{},'lastnick':nickname,'no_revert':False}
				to_ = f"to '{nickname}' "
			for member in ctx.guild.members: 
				if member.bot: continue
				mn_users += 1
			await ctx.send(tt.h+f"attempting to {mn_action[0]} `{mn_users}` nicknames, please wait...")
			await self.send_log(self, f"{mn_action[1]} '{mn_users}' nicknames {to_}in '{ctx.guild.name}'...", '[MASSNICK]')
			for member in ctx.guild.members:
				await ctx.trigger_typing()
				if ctx.guild.id in self.mn_cancelled:
					await ctx.send(tt.y+"massnick cancelled!")
					self.mn_cancelled.remove(ctx.guild.id)
					if ctx.guild.id in self.mn_in_progress:
						self.mn_in_progress.remove(ctx.guild.id)
					nicknames_list['lastnick'] = 'cancelled'
					self.dump_db(guild_nicknames_path, nicknames_list)
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
						nicknames_list['users'][str(member.id)] = oldnick
					mn_changed += 1
				except:
					continue
			self.mn_in_progress.remove(ctx.guild.id)
			self.dump_db(guild_nicknames_path, nicknames_list)
			await ctx.send(tt.y+f"`{mn_changed}/{mn_users}` nicknames successfully {mn_action[2]}!")
			await self.send_log(self, f"'{mn_changed}/{mn_users}' nicknames {mn_action[2]} {to_}in '{ctx.guild.name}'!", '[MASSNICK]')
		except Exception as error: 
			if ctx.guild.id in self.mn_in_progress:
				self.mn_in_progress.remove(ctx.guild.id)
			await ctx.send(tt.msg_e.format(error))

	@commands.command(aliases=['purge'])
	@commands.guild_only()
	@commands.has_permissions(manage_messages=True)
	@commands.bot_has_permissions(manage_messages=True)
	async def clear(self, ctx, clear:int):
		await ctx.trigger_typing()
		try:
			if (clear == 0) or (clear > 100): 
				await ctx.send(tt.w+"invalid number of messages! (must be between 1 - 100)")
				return
			await ctx.message.delete()
			await ctx.channel.purge(limit=(clear))
			await ctx.send(tt.y+f"cleared `{clear}` messages!", delete_after=2)
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

# 		========================

def setup(bot):
	bot.add_cog(utilities(bot))