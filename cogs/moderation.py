import discord
import os
import json
from discord.ext import commands
from utils import checks
from utils.funcs import funcs
import data.constants as tt

# 		========================

rhc_restrictions = {
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
		self.load_db = funcs.load_db
		self.dump_db = funcs.dump_db
	
# 		========================
	
	@commands.command()
	@commands.guild_only()
	@checks.is_in_guild([tt.srv['rhc']])
	@commands.has_permissions(manage_roles = True)
	async def restrict(self, ctx, user:discord.Member, restriction:str):
		await ctx.trigger_typing()
		try:
			if restriction not in rhc_restrictions:
				return await ctx.send(tt.x+f"invalid restriction! ({', '.join(rhc_restrictions)})")
			role = ctx.guild.get_role(rhc_restrictions[restriction])
			if role in user.roles:
				await ctx.send(tt.x+f"{user.name} already has the restriction '{restriction}'")
			else:
				await user.add_roles(role)
				await ctx.send(tt.y+f"{user.name} has been given the restriction '{restriction}'")
		except Exception as e: 
			await ctx.send(tt.msg_e.format(e))

	@commands.command()
	@commands.guild_only()
	@checks.is_in_guild([tt.srv['rhc']])
	@commands.has_permissions(manage_roles = True)
	async def unrestrict(self, ctx, user:discord.Member, restriction:str):
		await ctx.trigger_typing()
		try:
			if restriction not in rhc_restrictions:
				return await ctx.send(tt.x+f"invalid restriction! ({', '.join(rhc_restrictions)})")
			role = ctx.guild.get_role(rhc_restrictions[restriction])
			if role in user.roles:
				await user.remove_roles(role)
				await ctx.send(tt.y+f"removed the restriction '{restriction}' from {user.name}")
			else:
				await ctx.send(tt.x+f"{user.name} does not have the restriction '{restriction}'")
		except Exception as e: 
			await ctx.send(tt.msg_e.format(e))

# 		========================

def setup(bot):
	bot.add_cog(moderation(bot))