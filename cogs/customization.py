import discord
import os
import json
from discord.ext import commands
from utils import checks
from utils.funcs import funcs
import data.constants as tt

# 		========================

class customization(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.load_db = funcs.load_db
		self.dump_db = funcs.dump_db
		self.check_for_db = funcs.check_for_db
		self.send_log = funcs.send_log
		self.log_prefix = "[CUSTOMIZATION] "
		
# 		========================

	@commands.group(name = 'settings', aliases=['s', 'custom'])
	@commands.guild_only()
	async def settings(self, ctx):
		if ctx.invoked_subcommand is None:
			guild_data_path = tt.guild_data_path.format(str(ctx.guild.id))
			prefix = 'default'; msgchannel = 'not set'; joinmsg = 'not set'; leavemsg = 'not set'; banmsg = 'not set'
			if not os.path.exists(guild_data_path):
				await ctx.send("⚠️ ⠀this guild does not have any custom settings!")
				return
			guild_data = self.load_db(guild_data_path)
			if 'prefix' in guild_data:
				prefix = guild_data['prefix']
			if 'events' in guild_data:
				if 'channel' in guild_data['events']:
					msgchannel = self.bot.get_channel(guild_data['events']['channel'])
				if 'join' in guild_data['events']:
					joinmsg = guild_data['events']['join']
				if 'leave' in guild_data['events']:
					leavemsg = guild_data['events']['leave']
				if 'ban' in guild_data['events']:
					banmsg = guild_data['events']['ban']
			e_settings = discord.Embed(title=f"click here for documentation on using this command", url=tt.settings_page, description=f"these are the settings for trashbot for this specific guild\n", color=tt.clr['pink'])
			e_settings.set_author(name=f"trashbot settings", icon_url=tt.ico['cog'])
			e_settings.add_field(name="general", value=f"```py\nprefix : \"{prefix}\"\n```", inline=False)
			e_settings.add_field(name="events", value=f"```py\nmsgchannel : \"#{msgchannel}\"\njoinmsg : \"{joinmsg}\"\nleavemsg : \"{leavemsg}\"\nbanmsg : \"{banmsg}\"\n```", inline=False)
			#e_user.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url_as(format='png'))
			await ctx.send(embed=e_settings)

	#			-----  CUSTOM PREFIX  -----

	@settings.group(name = 'prefix')
	async def prefix(self, ctx):
		await ctx.trigger_typing()
		if ctx.invoked_subcommand is None:
			try:
				guild_data_path = tt.guild_data_path.format(str(ctx.guild.id))
				if not os.path.exists(guild_data_path):
					await ctx.send("⚠️ ⠀no custom prefix for this guild!")
					return
				guild_data = self.load_db(guild_data_path)
				if 'prefix' not in guild_data:
					await ctx.send("⚠️ ⠀no custom prefix for this guild!")
					return
				await ctx.send(f"ℹ️ ⠀this guild's custom prefix is '{guild_data['prefix']}'")
			except Exception as error:
				await ctx.send(tt.msg_e.format(error))

	@prefix.command(name = 'set')
	@checks.is_server_or_bot_admin()
	async def prefix_set(self, ctx, prefix:str):
		try:
			if prefix == tt.p:
				await ctx.invoke(self.bot.get_command('prefix reset'))
				return
			if len(prefix) > 10:
				await ctx.send("⚠️ ⠀prefix too long! (max of 10 characters)")
				return
			guild_data_path = tt.guild_data_path.format(str(ctx.guild.id))
			self.check_for_db(guild_data_path)
			guild_data = self.load_db(guild_data_path)
			guild_data['prefix'] = prefix
			self.dump_db(guild_data_path, guild_data)
			await ctx.send(f"✅ ⠀custom prefix for this guild set to '{prefix}'")
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	@prefix.command(name = 'reset')
	@checks.is_server_or_bot_admin()
	async def prefix_reset(self, ctx):
		try:
			guild_data_path = tt.guild_data_path.format(str(ctx.guild.id))
			if not os.path.exists(guild_data_path):
				await ctx.send(f"❌ ⠀this guild does not have a custom prefix set!")
				return
			guild_data = self.load_db(guild_data_path)
			if 'prefix' not in guild_data:
				await ctx.send(f"❌ ⠀this guild does not have a custom prefix set!")
				return
			del guild_data['prefix']
			self.dump_db(guild_data_path, guild_data)
			await ctx.send(f"✅ ⠀prefix for this guild set to default!")
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	#			-----  EVENT MESSAGES CHANNEL  -----

	@settings.group(name = 'msgchannel')
	async def msgchannel(self, ctx):
		if ctx.invoked_subcommand is None:
			try:
				guild_data_path = tt.guild_data_path.format(str(ctx.guild.id))
				if not os.path.exists(guild_data_path):
					await ctx.send("❌ ⠀this guild does not have an event messages channel set!")
					return
				guild_data = self.load_db(guild_data_path)
				if ('events' not in guild_data) or ('channel' not in guild_data['events']):
					await ctx.send("❌ ⠀this guild does not have an event messages channel set!")
					return
				guild_data = self.load_db(guild_data_path)
				channel = self.bot.get_channel(guild_data['events']['channel'])
				await ctx.send(f"ℹ️ ⠀the event messages channel for this guild is {channel.mention}")
			except Exception as error:
				await ctx.send(tt.msg_e.format(error))

	@msgchannel.command(name = 'set')
	@checks.is_server_or_bot_admin()
	async def msgchannel_set(self, ctx, channel:discord.TextChannel = None):
		try:
			guild_data_path = tt.guild_data_path.format(str(ctx.guild.id))
			self.check_for_db(guild_data_path)
			guild_data = self.load_db(guild_data_path)
			guild_data['events']['channel'] = channel
			self.dump_db(guild_data_path, guild_data)
			await ctx.send(f"✅ ⠀set the guild event messages channel!")
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	@msgchannel.command(name = 'reset')
	@checks.is_server_or_bot_admin()
	async def msgchannel_reset(self, ctx):
		try:
			guild_data_path = tt.guild_data_path.format(str(ctx.guild.id))
			if not os.path.exists(guild_data_path):
				await ctx.send("❌ ⠀this guild does not have an event messages channel set!")
				return
			guild_data = self.load_db(guild_data_path)
			del guild_data['events']['channel']
			self.dump_db(guild_data_path, guild_data)
			await ctx.send(f"✅ ⠀removed the guild event messages channel!")
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	#			-----  EVENT MESSAGES  -----

	@commands.command()
	async def event(self, ctx, action, event, message = None):
		try:
			guild_data_path = tt.guild_data_path.format(str(ctx.guild.id))
			if action == 'check':
				if not os.path.exists(guild_data_path):
					await ctx.send(f"❌ ⠀this guild does not have a {event} message set!")
					return
				guild_data = self.load_db(guild_data_path)
				if ('events' not in guild_data) or (event not in guild_data['events']):
					await ctx.send(f"❌ ⠀this guild does not have a {event} message set!")
					return
				await ctx.send(f"ℹ️ ⠀the custom join message for this guild is '{guild_data['events']['join']}'")
				return
			if action == 'set':
				self.check_for_db(guild_data_path)
				guild_data = self.load_db(guild_data_path)
				if (event in guild_data['events']) and (guild_data['events'][event] == message):
					await ctx.send(f"❌ ⠀this guilds {event} message is already set to that!")
					return
				guild_data['events'][event] = message
				await ctx.send(f"✅ ⠀set the guild {event} message!")
			if action == 'reset':
				if not os.path.exists(guild_data_path):
					await ctx.send(f"❌ ⠀this guild does not have a {event} message set!")
					return
				guild_data = self.load_db(guild_data_path)
				if event not in guild_data['events']:
					await ctx.send(f"❌ ⠀this guild does not have a {event} message set!")
					return
				del guild_data['events'][event]
				await ctx.send(f"✅ ⠀removed the guild {event} message!")
			self.dump_db(guild_data_path, guild_data)
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	#			-----  JOIN  -----

	@settings.group(name = 'joinmsg')
	async def joinmsg(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.invoke(self.bot.get_command('event'), action='check', event='join')

	@joinmsg.command(name = 'set')
	@checks.is_server_or_bot_admin()
	async def joinmsg_set(self, ctx, *, message:str):
		await ctx.invoke(self.bot.get_command('event'), action='set', event='join', message=message)

	@joinmsg.command(name = 'reset')
	@checks.is_server_or_bot_admin()
	async def joinmsg_reset(self, ctx):
		await ctx.invoke(self.bot.get_command('event'), action='reset', event='join')

	#			-----  LEAVE  -----

	@settings.group(name = 'leavemsg')
	async def leavemsg(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.invoke(self.bot.get_command('event'), action='check', event='leave')

	@leavemsg.command(name = 'set')
	@checks.is_server_or_bot_admin()
	async def leavemsg_set(self, ctx, *, message:str):
		await ctx.invoke(self.bot.get_command('event'), action='set', event='leave', message=message)

	@leavemsg.command(name = 'reset')
	@checks.is_server_or_bot_admin()
	async def leavemsg_reset(self, ctx):
		await ctx.invoke(self.bot.get_command('event'), action='reset', event='leave')

	#			-----  BAN  -----

	@settings.group(name = 'banmsg')
	async def banmsg(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.invoke(self.bot.get_command('event'), action='check', event='ban')

	@banmsg.command(name = 'set')
	@checks.is_server_or_bot_admin()
	async def banmsg_set(self, ctx, *, message:str):
		await ctx.invoke(self.bot.get_command('event'), action='set', event='ban', message=message)

	@banmsg.command(name = 'reset')
	@checks.is_server_or_bot_admin()
	async def banmsg_reset(self, ctx):
		await ctx.invoke(self.bot.get_command('event'), action='reset', event='ban')

# 		========================

def setup(bot):
	bot.add_cog(customization(bot))