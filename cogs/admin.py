import discord
import sys, os
import psutil
from discord.ext import commands
import data.constants as tt

# 		========================

class admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

# 		========================

	@commands.command()
	async def admins(self, ctx): 
		await ctx.trigger_typing()
		adm_list, adm_num = '', 0
		for user in tt.admins:
			user = self.bot.get_user(user)
			adm_list = f"{adm_list}{user} ({user.id})\n"; adm_num += 1
		e_adm = discord.Embed(color=tt.clr['pink'])
		e_adm.add_field(name=f"admins `[{adm_num}]`", value=adm_list)
		e_adm.set_author(name="admin list", icon_url=tt.ico['info'])
		await ctx.send(embed=e_adm)

	@commands.command()
	async def presence(self, ctx, *, presence=None):
		await ctx.trigger_typing()
		if ctx.author.id in tt.admins:
			if presence is None or "reset" == presence:
				presence = discord.Game(tt.presence)
				await self.bot.change_presence(status=discord.Status.online, activity=presence)
				tt.l = f"[{tt._t()}] ADMIN: presence reset by '{ctx.author}'"
				await ctx.send('> ✅ ⠀presence reset to default.')	
			else:
				presence = presence.replace("(v)", f"{tt.v}"); presence = discord.Game(presence)
				await self.bot.change_presence(status=discord.Status.online, activity=presence)
				tt.l = f"[{tt._t()}] ADMIN: presence set to '{presence}' by '{ctx.author}'"
				await ctx.send(f'> ✅ ⠀presence set to `{presence}`.')
			await self.bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)
		else:
			await ctx.send(embed=tt.permdeny)

	@commands.command()
	async def nick(self, ctx, *, nick=None):
		await ctx.trigger_typing()
		if ctx.author.id in tt.admins:
			trashbot = ctx.guild.get_member(self.bot.user.id)
			if nick is None: await trashbot.edit(nick=None); await ctx.send('> ✅ ⠀nickname reset')
			elif len(nick) > 32: await ctx.send('> ⚠️ ⠀nickname is too long! (32 character max)')
			else: await trashbot.edit(nick=nick); await ctx.send(f'> ✅ ⠀nickname set to `{nick}`.')
		else:
			await ctx.send(embed=tt.permdeny)

	@commands.command()
	async def leave(self, ctx):
		if ctx.author.id == tt.owner_id:
			await ctx.message.add_reaction('✅')
			tt.l = f"[{tt._t()}] ADMIN: '{ctx.author}' used leave in '{ctx.guild.name}'"
			await self.bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)
			await ctx.guild.leave()
		else:
			await ctx.send(embed=tt.permdeny)

	@commands.command()
	async def shutdown(self, ctx):
		if ctx.author.id == tt.owner_id:
			tt.l = f"[{tt._t()}] ADMIN: shutdown by '{ctx.author}'"
			await ctx.message.add_reaction('✅')
			await self.bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)
			tt.mrestart = True
			await self.bot.close()
		else:
			await ctx.send(embed=tt.permdeny)

	@commands.command()
	async def restart(self, ctx):
		if ctx.author.id in tt.admins:
			p = psutil.Process(os.getpid())
			for handler in p.get_open_files() + p.connections():
				os.close(handler.fd)
			python = sys.executable
			os.execl(python, python, *sys.argv)
#			tt.l = f"[{tt._t()}] ADMIN: restarted by '{ctx.author}'"
#			await ctx.message.add_reaction('✅')
#			await self.bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)
#			await os.execv(sys.executable, sys.executable, * sys.argv)
		else:
			await ctx.send(embed=tt.permdeny)

	@commands.command()
	async def massnick(self, ctx, *, nickmass=None):
		if ctx.author.id in tt.admins:
			mn_users = 0; mn_changed = 0; mn_failed = 0
			for member in ctx.guild.members: mn_users = mn_users + 1
#			if len(nickmass) > 32: await ctx.send("> ⚠️ ⠀that cant fit in a nickname! (32 character max)")
#			elif nickmass == None or "reset":
#				tt.l = f"[{tt._t()}] ADMIN: '{ctx.author}' used massnick reset in '{ctx.guild.name}'\n"
#				await ctx.send(f"> ⌛ ⠀attempting to reset `{mn_users}` nicknames, please wait...")
#				for member in ctx.guild.members:
#					await ctx.trigger_typing()
#					try: await member.edit(nick=None); mn_changed = mn_changed + 1
#					except: mn_failed += 1
#				tt.l = f"{tt.l}[{tt._t()}] ADMIN: reset '{mn_changed}' nicknames, '{mn_failed}' failed"
#				await ctx.send(f"> ✅ ⠀`{mn_changed}` nicknames successfully reset, `{mn_failed}` failed.")
#			else:
			await ctx.send(f"> ⌛ ⠀attempting to change `{mn_users}` nicknames, please wait...")
			for member in ctx.guild.members:
				await ctx.trigger_typing()
				try: await member.edit(nick=nickmass); mn_changed = mn_changed + 1
				except: mn_failed += 1
			await ctx.send(f"> ✅ ⠀`{mn_changed}` nicknames successfully changed, `{mn_failed}` failed.")
			await self.bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)
		else:
			await ctx.send(embed=tt.permdeny)

	@commands.command()
	async def guilds(self, ctx):
		await ctx.trigger_typing()
		if ctx.author.id in tt.admins:
			guildlist = ''
			for guild in self.bot.guilds: guildlist = guildlist + f'	 -- {guild.name} ({guild.owner}) [{guild.id}]\n'
			tt.l = f"[{tt._t()}] ADMIN: '{ctx.author}' called for the list of guilds\n"; tt.l = tt.l + guildlist
			await self.bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)
			await ctx.send("> ✅ ⠀guild list sent to logs!")
		else:
			await ctx.send(embed=tt.permdeny)

#	@commands.command()
#	async def inv(self, ctx):
#		await ctx.trigger_typing()
#		if ctx.author.id in tt.admins:
#			invite = await self.invites(433357665633042442)
#			tt.l = "yeah"
#			await self.bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)
#			await ctx.send(invite)
#		else:
#			await ctx.send(embed=tt.permdeny)

	@commands.command()
	async def echo(self, ctx, echochannel: int, *, botsay=None):
		if ctx.author.id in tt.admins:
			if botsay is None:
				await ctx.send("> ⚠️ ⠀please specify what you want me to say!")
			else:
				botsay = botsay.replace("@everyone", "@\u200beveryone")
				botsay = botsay.replace("@here", "@\u200bhere")
				tt.l = f"[{tt._t()}] '{ctx.author}' echoed from '{ctx.guild.name}' to channel ID '{echochannel}' message '{botsay}'"
				await self.bot.get_channel(echochannel).send(botsay)
				await ctx.message.add_reaction('✅')
				await self.bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)
				echochannel = 0
		else:
			await ctx.send(embed=tt.permdeny)

# 		========================

def setup(bot):
	bot.add_cog(admin(bot))
	