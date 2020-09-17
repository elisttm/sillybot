import discord
import os, sys
import json
import math
import traceback
from discord.ext import commands
from utils import checks
from utils.funcs import funcs
from data.messages import _a
from data.commands import cmdl
import data.constants as tt

# 		========================

class errors(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.determine_prefix = funcs.determine_prefix

# 		========================

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
#		if hasattr(ctx.command, 'on_error'):
#			return

		error = getattr(error, 'original', error)

		if isinstance(error, commands.CommandNotFound):
			return

		if isinstance(error, commands.NoPrivateMessage):
			try: 
				await ctx.author.send(_a.disabled_in_dm)
			except discord.Forbidden: 
				pass
			return

		if isinstance(error, checks.UnmatchedGuild):
			await ctx.send(_a.guild_not_enabled)
			return
	
		if isinstance(error, checks.NoPermission):
			await ctx.send(_a.no_permission)
			return
	
		if isinstance(error, commands.BotMissingPermissions):
			missing = [perm.replace('_', ' ').replace('guild', 'server') for perm in error.missing_perms]
			msg = f"`{tt.split_list(missing, 'and')}`"
			await ctx.send(_a.no_permission_perms.format('i', msg))
			return

		if isinstance(error, commands.MissingPermissions):
			missing = [perm.replace('_', ' ').replace('guild', 'server') for perm in error.missing_perms]
			msg = f"`{tt.split_list(missing, 'and')}`"
			await ctx.send(_a.no_permission_perms.format('you', msg))
			return

		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(_a.on_cooldown.format(math.ceil(error.retry_after)))
			return

		if isinstance(error, commands.UserInputError):
			ctx.command.reset_cooldown(ctx)
			command_usage = ''
			invoked_command = ctx.command.name
			if ctx.invoked_subcommand is not None:
				invoked_command = ctx.invoked_subcommand.name
			for ctg in cmdl.ctgs:
				for cmd in cmdl.ctgs[ctg]['cmds']:
					if cmd == invoked_command:
						command_usage = cmdl.ctgs[ctg]['cmds'][cmd]['usage']
			if command_usage != '':
				command_usage = f'\n{tt.s}{tt.s}`({self.determine_prefix(self, ctx.message)}{command_usage})`'
			await ctx.send(_a.invalid_params.format(command_usage))
			return

		if isinstance(error, commands.CheckFailure):
			await ctx.send(_a.no_permission)
			return

		print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
		traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
		
# 		========================

def setup(bot):
	bot.add_cog(errors(bot))