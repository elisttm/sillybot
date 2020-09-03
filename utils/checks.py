import discord, discord.utils
import json
import os
from discord.ext import commands
import data.constants as tt

class No_Permission(commands.CommandError): pass
class Unmatched_Guild(commands.CommandError): pass

def is_owner():
	return commands.check(lambda ctx: is_owner_check(ctx.message))

def is_admin():
	return commands.check(lambda ctx: is_admin_check(ctx.message))

def is_in_guild(guild_ids):
	return commands.check(lambda ctx: is_in_guild_check(message = ctx.message, guild_ids = guild_ids))

def is_server_or_bot_admin():
	return commands.check(lambda ctx: is_server_or_bot_admin_check(ctx.message))

def is_owner_check(message):
	if message.author.id == tt.owner_id:
		return True
	raise No_Permission()

def is_admin_check(message):
	if message.author.id in tt.admins:
		return True
	raise No_Permission()

def is_in_guild_check(message, guild_ids):
	if message.guild.id in guild_ids:
		return True
	raise Unmatched_Guild()

def is_server_or_bot_admin_check(message):
	member = message.guild.get_member(message.author.id)
	if member.guild_permissions.administrator:
		return True
	if member.guild_permissions.manage_server:
		return True
	if member.id in tt.admins:
		return True
	raise No_Permission()