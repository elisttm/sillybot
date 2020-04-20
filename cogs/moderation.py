import discord, asyncio
from discord.ext import commands
import data.constants as tt

# 		========================

class moderation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
# 		========================

	@commands.command()
	@commands.has_permissions(kick_members = True)
	async def kick(self, ctx, user:discord.Member=None, *, reason=None):
		await ctx.trigger_typing()
		if ctx.author.id != tt.owner_id: await ctx.send(embed=tt.permdeny)
		else:
			try:
				if reason == None: reason = 'no reason given'
				if user is None: await ctx.send("> ⚠️ ⠀please specify who you want to kick!")
				else:
					await ctx.guild.kick(user, reason=reason)
					await ctx.send(f"> ✅ ⠀kicked `{user.name}#{user.discriminator}` for `{reason}`")
					tt.l = f"[{tt._t()}] MODERATION: '{ctx.guild.name}' '{ctx.author}'"
				await self.bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)
			except Exception as error:
				await ctx.send(tt.msg_e.format(error))


	@commands.command()
	@commands.has_permissions(ban_members = True)
	async def ban(self, ctx, user:discord.Member=None, *, reason=None):
		await ctx.trigger_typing()
		if ctx.author.id != tt.owner_id: await ctx.send(embed=tt.permdeny)
		else:
			if reason == None: reason = 'no reason given'
			if user is None: await ctx.send("> ⚠️ ⠀please specify who you want to ban!")
			else:
				try:
					tt.l = f"[{tt._t()}] MODERATION: '{ctx.author}' banned {user} in '{ctx.guild.name}'"
					await ctx.guild.ban(user, reason=f"banned by {ctx.author}: {reason}")
					await ctx.send(f"> ✅ ⠀banned `{user.name}#{user.discriminator}` for `{reason}`")
					await self.bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)
				except Exception as error:
						await ctx.send(tt.msg_e.format(error))


	@commands.command()
	@commands.has_permissions(manage_messages = True)
	async def clear(self, ctx, clear:int=None, *, reason=None):
		if ctx.author.id != tt.owner_id: await ctx.send(embed=tt.permdeny)
		else:
			try:
				if clear is None: await ctx.send("> ⚠️ ⠀please specify how many messages you want to clear!")
				elif clear == 0: await ctx.send("> ⚠️ ⠀i cant clear 0 messages!")
				elif clear > 100: await ctx.send("> ⚠️ ⠀i can only clear 100 messages at a time!")
				else:
					await ctx.message.delete()
					await ctx.channel.purge(limit=(clear))
					await ctx.send(f"> ✅ ⠀cleared `{clear}` messages", delete_after=2)
			except Exception as error:
				await ctx.send(tt.msg_e.format(error))


# 		========================

def setup(bot):
	bot.add_cog(moderation(bot))
	