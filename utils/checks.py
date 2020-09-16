import discord, discord.utils
import json
import os
from discord.ext import commands
from utils.funcs import funcs
import data.constants as tt

# 		========================

class bot_checks():
	def __init__(self, bot):
		self.bot = bot
	
	def get_user_name(self, bot, user_id):
		return self.bot.get_user(user_id).name

# 		========================

class NoPermission(commands.CommandError): pass
class UnmatchedGuild(commands.CommandError): pass

# 		========================

def is_owner(): return commands.check(lambda ctx: is_bot_owner_check(ctx.message))
def is_admin(): return commands.check(lambda ctx: is_bot_admin_check(ctx.message))
def is_server_or_bot_admin(): return commands.check(lambda ctx: is_server_or_bot_admin_check(ctx.message))
def is_in_guilds(guild_ids): return commands.check(lambda ctx: is_in_guilds_check(ctx.message, guild_ids))
def is_bot_admin_or_users(user_ids): return commands.check(lambda ctx: is_bot_admin_or_users_check(ctx.message, user_ids))

# 		========================

def bot_admin(message):
	if message.author.id in tt.admins:
		return True

def guild_admin(message):
	member = message.guild.get_member(message.author.id)
	if (member.guild.owner == message.author) or (member.guild_permissions.administrator) or (member.guild_permissions.manage_guild):
		return True

def guild_mod(message):
	member = message.guild.get_member(message.author.id)
	if member.guild_permissions.manage_messages:
		return True

def is_user(message, user_ids):
	if message.author.id in user_ids:
		return True

# 		========================

def is_in_guilds_check(message, guild_ids):
	if message.guild.id in guild_ids:
		return True
	tt.error_guild_ids = guild_ids
	raise UnmatchedGuild()

def is_bot_owner_check(message):
	if message.author.id == tt.owner_id:
		return True
	tt.error_noperm = 'botowner'
	raise NoPermission()

def is_bot_admin_check(message):
	if bot_admin(message):
		return True
	tt.error_noperm = 'botadmin'
	raise NoPermission()

def is_server_or_bot_admin_check(message):
	if (guild_admin(message)) or (bot_admin(message)):
		return True
	tt.error_noperm = 'serverbotadmin'
	raise NoPermission()

def is_bot_admin_or_users_check(message, user_ids):
	if (bot_admin(message)) or (is_user(message, user_ids)):
		return True
	tt.error_noperm = 'botadminoruser'
	raise NoPermission()

# 		========================