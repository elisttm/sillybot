import discord 
import pickle
import time, datetime
from discord.ext import commands
import data.constants as tt

# 		========================

class utilities(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

# 		========================

	@commands.command()
	async def about(self, ctx):
		await ctx.trigger_typing()
		try:
			guild_num = len(list(self.bot.guilds)); user_num = 0
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

	@commands.command()
	async def ping(self, ctx):
		await ctx.trigger_typing()
		ping = 0; ping = round(self.bot.latency * 1000)
		await ctx.send(f"{ping}ms")

	@commands.command()
	async def invite(self, ctx):
		await ctx.trigger_typing()
		await ctx.send(tt.invite)


	@commands.command()
	async def user(self, ctx, user: discord.Member = None):
		await ctx.trigger_typing()
		user = ctx.author if not user else user
		try:
			try:
				nametag = ''
				if user.nick != None: nametag = nametag + f'({user.nick}) '
				if user.bot == True: nametag = nametag + f'[BOT] '
			except: nametag = ''
			e_user = discord.Embed(title=f"{user} {nametag}", 
				description=f"**ID**: `{user.id}`\n**guild join**: __{user.joined_at.strftime(tt.time0)}__\n**created**: __{user.created_at.strftime(tt.time0)}__", color=user.top_role.colour)
			e_user.set_author(name=f"{user.name} :: user profile", icon_url=tt.ico['info'])
			e_user.set_thumbnail(url=user.avatar_url)
			e_user.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url_as(format='png'))
			await ctx.send(embed=e_user)
		except Exception as error: await ctx.send(tt.msg_e.format(error))

	@commands.command()
	async def avatar(self, ctx, user: discord.Member = None):
		await ctx.trigger_typing()
		user = ctx.author if not user else user
		try:
			e_avatar = discord.Embed(color=ctx.message.author.top_role.colour)
			e_avatar.set_author(name=f"{user}'s avatar", icon_url=tt.ico['info'])
			e_avatar.set_image(url=user.avatar_url)
			e_avatar.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url_as(format='png'))
			await ctx.send(embed=e_avatar)
		except Exception as error: await ctx.send(tt.msg_e.format(error))

	@commands.command()
	async def server(self, ctx):
		await ctx.trigger_typing()
		try:
			e_server = discord.Embed(title=" ", 
				description=f"**ID**: `{ctx.message.guild.id}`\n**owner**: {ctx.message.guild.owner}\n**region**: {ctx.guild.region}\n**members**: {len(ctx.message.guild.members)}\n**created**: __{ctx.message.guild.created_at.strftime(tt.time0)}__", color=tt.clr['pink'])
			e_server.set_author(name=f"{ctx.message.guild.name} :: server info", icon_url=tt.ico['info'])
			e_server.set_thumbnail(url=ctx.message.guild.icon_url)
			e_server.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url_as(format='png'))
			await ctx.send(embed=e_server)
		except Exception as e: await ctx.send(tt.msg_e.format(e))

	@commands.command()
	@commands.cooldown(1, 300)
	async def report(self, ctx, *, report=None):
		await ctx.trigger_typing()
		try:
			if report == None:
				report_info = '> to send a feedback or bug report, use "t!report send [message]"'
				await ctx.send(report_info)
			elif len(report) > 1900:
				await ctx.send("⚠️ ⠀your report is too long!")
			elif report != None:
				tt.l = f"[{tt._t()}] feedback recieved from '{ctx.author}' in '{ctx.guild.name}'"
				await self.bot.get_channel(tt.logs).send(f"{tt.l}\n\"{report}\""); print(tt.l); await self.bot.get_user(tt.owner_id).send(f"{tt.l}\n> \"{report}\"")
				await ctx.send("✅ ⠀your report has been submitted!")
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))


	@commands.command()
	@commands.has_permissions(administrator = True)
	async def prefix(self, ctx, action=None, prefix=None):
		await ctx.trigger_typing()
		try:
			custom_prefixes = pickle.load(open(tt.prefixes_pkl, "rb"))
			if action == None:
				if ctx.message.guild.id in custom_prefixes:
					await ctx.send(f"ℹ️ ⠀this guild's custom prefix is '{custom_prefixes[ctx.message.guild.id]}'")
				else:
					await ctx.send("⚠️ ⠀no custom prefix for this guild. do t!prefix set to create one!")
			else:
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
	