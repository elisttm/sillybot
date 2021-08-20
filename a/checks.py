import os
from discord.ext import commands
from a.funcs import funcs
import a.constants as tt

class NoPermission(commands.CommandError): pass	
class GuildCommandDisabled(commands.CommandError): pass

def is_owner(): return commands.check(lambda ctx: is_bot_owner_check(ctx.message))
def is_admin(): return commands.check(lambda ctx: is_bot_admin_check(ctx.message))
def is_guild_admin(): return commands.check(lambda ctx: is_guild_admin_check(ctx.message))
def is_in_guilds(guild_ids): return commands.check(lambda ctx: is_guild_check(ctx.message, guild_ids))
def is_user(user_ids): return commands.check(lambda ctx: is_user_check(ctx.message, user_ids))
def is_tag_disabled(): return commands.check(lambda ctx: tags_disabled_check(ctx.message))

command_user_ids = {}

def bot_owner(message):
	if message.author.id == tt.owner_id:
		return True

def bot_admin(message):
	if (message.author.id in tt.admins) or (bot_owner(message)):
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
	if (message.guild.owner == message.author) or (bot_admin(message)):
		return True
	member = message.guild.get_member(message.author.id)
	admin_permissions = (
		member.guild_permissions.administrator,
		member.guild_permissions.manage_guild,
	)
	if any(admin_permissions):
		return True
	raise NoPermission()

def is_user_check(message, user_ids):
	if (message.author.id in user_ids):
		return True
	raise NoPermission()

def is_guild_check(message, guild_ids):
	if bot_owner(message):
		return True
	if message.guild.id in guild_ids:
		return True
	raise GuildCommandDisabled()

def tags_disabled_check(message):
	guild_data_path = tt.guild_data_path.format(str(message.guild.id))
	if not os.path.exists(guild_data_path):
		return True
	guild_data = funcs.load_db(guild_data_path)
	if 'globaltags' not in guild_data or guild_data['globaltags'] == True:
		return True
	raise GuildCommandDisabled()
	