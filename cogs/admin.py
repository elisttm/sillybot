import discord, os, sys
from discord.ext import commands
from a import checks
from a.funcs import f
import a.constants as tt

class admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@checks.is_bot_admin()
	async def restart(self, ctx):
		f.log(f"restarted by {ctx.author}")
		await ctx.message.add_reaction(tt.e.check)
		await os.execv(sys.executable,['python']+sys.argv)

	@commands.command()
	@commands.is_owner()
	async def leave(self, ctx):
		f.log(f"{ctx.guild.author} removed from '{ctx.guild.name}'")
		await ctx.message.add_reaction(tt.e.check)
		await ctx.guild.leave()

	@commands.command()
	async def admins(self, ctx):
		await ctx.trigger_typing() 
		e_adm = discord.Embed(color=tt.dcolor)
		e_adm.add_field(name=f"bot admins", value='\n'.join([str(self.bot.get_user(admin)) for admin in tt.admins]))
		e_adm.set_author(name="list of bot admins", icon_url=tt.icon.info)
		await ctx.send(embed=e_adm)

	@commands.command()
	@checks.is_bot_admin()
	async def presence(self, ctx, *, presence:str):
		x = tt.presence.default
		for y, z in enumerate(presence.split(';')):
			x[y] = z
		if x[1] not in tt.presence.status or x[2] not in tt.presence.activity:
			await ctx.send(tt.x+f"invalid format! (text;{'/'.join(tt.presence.status)};{'/'.join(tt.presence.activity)})")
			return
		await self.bot.change_presence(status=tt.presence.status[x[1]], activity=discord.Activity(type=tt.presence.activity[x[2]],name=x[0]))
		f.log(f"{ctx.author} set presence to {x[1]}, {x[2]} '{x[0]}'")
		await ctx.message.add_reaction(tt.e.check)

	@commands.command()
	@checks.is_bot_admin()
	async def guilds(self, ctx):
		for num, guild in enumerate(self.bot.guilds, 1): 
			print(f"{num}. [{guild.id}] {guild.name}")
		await ctx.message.add_reaction(tt.e.check)

	@commands.command()
	@checks.is_bot_admin()
	async def blacklist(self, ctx, user:discord.User=None):
		if user == None:
			_list = ''
			for id in tt.blacklist:
				_user = self.bot.get_user(id)
				_list += f"  - {_user} ({_user.id})\n"
			await ctx.send(f"```blacklisted users:\n{_list}```")
		elif user.id in tt.admins:
			await ctx.send(tt.x+"bot admins cannot be blacklisted!")
			return
		elif user.id not in tt.blacklist:
			tt.blacklist.append(user.id)
			f._list(tt.misc, 'misc', 'blacklist', [user.id], 'add')
			msg = f"blacklisted {user}"
		else:
			tt.blacklist.remove(user.id)
			f._list(tt.misc, 'misc', 'blacklist', [user.id], 'remove')
			msg = f"unblacklisted {user}"
		f.log(f"{ctx.author} {msg}")
		await ctx.send(tt.y+msg+'!')

	@commands.command(aliases=['tg'])
	@checks.is_bot_admin()
	async def toggle(self, ctx, *, x=None):
		if x == None:
			toggles = f.data(tt.misc, 'misc', 'disabled')['disabled']
			await ctx.send(f"```disabled commands:\n{tt.n.join(toggles) if len(toggles) > 0 else 'n/a'}\n\ndisabled cogs:\n{tt.n.join([cog for cog in tt.cogs if cog not in tt.loaded]) if sorted(tt.cogs) != sorted(tt.loaded) else 'n/a'}```")
			return
		if x in tt.cogs:
			try:
				await self.bot.load_extension('cogs.'+x)
				await ctx.message.add_reaction(tt.e.check)
				tt.loaded.append(x)
				f.log('loaded '+x)
			except commands.ExtensionAlreadyLoaded:
				await self.bot.unload_extension('cogs.'+x)
				await ctx.message.add_reaction(tt.e.check)
				tt.loaded.remove(x)
				f.log('unloaded '+x)
			except Exception as error:
				raise(error)
			return
		else:
			command = self.bot.get_command(x)
			if not command or ctx.command == command:
				await ctx.send(tt.x+f"invalid command or cog provided!")
				return
			command.enabled = not command.enabled
			f._list(tt.misc, 'misc', 'disabled', [command.qualified_name], 'add' if not command.enabled else 'remove')
			await ctx.message.add_reaction(tt.e.check)

	@commands.command()
	@checks.is_bot_admin()
	async def reload(self, ctx, cog):
		if cog not in tt.cogs:
			await ctx.send(tt.x+f"{cog} is not a valid cog!")
			return
		if cog in tt.loaded:
			tt.loaded.remove(cog)
		await self.bot.reload_extension('cogs.'+cog)
		if cog not in tt.loaded: 
			tt.loaded.append(cog)
		await ctx.message.add_reaction(tt.e.check)
		f.log('reloaded '+cog)

async def setup(bot):
	await bot.add_cog(admin(bot))
