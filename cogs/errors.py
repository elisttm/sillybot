import discord, math, traceback
from discord.ext import commands
from a import checks
from a.funcs import f
from a.stuff import cmds
import a.constants as tt

def format_perms(error):
	return f.split_list([perm.replace('_',' ').replace('guild','server') for perm in error.missing_permissions],'and','`')

class errors(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		error = getattr(error, 'original', error)

		if isinstance(error, commands.CommandNotFound):
			return

		elif isinstance(error, commands.UserInputError):
			ctx.command.reset_cooldown(ctx)
			command = ctx.command.qualified_name
			cog = ctx.command.cog.qualified_name
			await ctx.send(tt.w+f"invalid command parameters provided!"+(f'\n{tt.s}{tt.s}`{ctx.prefix if str(self.bot.user.id) not in ctx.prefix else "@sillybot "}{cmds._c_[cog][1][command][0]}`' if cog in cmds._c_ and command in cmds._c_[cog][1] else ''))

		elif isinstance(error, commands.DisabledCommand):
			await ctx.send(tt.x+f"this command is currently disabled for maintenance!")
		
		elif isinstance(error, commands.NoPrivateMessage): 
			await ctx.send(tt.x+"this command can only be used in servers!")
	
		elif isinstance(error, commands.BotMissingPermissions):
			await ctx.send(tt.x+f"i need {format_perms(error)} to use this command!")

		elif isinstance(error, commands.MissingPermissions):
			await ctx.send(tt.x+f"you need {format_perms(error)} to use this command!")

		elif isinstance(error, commands.CommandOnCooldown):
			await ctx.send(tt.h+f"please wait `{f.seconds(math.ceil(error.retry_after))}` before using this command again!")

		elif isinstance(error, checks.GuildCommandDisabled):
			await ctx.send(tt.x+"this command is disabled in this server!")

		elif isinstance(error, commands.CheckFailure):
			await ctx.send(tt.x+"you do not have permission to use this command!")

		else:
			f.log(f"Ignoring exception in command '{ctx.command.qualified_name}':\n"+''.join(traceback.format_exception(type(error), error, error.__traceback__)), False, ['temp/error.txt','w'], tt.ansi.red+tt.ansi.bold)
			await ctx.send(tt.w+f"i ran into an error running this command! the error log is attached, please report it with 't!report'!\n**note: sillybot is currently in a testing stage for discord.py 2.0; if you experience any errors, i highly encourage you report them!**", file=discord.File('temp/error.txt'))
			
async def setup(bot):
	await bot.add_cog(errors(bot))
