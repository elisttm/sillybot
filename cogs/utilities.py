import discord 
import pickle
import time
from discord.ext import commands
import data.constants as tt

# 		========================

class utilities(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def send_log(self, log:str):
		log_msg = f"[{tt._t()}] {log}"
		print(log_msg)
		await self.bot.get_channel(tt.logs).send(f"```{log_msg}```")

# 		========================

	@commands.command()
	async def about(self, ctx):
		await ctx.trigger_typing()
		try:
			guild_num = len(list(self.bot.guilds))
			user_num = 0
			for user in self.bot.users:
				if user.bot is True: continue 
				else: user_num += 1
			e_about = discord.Embed(title=f"trashbot | v{tt.v}", url=tt.website, description=f"{tt.desc}\n\n**bot name**: {self.bot.user}\n**bot ID**: `{self.bot.user.id}`", color=tt.clr['pink'])
			e_about.add_field(name="stats", value=f"servers: `{guild_num}`, users: `{user_num}`", inline=True)
			e_about.add_field(name=f"client uptime", value=f"{tt.uptime()}", inline=True)
			e_about.set_author(name=f"about trashbot", icon_url=tt.ico['info'])
			e_about.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url_as(format='png'))
			e_about.set_thumbnail(url=self.bot.user.avatar_url)
			await ctx.send(embed=e_about)
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	@commands.command(pass_context=True)
	async def ping(self, ctx):
		try:
			ptime = time.time()
			message = await ctx.send("⌛ ⠀pinging...")
			ping = round((time.time() - ptime) * 1000)
			await message.edit(content=f"🏓 ⠀pong! ({ping}ms)")
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	async def invite(self, ctx):
		await ctx.trigger_typing()
		await ctx.send(f"use this link to invite trashbot to your server\n{tt.invite}")

	@commands.command()
	@commands.guild_only()
	async def user(self, ctx, user: discord.Member = None):
		await ctx.trigger_typing()
		user = ctx.author if not user else user
		try:
			try:
				nametag = ''
				if user.nick != None: nametag = nametag + f'({user.nick}) '
				if user.bot == True: nametag = nametag + f'[BOT] '
			except: 
				nametag = ''
			e_user = discord.Embed(title=f"{user} {nametag}", description=f"**ID**: `{user.id}`\n**guild join**: __{user.joined_at.strftime(tt.time0)}__\n**created**: __{user.created_at.strftime(tt.time0)}__", color=user.top_role.colour)
			e_user.set_author(name=f"{user.name} :: user profile", icon_url=tt.ico['info'])
			e_user.set_thumbnail(url=user.avatar_url)
			e_user.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url_as(format='png'))
			await ctx.send(embed=e_user)
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@commands.guild_only()
	async def avatar(self, ctx, user: discord.Member = None):
		await ctx.trigger_typing()
		user = ctx.author if not user else user
		try:
			e_avatar = discord.Embed(color=ctx.message.author.top_role.colour)
			e_avatar.set_author(name=f"{user}'s avatar", icon_url=tt.ico['info'])
			e_avatar.set_image(url=user.avatar_url)
			e_avatar.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url_as(format='png'))
			await ctx.send(embed=e_avatar)
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@commands.guild_only()
	async def server(self, ctx):
		await ctx.trigger_typing()
		try:
			e_server = discord.Embed(title=f"{ctx.message.guild.name}", description=f"**ID**: `{ctx.message.guild.id}`\n**owner**: {ctx.message.guild.owner}\n**region**: {ctx.guild.region}\n**members**: {len(ctx.message.guild.members)}\n**created**: __{ctx.message.guild.created_at.strftime(tt.time0)}__", color=tt.clr['pink'])
			e_server.set_author(name=f"{ctx.message.guild.name} :: server info", icon_url=tt.ico['info'])
			e_server.set_thumbnail(url=ctx.message.guild.icon_url)
			e_server.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url_as(format='png'))
			await ctx.send(embed=e_server)
		except Exception as e: 
			await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def github(self, ctx):
		await ctx.trigger_typing()
		await ctx.send(tt.github)

	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 300, commands.BucketType.user)
	async def report(self, ctx, *, report:str):
		await ctx.trigger_typing()
		try:
			if len(report) > 1000:
				await ctx.send("⚠️ ⠀your report is too long!")
			else:
				report = tt.sanitize(text = report)
				report = report.replace('`', '\`')
				report_info = f"feedback recieved from '{ctx.author}' in '{ctx.guild.name}'"
				await self.send_log(log = report_info)
				await self.bot.get_user(tt.owner_id).send(f"{report_info}\n> ```{report}```")
				await ctx.send("✅ ⠀your report has been submitted!")
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@commands.guild_only()
	@commands.has_permissions(administrator = True)
	async def massnick(self, ctx, *, nickname):
		try:
			mn_users, mn_changed, mn_failed = 0
			for member in ctx.guild.members: 
				mn_users += 1
			await ctx.send(f"⌛ ⠀attempting to change `{mn_users}` nicknames, please wait...")
			await self.send_log(log = f"MASSNICK: [{ctx.guild.name}] attempting to change '{mn_users}' nicknames to '{nickname}'...")
			for member in ctx.guild.members:
				await ctx.trigger_typing()
				try: 
					await member.edit(nick=nickname)
					mn_changed += 1
				except: 
					mn_failed += 1
			await ctx.send(f"✅ ⠀`{mn_changed}` nicknames successfully changed, `{mn_failed}` failed.")
			await self.send_log(log = f"MASSNICK: [{ctx.guild.name}] '{mn_changed}/{mn_users}' nicknames changed to '{nickname}'")
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command(aliases=['purge'])
	@commands.guild_only()
	@commands.has_permissions(manage_messages = True)
	async def clear(self, ctx, clear:int):
		try:
			clear_invalidamount = "⚠️ ⠀invalid message clear amount! ({})"
			if clear == 0: 
				await ctx.send(clear_invalidamount.format("amount must be at least 1"))
			elif clear > 100: 
				await ctx.send(clear_invalidamount.format("amount cannot exceed 100"))
			else:
				await ctx.message.delete()
				await ctx.channel.purge(limit=(clear))
				await ctx.send(f"✅ ⠀cleared `{clear}` messages", delete_after=2)
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@commands.guild_only()
	@commands.has_permissions(administrator = True)
	async def prefix(self, ctx, action=None, prefix=None):
		await ctx.trigger_typing()
		try:
			custom_prefixes = pickle.load(open(tt.prefixes_pkl, "rb"))
			if action == None:
				if ctx.message.guild.id in custom_prefixes:
					await ctx.send(f"ℹ️ ⠀this guild's custom prefix is '{custom_prefixes[ctx.message.guild.id]}'")
				else:
					await ctx.send("⚠️ ⠀no custom prefix for this guild. do `t!prefix set [prefix]` to create one!")
			else:
				action = action.lower()
				if action == 'set':
					if prefix != None:
						if ctx.message.guild.id in custom_prefixes:
							del custom_prefixes[ctx.message.guild.id]
						custom_prefixes[ctx.message.guild.id] = prefix
						await ctx.send(f"✅ ⠀custom prefix for this guild set to '{prefix}'")
					else:
						await ctx.send("⚠️ ⠀please provide a valid custom prefix!")
				elif action == 'remove':
					if ctx.message.guild.id in custom_prefixes:
						del custom_prefixes[ctx.message.guild.id]
						await ctx.send(f"✅ ⠀removed custom prefix for this guild")
					else:
						await ctx.send(f"❌ ⠀this guild does not have a custom prefix set!")
				pickle.dump(custom_prefixes, open(tt.prefixes_pkl, "wb"))
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

# 		========================

def setup(bot):
	bot.add_cog(utilities(bot))