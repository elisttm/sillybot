import discord
from discord.ext import commands
import a.constants as tt

class GuildCommandDisabled(commands.CommandError): pass

def is_bot_owner(): return commands.check(lambda ctx: bot_owner_check(ctx))
def is_bot_admin(): return commands.check(lambda ctx: bot_admin_check(ctx))
def is_guild_admin(): return commands.check(lambda ctx: guild_admin_check(ctx))
def is_guild(guild_ids): return commands.check(lambda ctx: guild_check(ctx, guild_ids))
def is_user(user_ids): return commands.check(lambda ctx: user_check(ctx, user_ids))

def bot_owner(ctx):
	return ctx.author.id == tt.admins[0]

def bot_admin(ctx):
	return ctx.author.id in tt.admins
		
def dm_channel(ctx):
	return isinstance(ctx.channel, discord.channel.DMChannel)

def guild_owner(ctx):
	return ctx.guild.owner == ctx.author

def bot_owner_check(ctx):
	if bot_owner(ctx):
		return True
	raise(commands.CheckFailure)

def bot_admin_check(ctx):
	if bot_admin(ctx):
		return True
	raise(commands.CheckFailure)

def guild_admin_check(ctx):
	if any([ctx.author.guild_permissions.administrator, guild_owner(ctx), bot_admin(ctx), not dm_channel(ctx)]):
		return True
	raise(commands.CheckFailure)

def user_check(ctx, user_ids):
	if ctx.author.id in user_ids or bot_owner(ctx):
		return True
	raise(commands.CheckFailure)

def guild_check(ctx, guild_ids):
	if ctx.guild.id in guild_ids or ctx.guild.id == tt.servers.test:
		return True
	raise GuildCommandDisabled()
