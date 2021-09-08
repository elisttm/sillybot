import discord, math, traceback
from discord.ext import commands
from a import checks
from a.funcs import f
import a.commands as cmds
import a.constants as tt

class errors(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def format_perms(error):
		return f.split_list([perm.replace('_',' ').replace('guild', 'server') for perm in error.missing_perms],'and','`')

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
#		if hasattr(ctx.command, 'on_error'):
#			return

		error = getattr(error, 'original', error)

		if isinstance(error, commands.CommandNotFound):
			return

		if isinstance(error, commands.NoPrivateMessage):
			try: 
				await ctx.author.send(tt.x+"this command cannot be used in dms!")
			except discord.Forbidden: 
				pass
			return

		if isinstance(error, checks.GuildCommandDisabled):
			await ctx.send(tt.x+"this command is disabled in this server!")
			return

		if isinstance(error, checks.NoPermission):
			await ctx.send( tt.x+"you do not have permission to use this command!")
			return
	
		if isinstance(error, commands.BotMissingPermissions):
			await ctx.send(tt.x+f"i am missing required permissions for this command! ({self.format_perms(error)})")
			return

		if isinstance(error, commands.MissingPermissions):
			await ctx.send(tt.x+f"you are missing required permissions for this command! ({self.format_perms(error)})")
			return

		if isinstance(error, commands.CommandOnCooldown):
			s = math.ceil(error.retry_after); m=h=0
			_time_ = f"{s}s"
			if s > 60:
				m, s = divmod(s, 60)
				_time_ = f"{m}m {s}s"
			if m > 60:
				h, m = divmod(m, 60)
				_time_ = f"{h}h {m}m {s}s"
			await ctx.send(tt.e['hourglass']+tt.s+f"please wait `{_time_}` before using this command again!")
			return

		if isinstance(error, commands.UserInputError):
			ctx.command.reset_cooldown(ctx)
			usage = ''
			command = ctx.command.name
			if ctx.invoked_subcommand is not None:
				command = ctx.invoked_subcommand.name
			for ctg in cmds._c_:
				if command in cmds._c_[ctg][1]:
					usage = cmds._c_[ctg][1][command][0]
			if usage != '':
				usage = f'\n{tt.s}{tt.s}`({f.determine_prefix(self, ctx.message)}{usage})`'
			await ctx.send(tt.w+f"invalid command parameters provided! {usage}")
			return

		if isinstance(error, commands.CheckFailure):
			await ctx.send(tt.x+"you do not have permission to use this command!")
			return

		f.log(f"Ignoring exception in command '{ctx.command}':\n"+''.join(traceback.format_exception(type(error), error, error.__traceback__)), False, [tt.error,'w'])
		await ctx.send(tt.w+"i ran into an error running this command! the full error log is attached, feel free to report it!", file=discord.File(tt.error))
		
def setup(bot):
	bot.add_cog(errors(bot))