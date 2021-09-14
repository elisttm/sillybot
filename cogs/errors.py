import discord, math, traceback, sys
from discord.ext import tasks, commands
from a import checks
from a.funcs import f
import a.commands as cmds
import a.constants as tt

def format_perms(error):
	return f.split_list([perm.replace('_',' ').replace('guild', 'server') for perm in error.missing_perms],'and','`')

class errors(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.send_log.start()

	def cog_unload(self):
		self.send_log.cancel()

	@tasks.loop(minutes=1.0)
	async def send_log(self):
		await self.bot.wait_until_ready()
		logdata = tt.yeah.find_one({'_id':'logs'})
		if len(logdata['log']) > 2:
			await self.bot.get_channel(tt.channels['log']).send(f"```{tt.n.join(logdata['log'])[:1990]}```")
			tt.yeah.update_one({'_id':'logs'},{"$set":{'log':[]}})

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
	#	if hasattr(ctx.command, 'on_error'):
	#		return

		error = getattr(error, 'original', error)

		if isinstance(error, commands.CommandNotFound):
			return

		elif isinstance(error, commands.UserInputError):
			ctx.command.reset_cooldown(ctx)
			usage = ''
			command = ctx.command.qualified_name
			for ctg in cmds._c_:
				if command in cmds._c_[ctg][1]:
					usage = f'\n{tt.s}{tt.s}`{ctx.prefix if str(self.bot.user.id) not in ctx.prefix else tt.p}{cmds._c_[ctg][1][command][0]}`'
					break
			await ctx.send(tt.w+f"invalid command parameters provided! {usage}")

		elif isinstance(error, commands.DisabledCommand):
			await ctx.send(tt.x+f"this command is currently disabled for maintenance!")
		
		elif isinstance(error, commands.NoPrivateMessage): 
			await ctx.send(tt.x+"this command can only be used in servers!")
	
		elif isinstance(error, commands.BotMissingPermissions):
			await ctx.send(tt.x+f"i need {format_perms(error)} to use this command!")

		elif isinstance(error, commands.MissingPermissions):
			await ctx.send(tt.x+f"you need {format_perms(error)} to use this command!")

		elif isinstance(error, commands.CommandOnCooldown):
			await ctx.send(tt.e.hourglass+tt.s+f"please wait `{f.timecount(math.ceil(error.retry_after))}` before using this command again!")

		elif isinstance(error, checks.GuildCommandDisabled):
			await ctx.send(tt.x+"this command is disabled in this server!")

		elif isinstance(error, checks.NoPermission):
			await ctx.send( tt.x+"you do not have permission to use this command!")

		elif isinstance(error, commands.CheckFailure):
			await ctx.send(tt.x+"you do not have permission to use this command!")

		else:
			f.log(f"Ignoring exception in command '{ctx.command.qualified_name}':\n"+''.join(traceback.format_exception(type(error), error, error.__traceback__)), False, ['misc/error.txt','w'])
			await ctx.send(tt.w+f"i ran into an error running this command! the error log is attached, please feel free to report it with t!report!", file=discord.File('misc/error.txt'))
			open("misc/error.txt", "a").truncate().close()
			
def setup(bot):
	bot.add_cog(errors(bot))