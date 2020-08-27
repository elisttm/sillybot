import discord
import sys, os
import pickle
from discord.ext import commands
import data.constants as tt

# 		========================

class admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def is_admin(ctx):
		return ctx.author.id in tt.admins

	async def send_log(self, log:str):
		log_msg = f"[{tt._t()}] [ADMIN] {log}"
		print(log_msg)
		await self.bot.get_channel(tt.logs).send(f"```{log_msg}```")
		
# 		========================
	
	@commands.command()
	async def admins(self, ctx): 
		try:
			await ctx.trigger_typing()
			admin_list = ''; admin_num = 0
			for user_id in tt.admins:
				user = self.bot.get_user(user_id)
				admin_num += 1
				admin_list += f"{user} ({user.id})\n"; 
			e_adm = discord.Embed(color=tt.clr['pink'])
			e_adm.add_field(name=f"admins `[{admin_num}]`", value=admin_list)
			e_adm.set_author(name="admin list", icon_url=tt.ico['info'])
			e_adm.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url_as(format='png'))
			await ctx.send(embed=e_adm)
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@commands.check(is_admin)
	async def presence(self, ctx, *, presence=None):
		try:
			await ctx.trigger_typing()
			if presence is None:
				presence = discord.Game(tt.presence)
				await self.bot.change_presence(status=discord.Status.online, activity=presence)
				await self.send_log(log = f"presence reset by '{ctx.author}'")
				await ctx.send('✅ ⠀presence reset to default.')	
			else:
				#presence = presence.replace("{version}", f"{tt.v}")
				presence = discord.Game(presence)
				await self.bot.change_presence(status=discord.Status.online, activity=presence)
				await self.send_log(log = f"presence set to '{presence}' by '{ctx.author}'")
				await ctx.send(f'✅ ⠀presence set to `{presence}`.')
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@commands.check(is_admin)
	async def guilds(self, ctx):
		try:
			await ctx.trigger_typing()
			guildlist = ''; guildnum = 0
			for guild in self.bot.guilds: 
				guildnum += 1
				guildlist += f"  {guildnum}. {guild.name} ({guild.owner}) [{guild.id}]\n"
			await self.send_log(log = f"'{ctx.author}' called for the list of guilds ({guildnum})\n{guildlist}")
			await ctx.send("✅ ⠀guild list sent to logs!")
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@commands.check(is_admin)
	async def echo(self, ctx, channel:discord.TextChannel, *, message:str):
		try:
			message = tt.sanitize(message)
			await self.send_log(log = f"'{ctx.author}' in '{ctx.guild.name}' said '{message}'")
			await ctx.send(message)
		except Exception as e: 
			await ctx.send(tt.msg_e.format(e))

	@commands.command()
	@commands.is_owner()
	async def leave(self, ctx):
		try:
			await ctx.message.add_reaction('✅')
			await self.send_log(log = f"'{ctx.author}' used leave in '{ctx.guild.name}'")
			await ctx.guild.leave()
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@commands.is_owner()
	async def shutdown(self, ctx):
		await self.send_log(log = f"shutdown by '{ctx.author}'")
		await ctx.message.add_reaction('✅')
		await self.bot.logout()
	
	@commands.command()
	@commands.check(is_admin)
	async def restart(self, ctx):
		try:
			await self.send_log(log = f"restarted by '{ctx.author}'")
			await ctx.message.add_reaction('✅')
			await os.execv(sys.executable, ['python'] + sys.argv)
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@commands.check(is_admin)
	async def blacklist(self, ctx, arg1=None, user: discord.Member = None):
		try:
			blacklist = pickle.load(open(tt.blacklist_pkl, "rb"))
			if arg1 == None:
				if user == None:
					blacklist_list = ''
					for x in blacklist:
						user = self.bot.get_user(x)
						blacklist_list = blacklist_list + f"- {user} ({user.id})\n"
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