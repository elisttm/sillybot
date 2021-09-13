import discord, os, sys
from discord.ext import commands
from a import checks
from a.funcs import f
import a.constants as tt

class admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.load_db = f.load_json
		self.dump_db = f.dump_json
		
# 		========================
	
	@commands.command()
	async def test(self, ctx, text=None):
		#print(text)
		#await ctx.message.add_reaction(tt.e.check)
		return
	
	@commands.command()
	async def admins(self, ctx):
		await ctx.trigger_typing() 
		admin_list = ''; admin_num = 0
		for admin in tt.admins:
			user = self.bot.get_user(admin)
			admin_num += 1
			admin_list += f"{user} ({user.id})\n"; 
		e_adm = discord.Embed(color=tt.color.pink)
		e_adm.add_field(name=f"admins [{admin_num}]", value=admin_list)
		e_adm.set_author(name="list of trashbot's admins", icon_url=tt.icon.info)
		await ctx.send(embed=e_adm)

	@commands.command()
	@checks.is_admin()
	async def presence(self, ctx, *, presence:str):
		a = {'playing':discord.ActivityType.playing, 'listening':discord.ActivityType.listening, 'online':discord.Status.online, 'idle':discord.Status.idle, 'dnd':discord.Status.dnd, 'invis':discord.Status.invisible,}
		_presence = presence.split(';')
		x = [tt.p+'help','online', 'playing']
		y = 0
		for z in _presence:
			x[y] = z
			y += 1
		await self.bot.change_presence(status=a[x[1]], activity=discord.Activity(type=a[x[2]],name=x[0]))
		f.log(f"{ctx.author} set presence to {x[1]} {x[2]} '{x[0]}'")
		await ctx.message.add_reaction(tt.e.check)

	@commands.command()
	@checks.is_admin()
	async def guilds(self, ctx):
		guilds_list = ''; guilds_num = 0
		for guild in self.bot.guilds: 
			guilds_num += 1
			guilds_list += f"{guilds_num}. {guild.id} - {guild.name} - {guild.owner}\n"
		print(f"'list of guilds ({guilds_num})\n{guilds_list}")
		await ctx.message.add_reaction(tt.e.check)

	@commands.command()
	@commands.is_owner()
	async def leave(self, ctx):
		f.log(f"{ctx.guild.author} removed trashbot from '{ctx.guild.name}'")
		await ctx.message.add_reaction(tt.e.check)
		await ctx.guild.leave()

	@commands.command()
	@commands.is_owner()
	async def shutdown(self, ctx):
		f.log(f"shutdown by {ctx.author}")
		await ctx.message.add_reaction(tt.e.check)
		await self.bot.logout()
	
	@commands.command()
	@checks.is_admin()
	async def restart(self, ctx):
		f.log(f"restarted by {ctx.author}")
		await ctx.message.add_reaction(tt.e.check)
		await os.execv(sys.executable,['python']+sys.argv)

	@commands.command()
	@checks.is_admin()
	async def blacklist(self, ctx, user: discord.User=None):
		_list = ''; _count = 0
		tt.blacklist_list = f.data(tt.yeah, 'misc', 'blacklist')['blacklist']
		if user is None:
			for id in tt.blacklist_list:
				_count += 1; _list += f"  - {self.bot.get_user(id)} ({self.bot.get_user(id).id})\n"
			await ctx.send(f"```blacklisted users [{_count}]:\n{_list}```")
			return
		if user.id in tt.admins:
			await ctx.send(tt.x+"bot admins cannot be blacklisted!")
			return
		if user.id not in tt.blacklist_list:
			tt.blacklist_list.append(user.id)
			f.data_update(tt.yeah, 'misc', 'blacklist', [user.id], 'append')
			msg = [f"{user} has been blacklisted!",f"{ctx.author} blacklisted {user}"]
		else:
			tt.blacklist_list.remove(user.id)
			f.data_update(tt.yeah, 'misc', 'blacklist', [user.id], 'remove')
			msg = [f"{user} has been removed from the blacklist!",f"{ctx.author} unblacklisted {user}"]
		f.log(msg[1])
		await ctx.send(tt.y+msg[0])

	@commands.command(aliases=['coglist'])
	async def cogs(self, ctx):
		await ctx.trigger_typing()
		cm_list_loaded = ''; cm_list_unloaded = ''
		for cog in tt.cogs:
			if cog in tt.loaded:
				cm_list_loaded += f"{cog}\n"
			else:
				cm_list_unloaded += f"{cog}\n"
		e_cm = discord.Embed(color=tt.color.pink)
		e_cm.add_field(name=f"loaded cogs", value=cm_list_loaded)
		if cm_list_unloaded != '':
			e_cm.add_field(name=f"unloaded cogs", value=cm_list_unloaded)
		e_cm.set_author(name="cog manager", icon_url=tt.icon.cog)
		await ctx.send(embed=e_cm)

	@commands.command()
	@checks.is_admin()
	async def load(self, ctx, cog:str):
		try:
			self.bot.load_extension('cogs.'+cog)
			tt.loaded.append(cog)
			cm_msg = f"loaded '{cog}'"
			await ctx.message.add_reaction(tt.e.check)
		except commands.ExtensionNotFound:
			await ctx.send(tt.w+f"'{cog}' is not a valid cog!")
			return
		except commands.ExtensionAlreadyLoaded:
			await ctx.send(tt.x+f"'{cog}' is already loaded!")
			return
		except Exception as error:
			cm_msg = f"'{cog}' failed to load [{error}]"
			await ctx.send(tt.x+f"{cm_msg}")
		f.log(f"{cm_msg}")
			
	@commands.command()
	@checks.is_admin()
	async def unload(self, ctx, cog:str):
		try:
			self.bot.unload_extension('cogs.'+cog)
			tt.loaded.remove(cog)
			cm_msg = f"unloaded '{cog}'"
			await ctx.message.add_reaction(tt.e.check)
		except commands.ExtensionNotFound:
			await ctx.send(tt.w+f"'{cog}' is not a valid cog!")
			return
		except commands.ExtensionNotLoaded:
			await ctx.send(tt.x+f"'{cog}' is already unloaded!")
			return
		except Exception as error:
			cm_msg = f"'{cog}' failed to unload [{error}]"
			await ctx.send(tt.x+f"{cm_msg}")
		f.log(f"{cm_msg}")

	@commands.command()
	@checks.is_admin()
	async def reload(self, ctx, cog=None):
		if cog in tt.cogs:
			try:
				self.bot.reload_extension('cogs.' + cog)
				if cog not in tt.loaded: tt.loaded.append(cog)
				cm_msg = f"reloaded '{cog}'"
				await ctx.message.add_reaction(tt.e.check)
			except Exception as error:
				if cog in tt.loaded: tt.loaded.remove(cog)
				cm_msg = f"'{cog}' failed to reload [{error}]"
				await ctx.send(tt.x+f"{cm_msg}")
			f.log(f"{cm_msg}")
		else: 
			await ctx.send(tt.x+f"'{cog}' is not a valid cog!")

# 		========================

def setup(bot):
	bot.add_cog(admin(bot))
