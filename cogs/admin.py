import discord
import os, sys
import json
from discord.ext import commands
from utils import checks
from utils.funcs import funcs
import data.constants as tt

# 		========================

class admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.load_db = funcs.load_db
		self.dump_db = funcs.dump_db
		self.send_log = funcs.send_log
		self.log_prefix = "[ADMIN] "
		
# 		========================
	
	@commands.command()
	async def admins(self, ctx):
		await ctx.trigger_typing() 
		try:
			admin_list = ''; admin_num = 0
			for admin in tt.admins:
				user = self.bot.get_user(admin)
				admin_num += 1
				admin_list += f"{user} ({user.id})\n"; 
			e_adm = discord.Embed(color=tt.clr['pink'])
			e_adm.add_field(name=f"admins [{admin_num}]", value=admin_list)
			e_adm.set_author(name="list of trashbot's admins", icon_url=tt.ico['info'])
			await ctx.send(embed=e_adm)
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@checks.is_admin()
	async def presence(self, ctx, *, presence = None):
		await ctx.trigger_typing()
		try:
			if presence is None:
				presence = tt.presence
			await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(presence))
			await self.send_log(self, f"presence set to '{presence}' by '{ctx.author}'", self.log_prefix)
			await ctx.message.add_reaction('✅')
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@checks.is_admin()
	async def guilds(self, ctx):
		try:
			guilds_list = ''; guilds_num = 0
			for guild in self.bot.guilds: 
				guilds_num += 1
				guilds_list += f"  {guilds_num}. {guild.name} ({guild.owner}) [{guild.id}]\n"
			await self.send_log(self, f"'{ctx.author}' called for the list of guilds ({guilds_num})\n{guilds_list}", self.log_prefix)
			await ctx.message.add_reaction('✅')
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@commands.is_owner()
	async def leave(self, ctx):
		try:
			await self.send_log(self, f"trashbot left '{ctx.guild.name}'", self.log_prefix)
			await ctx.message.add_reaction('✅')
			await ctx.guild.leave()
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@commands.is_owner()
	async def shutdown(self, ctx):
		try:
			await self.send_log(self, f"shutdown by '{ctx.author}'", self.log_prefix)
			await ctx.message.add_reaction('✅')
			await self.bot.logout()
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))
	
	@commands.command()
	@checks.is_admin()
	async def restart(self, ctx):
		try:
			await self.send_log(self, f"restarted by '{ctx.author}'", self.log_prefix)
			await ctx.message.add_reaction('✅')
			await os.execv(sys.executable, ['python'] + sys.argv)
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@checks.is_admin()
	async def blacklist(self, ctx, user: discord.User = None):
		try:
			bl_user_list = ''
			blacklist_list = self.load_db(tt.blacklist_db)
			if user is None:
				for bl_user_id in blacklist_list:
					bl_user = self.bot.get_user(bl_user_id)
					bl_user_list += f"  - {bl_user} ({bl_user.id})\n"
				await ctx.send(f"```blacklisted users [{len(blacklist_list)}]:\n{bl_user_list}```")
				return
			if user.id in tt.admins:
				await ctx.send("❌ ⠀cannot blacklist bot admins!")
				return
			if user.id not in blacklist_list:
				blacklist_list.append(user.id)
				blacklist_msg = f"{user} added to blacklist"
			else:
				blacklist_list.remove(user.id)
				blacklist_msg = f"{user} removed from blacklist"
			self.dump_db(tt.blacklist_db, blacklist_list)
			await self.send_log(self, blacklist_msg, self.log_prefix)
			await ctx.send(f"✅ ⠀{blacklist_msg}")
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

# 		========================

def setup(bot):
	bot.add_cog(admin(bot))