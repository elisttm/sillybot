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
			await ctx.send(f'❌ ⠀i do not have permission to do this! {missing_perms}')
			return

		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(f"❌ ⠀please wait `{math.ceil(error.retry_after)}s` before using this command again!")
			return

		if isinstance(error, commands.MissingPermissions):
			await ctx.send(f"❌ ⠀you do not have permission to use this command! ({missing_perms})")
			return

		if isinstance(error, commands.UserInputError):
			await ctx.send("⚠️ ⠀invalid argument(s) provided!")
			return

		if isinstance(error, commands.NoPrivateMessage):
			try: 
				await ctx.author.send('❌ ⠀this command doesnt work in dms!')
			except discord.Forbidden: 
				pass
			return

		if isinstance(error, commands.CheckFailure):
			await ctx.send(tt.permdeny)
			return

		if isinstance(error, commands.CommandInvokeError):
			if 'HTTPException' in str(e):
				if 'status code: 413' in str(e):
					try:
						await ctx.channel.send('❌ ⠀failed to upload file (too large)')
					except:
						pass

		print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
		traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
		
# 		========================

def setup(bot):
	bot.add_cog(errors(bot))