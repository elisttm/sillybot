import discord
from discord.ext import commands
import data.constants as tt

# 		========================

class fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
# 		========================

	@commands.command()
	async def say(self, ctx, *, botsay=None):
		try:
			if botsay is None:
				await ctx.send("⚠️ ⠀please specify what you want me to say!")
			else:
				botsay = tt.sanitize(text = botsay)
				tt.l = f"[{tt._t()}] '{ctx.author}' in '{ctx.guild.name}' said '{botsay}'"
				await ctx.send(botsay)
				await self.bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)
		except Exception as e: 
			await ctx.send(tt.msg_e.format(e))

# 		========================

def setup(bot):
	bot.add_cog(fun(bot))