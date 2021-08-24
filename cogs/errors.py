import discord, os, sys, math, traceback
from discord.ext import commands
from a import checks
from a.funcs import funcs
import a.commands as cmds
import a.constants as tt

class errors(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.determine_prefix = funcs.determine_prefix

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
#		if hasattr(ctx.command, 'on_error'):
#			return

		error = getattr(error, 'original', error)

		if isinstance(error, commands.CommandNotFound):
			return

		if isinstance(error, commands.NoPrivateMessage):
			try: await ctx.author.send(tt.x+"that command only avaialable in servers!")
			except discord.Forbidden: pass
			return

		if isinstance(error, checks.GuildCommandDisabled):
			await ctx.send(tt.x+"that command is disabled in this server!")
			return

		if isinstance(error, checks.NoPermission):
			await ctx.send( tt.x+"you do not have permission to use this command!")
			return
	
		if isinstance(error, commands.BotMissingPermissions):
			missing = [perm.replace('_',' ').replace('guild', 'server') for perm in error.missing_perms]
			msg = f"`{tt.split_list(missing, 'and')}`"
			await ctx.send(tt.x+f"i do not have the required permissions to use this command! ({msg})")
			return

		if isinstance(error, commands.MissingPermissions):
			missing = [perm.replace('_',' ').replace('guild', 'server') for perm in error.missing_perms]
			msg = f"`{tt.split_list(missing, 'and')}`"
			await ctx.send(tt.x+f"you do not have the required permissions to use this command! ({msg})")
			return

		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(tt.x+f"please wait `{math.ceil(error.retry_after)}s` before using this command again!")
			return

		if isinstance(error, commands.UserInputError):
			ctx.command.reset_cooldown(ctx)
			command_usage = ''
			invoked_command = ctx.command.name
			if ctx.invoked_subcommand is not None:
				invoked_command = ctx.invoked_subcommand.name
			for ctg in cmds._c_:
				if invoked_command in cmds._c_[ctg][1]:
					command_usage = cmds._c_[ctg][1][invoked_command][0]
			if command_usage != '':
				command_usage = f'\n{tt.s}{tt.s}`({self.determine_prefix(self, ctx.message)}{command_usage})`'
			await ctx.send(tt.w+f"invalid command parameter(s) provided! {command_usage}")
			return

		if isinstance(error, commands.CheckFailure):
			await ctx.send(tt.x+"you do not have permission to use this command!")
			return

		print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
		traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
		
def setup(bot):
	bot.add_cog(errors(bot))