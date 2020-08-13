import discord
import sys, os
import psutil
import pickle
from discord.ext import commands
import data.constants as tt

# 		========================

class admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

# 		========================

	@commands.command()
	async def admins(self, ctx): 
		try:
			await ctx.trigger_typing()
			adm_list, adm_num = '', 0
			for user in tt.admins:
				user = self.bot.get_user(user)
				adm_list = f"{adm_list}{user} ({user.id})\n"; adm_num += 1
			e_adm = discord.Embed(color=tt.clr['pink'])
			e_adm.add_field(name=f"admins `[{adm_num}]`", value=adm_list)
			e_adm.set_author(name="admin list", icon_url=tt.ico['info'])
			await ctx.send(embed=e_adm)
		except Exception as e: await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def presence(self, ctx, *, presence=None):
		try:
			await ctx.trigger_typing()
			if ctx.author.id in tt.admins:
				if presence is None or "reset" == presence:
					presence = discord.Game(tt.presence)
					await self.bot.change_presence(status=discord.Status.online, activity=presence)
					tt.l = f"[{tt._t()}] ADMIN: presence reset by '{ctx.author}'"
					await ctx.send('✅ ⠀presence reset to default.')	
				else:
					presence = presence.replace("(v)", f"{tt.v}"); presence = discord.Game(presence)
					await self.bot.change_presence(status=discord.Status.online, activity=presence)
					tt.l = f"[{tt._t()}] ADMIN: presence set to '{presence}' by '{ctx.author}'"
					await ctx.send(f'✅ ⠀presence set to `{presence}`.')
				await self.bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)
			else: await ctx.send(embed=tt.permdeny)
		except Exception as e: await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def leave(self, ctx):
		try:
			if ctx.author.id == tt.owner_id:
				await ctx.message.add_reaction('✅')
				tt.l = f"[{tt._t()}] ADMIN: '{ctx.author}' used leave in '{ctx.guild.name}'"
				await self.bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)
				await ctx.guild.leave()
			else: await ctx.send(embed=tt.permdeny)
		except Exception as e: await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def shutdown(self, ctx):
		try:
			if ctx.author.id == tt.owner_id:
				tt.l = f"[{tt._t()}] ADMIN: shutdown by '{ctx.author}'"
				await ctx.message.add_reaction('✅')
				await self.bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)
				tt.mrestart = True
				await self.bot.close()
				await sys.exit(0)
			else: await ctx.send(embed=tt.permdeny)
		except Exception as e: await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def massnick(self, ctx, *, nickmass=None):
		try:
			if ctx.author.id in tt.admins:
				mn_users, mn_changed, mn_failed = 0
				for member in ctx.guild.members: mn_users += 1
				await ctx.send(f"⌛ ⠀attempting to change `{mn_users}` nicknames, please wait...")
				for member in ctx.guild.members:
					await ctx.trigger_typing()
					try: await member.edit(nick=nickmass); mn_changed += 1
					except: mn_failed += 1
				await ctx.send(f"✅ ⠀`{mn_changed}` nicknames successfully changed, `{mn_failed}` failed.")
				await self.bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)
			else: await ctx.send(embed=tt.permdeny)
		except Exception as e: await ctx.send(tt.msg_e.format(e))
	
	@commands.command()
	async def guilds(self, ctx):
		try:
			await ctx.trigger_typing()
			if ctx.author.id in tt.admins:
				guildlist = f''
				for guild in self.bot.guilds: guildlist = guildlist + f'	 -- {guild.name} ({guild.owner}) [{guild.id}]\n'
				tt.l = f"[{tt._t()}] ADMIN: '{ctx.author}' called for the list of guilds\n"; tt.l = tt.l + guildlist
				await self.bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)
				await ctx.send("✅ ⠀guild list sent to logs!")
			else: await ctx.send(embed=tt.permdeny)
		except Exception as e: await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def echo(self, ctx, echochannel: int, *, botsay=None):
		try:
			if ctx.author.id in tt.admins:
				if botsay is None:
					await ctx.send("⚠️ ⠀please specify what you want me to say!")
				else:
					tt.sanitize(botsay)
					tt.l = f"[{tt._t()}] '{ctx.author}' echoed from '{ctx.guild.name}' to channel ID '{echochannel}' message '{botsay}'"
					await self.bot.get_channel(echochannel).send(botsay)
					await ctx.message.add_reaction('✅')
					await self.bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)
					echochannel = 0
			else: await ctx.send(embed=tt.permdeny)
		except Exception as e: await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def restart(self, ctx):
		try:
			if ctx.author.id in tt.admins:
				tt.l = f"[{tt._t()}] ADMIN: restarted by '{ctx.author}'"
				await ctx.message.add_reaction('✅')
				await self.bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)
				await os.execv(sys.executable, ['python'] + sys.argv)
			else: await ctx.send(embed=tt.permdeny)
		except Exception as e: await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def blacklist(self, ctx, arg1=None, user: discord.Member = None):
		try:
			if ctx.author.id in tt.admins:
				blacklist = pickle.load(open(tt.blacklist_pkl, "rb"))
				if arg1 == None:
					if user == None:
						blacklist_list = ''
						for x in blacklist:
							user = self.bot.get_user(x)
							blacklist_list = blacklist_list + f"- {user} ({user.id})\n"
							await ctx.send(f"```list of blacklisted users ({len(blacklist)}):\n{blacklist_list}```")
				elif arg1 == 'add':
					if user == None:
						await ctx.send("⚠️ ⠀please provide a user ID or mention!")
					else:
						if user.id not in blacklist:
							blacklist.append(user.id)
							pickle.dump(blacklist, open(tt.blacklist_pkl, "wb"))
							await ctx.send("✅ ⠀user added to blacklist")
						else:
							await ctx.send("❌ ⠀user is already blacklisted!")
				elif arg1 == 'remove':
					if user == None:
						await ctx.send("⚠️ ⠀please provide a user ID or mention!")
					else:
						if user.id in blacklist:
							blacklist.remove(user.id)
							pickle.dump(blacklist, open(tt.blacklist_pkl, "wb"))
							await ctx.send("✅ ⠀user removed from blacklist")
						else:
							await ctx.send("❌ ⠀user is not blacklisted!")
				else:
					await ctx.send("invalid subcommand")
			else: await ctx.send(embed=tt.permdeny)
		except Exception as e: await ctx.send(tt.msg_e.format(e))

#pickle.dump(blacklist, open(tt.blacklist_pkl, "wb"))


# 		========================

def setup(bot):
	bot.add_cog(admin(bot))
	