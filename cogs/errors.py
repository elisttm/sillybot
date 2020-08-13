import discord
import traceback
import sys
import math
from discord.ext import commands

# 		========================

class errors(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

# 		========================

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
#		if hasattr(ctx.command, 'on_error'):
#			return

		error = getattr(error, 'original', error)

		if isinstance(error, commands.CommandNotFound):
			return

		if isinstance(error, commands.BotMissingPermissions):
			await ctx.send('⚠️ ⠀i do not have permission to do this!')
			return

		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send("⚠️ ⠀please wait {}s before using this command again!".format(math.ceil(error.retry_after)))
			return

		if isinstance(error, commands.MissingPermissions):
			await ctx.send(embed=tt.permdeny)
			return

		if isinstance(error, commands.UserInputError):
			await ctx.send("⚠️ ⠀invalid argument given!")
			return

		if isinstance(error, commands.NoPrivateMessage):
			try: 
				await ctx.author.send('⚠️ ⠀this command doesnt work in dms!')
			except discord.Forbidden: 
				pass
			return

		if isinstance(error, commands.CheckFailure):
			await ctx.send(embed=tt.permdeny)
			return

		print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
		traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
		
# 		========================

def setup(bot):
	bot.add_cog(errors(bot))