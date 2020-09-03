import discord
import sys, os
import pickle
from discord.ext import commands
from utils import checks
from utils.funcs import funcs
import data.constants as tt

# 		========================

class admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
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
			e_adm.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url_as(format='png'))
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
			await self.send_log(self, log = f"presence set to '{presence}' by '{ctx.author}'", prefix = self.log_prefix)
			await ctx.send(f"✅ ⠀presence set to '{presence}''")
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
			await self.send_log(self, log = f"'{ctx.author}' called for the list of guilds ({guilds_num})\n{guilds_list}", prefix = self.log_prefix)
			await ctx.message.add_reaction('✅')
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@checks.is_admin()
	async def echo(self, ctx, echo_channel:int, *, message:str):
		try:
			message = tt.sanitize(message)
			await self.bot.get_channel(int(echo_channel)).send(message)
			await self.send_log(self, log = f"'{ctx.author}' in '{ctx.guild.name}' echoed '{message}' to channel ID '{echo_channel}'", prefix = self.log_prefix)
			await ctx.message.add_reaction('✅')
		except Exception as e: 
			await ctx.send(tt.msg_e.format(e))

	@commands.command()
	@commands.is_owner()
	async def leave(self, ctx):
		try:
			await self.send_log(self, log = f"trashbot left '{ctx.guild.name}'", prefix = self.log_prefix)
			await ctx.message.add_reaction('✅')
			await ctx.guild.leave()
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@commands.is_owner()
	async def shutdown(self, ctx):
		try:
			await self.send_log(self, log = f"shutdown by '{ctx.author}'", prefix = self.log_prefix)
			await ctx.message.add_reaction('✅')
			await self.bot.logout()
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))
	
	@commands.command()
	@checks.is_admin()
	async def restart(self, ctx):
		try:
			await self.send_log(self, log = f"restarted by '{ctx.author}'", prefix = self.log_prefix)
			await ctx.message.add_reaction('✅')
			await os.execv(sys.executable, ['python'] + sys.argv)
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	# this needs to be optimized
	@commands.command()
	@checks.is_admin()
	async def blacklist(self, ctx, arg1=None, user: discord.User = None):
		try:
			blacklist = pickle.load(open(tt.blacklist_pkl, "rb"))
			if arg1 == None:
				if user == None:
					blacklist_list = ''
					for x in blacklist:
						user = self.bot.get_user(x)
						blacklist_list += f"- {user} ({user.id})\n"
					await ctx.send(f"```list of blacklisted users ({len(blacklist)}):\n{blacklist_list}```")
			elif arg1 == 'add':
				if user == None:
					await ctx.send("⚠️ ⠀please provide a user ID or mention!")
				else:
					if user.id not in blacklist:
						blacklist.append(user.id)
						pickle.dump(blacklist, open(tt.blacklist_pkl, "wb"))
						await ctx.send("✅ ⠀user added to blacklist")
					else:
						await ctx.send("❌ ⠀user is already blacklisted!")
			elif arg1 == 'remove':
				if user == None:
					await ctx.send("⚠️ ⠀please provide a user ID or mention!")
				else:
					if user.id in blacklist:
						blacklist.remove(user.id)
						pickle.dump(blacklist, open(tt.blacklist_pkl, "wb"))
						await ctx.send("✅ ⠀user removed from blacklist")
					else:
						await ctx.send("❌ ⠀user is not blacklisted!")
			else:
				await ctx.send("invalid subcommand")
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

#pickle.dump(blacklist, open(tt.blacklist_pkl, "wb"))

# 		========================

def setup(bot):
	bot.add_cog(admin(bot))