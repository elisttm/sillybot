import discord
from discord.ext import commands
from utils import checks
from utils.funcs import funcs
import data.constants as tt

# 		========================

class moderation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	


# 		========================
	
	@commands.command()
	@commands.guild_only()
	@checks.is_in_guild([tt.srv['rhc']])
	@commands.has_permissions(manage_roles = True)
	async def restrict(self, ctx, user:discord.Member, restriction:str):
		await ctx.trigger_typing()
		try:
			if restriction not in tt.rhc_restrictions:
				await ctx.send(f"❌ ⠀invalid restriction! ({', '.join(tt.rhc_restrictions)})")
				return
			role = ctx.guild.get_role(tt.rhc_restrictions[restriction])
			if role in user.roles:
				await ctx.send(f"❌ ⠀{user.name} already has the restriction '{restriction}'")
			else:
				await user.add_roles(role)
				await ctx.send(f"✅ ⠀{user.name} has been given the restriction '{restriction}'")
		except Exception as e: 
			await ctx.send(tt.msg_e.format(e))

	@commands.command()
	@commands.guild_only()
	@checks.is_in_guild([tt.srv['rhc']])
	@commands.has_permissions(manage_roles = True)
	async def unrestrict(self, ctx, user:discord.Member, restriction:str):
		await ctx.trigger_typing()
		try:
			if restriction not in tt.rhc_restrictions:
				await ctx.send(f"❌ ⠀invalid restriction! ({', '.join(tt.rhc_restrictions)})")
				return
			role = ctx.guild.get_role(tt.rhc_restrictions[restriction])
			if role in user.roles:
				await user.remove_roles(role)
				await ctx.send(f"✅ ⠀removed the restriction '{restriction}' from {user.name}")
			else:
				await ctx.send(f"❌ ⠀{user.name} does not have the restriction '{restriction}'")
		except Exception as e: 
			await ctx.send(tt.msg_e.format(e))

# 		========================

def setup(bot):
	bot.add_cog(moderation(bot))