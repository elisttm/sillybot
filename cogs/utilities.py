import discord, time, datetime, re, urllib
from discord.ext import commands, tasks
from a import checks
from a.funcs import f
import a.constants as tt

class utilities(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.mn_in_progress = []
		self.mn_storage = {}

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
		try:
			emoji = await commands.PartialEmojiConverter().convert(ctx, pemoji)
			print(emoji)
			emoji_url = emoji.url
		except:
			url = '-'.join([f'{ord(e):X}' for e in pemoji]) if len(pemoji) > 1 else f'{ord(pemoji):X}'
			emoji_url = f"https://twemoji.maxcdn.com/v/latest/72x72/{url.lower()}.png"
			try: 
				urllib.request.urlopen(emoji_url).getcode()
			except:
				raise(commands.UserInputError)
				return
		await ctx.send(emoji_url)

	@commands.command(aliases=['purge'])
	@commands.guild_only()
	@commands.has_permissions(manage_messages=True)
	@commands.bot_has_permissions(manage_messages=True)
	async def clear(self, ctx, clear:int):
		await ctx.trigger_typing()
		if clear == 0 or clear > 100: 
			await ctx.send(tt.w+"invalid number of messages! (must be between 1-100)")
			return
		await ctx.message.delete()
		await ctx.channel.purge(limit=clear)
		await ctx.send(tt.y+f"purged `{clear}` messages!", delete_after=3)

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
			if len(param) > 32:
				await ctx.send(tt.w+"maximum of 32 characters for nicknames!")
				return
			print(1)
			if ctx.guild.id in self.mn_in_progress:
				if param == 'cancel':
					self.mn_in_progress.remove(ctx.guild.id)
					return
				await ctx.send(tt.w+"there is already a massnick in progress!")
				return
			elif param == 'cancel':
				await ctx.send(tt.x+"there is no massnick in progress!")
				return
			self.mn_in_progress.append(ctx.guild.id)
			print(2) 
			nicknames_list = f.data(tt.storage, ctx.guild.id, 'nicknames', {'nicknames':{}})['nicknames']
			print(nicknames_list)
			if param == 'revert':
				if 'users' not in nicknames_list or len(nicknames_list['users']) == 0:
					await ctx.send(tt.x+"there is no nickname history stored!")
					return
				nickname = 'revert'
			elif param == 'reset':
				nickname = None
			else:
				nickname = param
				param = 'change'
			print(nickname)
			mn_users = [member for member in ctx.guild.members if not member.bot and member.top_role < ctx.guild.me.top_role and member.nick != nickname]
			await ctx.send(tt.h+f"attempting to {param} {len(mn_users)} of {ctx.guild.member_count} nicknames, please wait...")
			f.log(f"modifying {len(mn_users)} nicknames in {ctx.guild.name}", '[MASSNICK]')
			mn_changed = 0
			self.mn_storage[ctx.guild.id] = {}
			async with ctx.channel.typing():
				for member in mn_users:
					if ctx.guild.id not in self.mn_in_progress:
						await ctx.send(tt.y+"massnick cancelled!")
						break
					if param == 'revert':
						if member.nick != nicknames_list['lastnick'] or str(member.id) not in nicknames_list['users']:
							continue
						nickname = nicknames_list['users'][str(member.id)]
					else:
						self.mn_storage[ctx.guild.id][str(member.id)] = member.nick
					try:
						await member.edit(nick=nickname)
						mn_changed += 1
					except:
						continue
			f.data_update(tt.storage, ctx.guild.id, 'nicknames', {'users':self.mn_storage[ctx.guild.id],'lastnick':nickname})
			self.mn_in_progress.remove(ctx.guild.id)
			await ctx.send(tt.y+f"`{mn_changed}/{len(mn_users)}` nicknames successfully {param if not param == 'change' else 'changed'}!")
			f.log(f"modified {mn_changed}/{len(mn_users)} nicknames in {ctx.guild.name}", '[MASSNICK]')
		except: 
			if ctx.guild.id in self.mn_in_progress:
				self.mn_in_progress.remove(ctx.guild.id)

# 		========================

def setup(bot):
	bot.add_cog(utilities(bot))