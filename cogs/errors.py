import discord
import traceback
import sys
from discord.ext import commands

# 		========================

class errors(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

# 		========================

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if hasattr(ctx.command, 'on_error'):
			return

			cog = ctx.cog
			if cog:
				if cog._get_overridden_method(cog.cog_command_error) is not None:
					return

			ignored = (commands.CommandNotFound, )
			error = getattr(error, 'original', error)

			if isinstance(error, ignored):
				pass

#			elif isinstance(error, commands.MissingPermissions):
#				await ctx.author.send("you are missing permissions to do that")
#				print("what")

			if isinstance(error, commands.CheckFailure):
				await ctx.send("insufficient permissions (checkfailure)")

			else:
				print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
				traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

# 		========================

def setup(bot):
    bot.add_cog(errors(bot))