import discord, asyncio
from discord.ext import commands
import data.constants as tt

# 		========================

class moderation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
# 		========================

	@commands.command(aliases=['purge'])
	@commands.has_permissions(manage_messages = True)
	async def clear(self, ctx, clear:int=None, *, reason=None):
#		if ctx.author.id != tt.owner_id: await ctx.send(embed=tt.permdeny)
#		else:
		try:
			if clear is None: await ctx.send("```⚠️ ⠀please specify how many messages you want to clear!```")
			elif clear == 0: await ctx.send("```⚠️ ⠀please specify more than 0 messages!```")
			elif clear > 100: await ctx.send("```⚠️ ⠀i can only clear 100 messages at a time!```")
			else:
				await ctx.message.delete()
				await ctx.channel.purge(limit=(clear))
				await ctx.send(f"> ✅ ⠀cleared `{clear}` messages", delete_after=2)
		except Exception as e: await ctx.send(tt.msg_e.format(e))

# 		========================

def setup(bot):
	bot.add_cog(moderation(bot))
	