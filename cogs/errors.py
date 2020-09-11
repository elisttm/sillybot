import discord
import os, sys
import json
import math
import traceback
from discord.ext import commands
from utils import checks
from utils.funcs import funcs
from data.messages import _a
from data.commands import help_list
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

		if isinstance(error, commands.BotMissingPermissions):
			await ctx.send(_a.bot_no_permission)
			return

		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(_a.on_cooldown.format(math.ceil(error.retry_after)))
			return

		if isinstance(error, commands.MissingPermissions):
			await ctx.send(_a.no_permission)
			return

		if isinstance(error, commands.UserInputError):
			ctx.command.reset_cooldown(ctx)
			command_usage = ''
			invoked_command = ctx.command.name
			if ctx.invoked_subcommand is not None:
				invoked_command = ctx.invoked_subcommand.name
			for cog in help_list.categories:
				for command in help_list.categories[cog]['commands']:
					if command.startswith(invoked_command):
						command_usage = command
			if command_usage != '':
				if ctx.invoked_subcommand is not None:
					command_usage = ctx.command.parent.name+' '+command_usage
				command_usage = f'`({self.determine_prefix(self, ctx.message)}{command_usage})`'
			await ctx.send(_a.invalid_params.format(command_usage))
			return

		if isinstance(error, commands.NoPrivateMessage):
			try: 
				await ctx.author.send(_a.disabled_in_dm)
			except discord.Forbidden: 
				pass
			return

		if isinstance(error, checks.NoPermission):
			await ctx.send(_a.no_permission)
			return

		if isinstance(error, checks.UnmatchedGuild):
			await ctx.send(_a.guild_not_enabled)
			return

		if isinstance(error, commands.CheckFailure):
			await ctx.send(_a.no_permission)
			return

		print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
		traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
		
# 		========================

def setup(bot):
	bot.add_cog(errors(bot))