import discord
from discord.ext import commands
import data.constants as tt

# 		========================

restrictions = {
	'serious' : 705870681849594027,
	'reaction' : 747664614493519962,
	'image' : 714875237644108140,
	'vc' : 719987120441131048,
	'dino' : 746068022401302663,
	'poop' : 745008022773956609,
}

class moderation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	def is_in_guild(guild_id):
		async def predicate(ctx):
			return ctx.guild and ctx.guild.id == guild_id
		return commands.check(predicate)

# 		========================
	
	@commands.command()
	@commands.guild_only()
	@is_in_guild(695967253900034048) # rhc
	@commands.has_permissions(manage_roles = True)
	async def restrict(self, ctx, user:discord.Member, restriction:str):
		await ctx.trigger_typing()
		try:
			if restriction in restrictions:
				role = ctx.guild.get_role(restrictions[restriction])
				if role in user.roles:
					await ctx.send(f"❌ ⠀{user.name} already has the restriction '{restriction}'")
				else:
					await user.add_roles(role)
					await ctx.send(f"✅ ⠀{user.name} has been given the restriction '{restriction}'")
			else:
				await ctx.send(f"❌ ⠀invalid restriction! ({', '.join(restrictions)})")
		except Exception as e: 
			await ctx.send(tt.msg_e.format(e))

	@commands.command()
	@commands.guild_only()
	@is_in_guild(695967253900034048) # rhc
	@commands.has_permissions(manage_roles = True)
	async def unrestrict(self, ctx, user:discord.Member, restriction:str):
		await ctx.trigger_typing()
		try:
			if restriction in restrictions:
				role = ctx.guild.get_role(restrictions[restriction])
				if role in user.roles:
					await user.remove_roles(role)
					await ctx.send(f"✅ ⠀removed the restriction '{restriction}' from {user.name}")
				else:
					await ctx.send(f"❌ ⠀{user.name} does not have the restriction '{restriction}'")
			else:
				await ctx.send(f"❌ ⠀invalid restriction! ({', '.join(restrictions)})")
		except Exception as e: 
			await ctx.send(tt.msg_e.format(e))

# 		========================

def setup(bot):
	bot.add_cog(moderation(bot))