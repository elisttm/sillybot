import discord
from discord.ext import commands
from a.funcs import f
import a.constants as tt

class NoPermission(commands.CommandError): pass	
class GuildCommandDisabled(commands.CommandError): pass

def is_owner(): return commands.check(lambda ctx: is_bot_owner_check(ctx.message))
def is_admin(): return commands.check(lambda ctx: is_bot_admin_check(ctx.message))
def is_guild_admin(): return commands.check(lambda ctx: is_guild_admin_check(ctx.message))
def is_guild(guild_ids): return commands.check(lambda ctx: is_guild_check(ctx.message, guild_ids))
def is_user(user_ids): return commands.check(lambda ctx: is_user_check(ctx.message, user_ids))

def bot_owner(message):
	if message.author.id == tt.admins[0]:
		return True

def bot_admin(message):
	if message.author.id in tt.admins:
		return True

def dm_channel(message):
	if isinstance(message.channel, discord.channel.DMChannel):
		return True

def is_bot_owner_check(message):
	if bot_owner(message):
		return True
	raise NoPermission()

def is_bot_admin_check(message):
	if bot_admin(message):
		return True
	raise NoPermission()

def is_guild_admin_check(message):
	member = message.guild.get_member(message.author.id)
	if dm_channel(message) or bot_admin(message) or message.guild.owner == message.author or any([member.guild_permissions.administrator, member.guild_permissions.manage_guild]):
		return True
	raise NoPermission()

def is_user_check(message, user_ids):
	if bot_owner(message) or message.author.id in user_ids:
		return True
	raise NoPermission()

def is_guild_check(message, guild_ids):
	if dm_channel(message) or bot_owner(message) or message.guild.id in guild_ids:
		return True
	raise GuildCommandDisabled()