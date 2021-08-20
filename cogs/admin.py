import discord, os, sys, json
from discord.ext import commands
from a import checks
from a.funcs import funcs
import a.constants as tt

class admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.load_db = funcs.load_db
		self.dump_db = funcs.dump_db
		self.send_log = funcs.send_log
		
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
			await self.send_log(self, f"presence set to '{presence}' by '{ctx.author}'")
			await ctx.message.add_reaction(tt.e['check'])
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@checks.is_admin()
	async def guilds(self, ctx):
		try:
			guilds_list = ''; guilds_num = 0
			for guild in self.bot.guilds: 
				guilds_num += 1
				guilds_list += f"{guilds_num}. {guild.id} {guild.name} {guild.owner}\n"
			await self.send_log(self, f"'{ctx.author}' called for the list of guilds ({guilds_num})\n{guilds_list}")
			await ctx.message.add_reaction(tt.e['check'])
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@commands.is_owner()
	async def leave(self, ctx):
		try:
			await self.send_log(self, f"trashbot left '{ctx.guild.name}'")
			await ctx.message.add_reaction(tt.e['check'])
			await ctx.guild.leave()
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@commands.is_owner()
	async def shutdown(self, ctx):
		try:
			await self.send_log(self, f"shutdown by '{ctx.author}'")
			await ctx.message.add_reaction(tt.e['check'])
			await self.bot.logout()
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))
	
	@commands.command()
	@checks.is_admin()
	async def restart(self, ctx):
		try:
			await self.send_log(self, f"restarted by '{ctx.author}'")
			await ctx.message.add_reaction(tt.e['check'])
			await os.execv(sys.executable, ['python'] + sys.argv)
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@checks.is_admin()
	async def blacklist(self, ctx, user: discord.User=None):
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
				await ctx.send(tt.x+"cannot blacklist bot admins!")
				return
			if user.id not in blacklist_list:
				blacklist_list.append(user.id)
				blacklist_msg = f"{user} added to blacklist"
			else:
				blacklist_list.remove(user.id)
				blacklist_msg = f"{user} removed from blacklist"
			self.dump_db(tt.blacklist_db, blacklist_list)
			await self.send_log(self, blacklist_msg)
			await ctx.send(tt.y+f"{blacklist_msg}")
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command(aliases=['coglist'])
	async def cogs(self, ctx):
		await ctx.trigger_typing()
		cm_list_loaded = ''; cm_list_unloaded = ''; cm_num = 0
		for cog, status in tt.loaded.items():
			if status == True: 
				cm_num += 1
				cm_list_loaded += f"{cog}\n"
			if status == False: 
				cm_list_unloaded += f"{cog}\n"
		e_cm = discord.Embed(color=tt.clr['pink'])
		e_cm.add_field(name=f"loaded cogs `[{cm_num}/{len(tt.cogs)}]`", value=cm_list_loaded)
		if cm_list_unloaded != '':
			e_cm.add_field(name=f"unloaded cogs", value=cm_list_unloaded)
		e_cm.set_author(name="cog manager", icon_url=tt.ico['cog'])
		await ctx.send(embed=e_cm)

	@commands.command()
	@checks.is_admin()
	async def load(self, ctx, cog:str):
		await ctx.trigger_typing()
		try:
			self.bot.load_extension('cogs.'+cog)
			tt.loaded[cog] = True
			cm_msg = f"loaded '{cog}'"
			await ctx.send(tt.y+f"{cm_msg}")
		except commands.ExtensionNotFound:
			await ctx.send(tt.x+f"'{cog}' is not a valid cog!")
			return
		except commands.ExtensionAlreadyLoaded:
			await ctx.send(tt.x+f"'{cog}' is already loaded!")
			return
		except Exception as error:
			cm_msg = f"'{cog}' failed to load [{error}]"
			await ctx.send(tt.x+f"{cm_msg}")
		await self.send_log(self, f"{cm_msg}")
			
	@commands.command()
	@checks.is_admin()
	async def unload(self, ctx, cog:str):
		await ctx.trigger_typing()
		try:
			self.bot.unload_extension('cogs.'+cog)
			tt.loaded[cog] = False
			cm_msg = f"unloaded '{cog}'"
			await ctx.send(tt.y+f"{cm_msg}")
			await self.send_log(self, f"{cm_msg}")
		except commands.ExtensionNotFound:
			await ctx.send(tt.x+f"'{cog}' is not a valid cog!")
			return
		except commands.ExtensionNotLoaded:
			await ctx.send(tt.x+f"'{cog}' is already unloaded!")
			return
		except Exception as error:
			cm_msg = f"'{cog}' failed to unload [{error}]"
			await ctx.send(tt.x+f"{cm_msg}")

	@commands.command()
	@checks.is_admin()
	async def reload(self, ctx, cog=None):
		await ctx.trigger_typing()
		if cog is None:
			cm_num = 0;  cm_log = ''; cm_msg = ''
			await self.send_log(self, f"reloading {len(tt.cogs)} cogs ...")
			for cog in tt.cogs:
				await ctx.trigger_typing()
				try:
					self.bot.reload_extension('cogs.'+cog)
					tt.loaded[cog] = True
					cm_num += 1
					cm_msg += tt.y+f"{cog}\n" 
					cm_log += f"    -- reloaded '{cog}'\n"
				except Exception as error:
					tt.loaded[cog] = False
					cm_msg += tt.x+f"{cog} [{error}]\n"
					cm_log += f"    <> '{cog}' failed to reload [{error}]\n"
			cm_rld = f"[{cm_num}/{len(tt.cogs)}] cogs reloaded!"
			await self.send_log(self, f"{cm_log}[{tt._t()}] {cm_rld}", show_prefix = False)
			await ctx.send(f"{cm_rld}\n{cm_msg}")
		elif cog in tt.cogs:
			try:
				self.bot.reload_extension('cogs.' + cog)
				tt.loaded[cog] = True
				cm_msg = f"reloaded '{cog}'"
				await ctx.send(tt.y+f"{cm_msg}")
			except Exception as error:
				cm_msg = f"'{cog}' failed to reload [{error}]"
				await ctx.send(tt.x+f"{cm_msg}")
			await self.send_log(self, f"{cm_msg}")
		else: 
			await ctx.send(tt.x+f"'{cog}' is not a valid cog!")

# 		========================

def setup(bot):
	bot.add_cog(admin(bot))
