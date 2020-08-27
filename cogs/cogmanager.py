import discord
from discord.ext import commands
import data.constants as tt

# 		========================

class cogmanager(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	async def is_admin(ctx):
		return ctx.author.id in tt.admins
		
	async def send_log(self, log:str, prefix = True):
		if prefix == True: 
			log_msg = f"[{tt._t()}] [COGMANAGER] {log}"
		else: 
			log_msg = log
		print(log_msg)
		await self.bot.get_channel(tt.logs).send(f"```{log_msg}```")

	# 		========================

	@commands.command(aliases=['coglist'])
	async def cogs(self, ctx):
		cm_list = ''; cm_num = 0
		for cog, status in tt.loaded.items():
			if status == True: 
				cm_list = f"{cm_list}'{cog}' : `Loaded`\n"; cm_num += 1
			if status == False: 
				cm_list = f"{cm_list}'{cog}' : `Unloaded`\n"
		e_cm = discord.Embed(color=tt.clr['pink'])
		e_cm.add_field(name=f"cogs `[{cm_num}/{len(tt.cogs)}]`", value=cm_list)
		e_cm.set_author(name="cog manager", icon_url=tt.ico['cog'])
		await ctx.send(embed=e_cm)

	@commands.command(aliases=['l'])
	@commands.check(is_admin)
	async def load(self, ctx, cog:str):
		await ctx.trigger_typing()
		if cog in tt.cogs: 
			await ctx.trigger_typing()
			try:
				self.bot.load_extension('cogs.' + cog)
				tt.loaded[cog] = True
				cm_msg = f"loaded '{cog}'"
				await ctx.send(f"✅ ⠀{cm_msg}")
			except Exception as error:
				cm_msg = f"'{cog}' failed to load [{error}]"
				await ctx.send(f"❌ ⠀{cm_msg}")
			await self.send_log(log = f"{cm_msg}")
		else:
			await ctx.send("⚠️ ⠀please specify a valid cog!")

	@commands.command(aliases=['u', 'ul'])
	@commands.check(is_admin)
	async def unload(self, ctx, cog:str):
		await ctx.trigger_typing()
		if cog in tt.cogs: 
			try:
				self.bot.unload_extension('cogs.' + cog)
				tt.loaded[cog] = False
				cm_msg = f"unloaded '{cog}'"
				await ctx.send(f"✅ ⠀{cm_msg}")
			except Exception as error:
				cm_msg = f"'{cog}' failed to unload [{error}]"
				await ctx.send(f"❌ ⠀{cm_msg}")
			await self.send_log(log = f"({ctx.author}) {cm_msg}")
		else:
			await ctx.send("⚠️ ⠀please specify a valid cog!")

	@commands.command(aliases=['rl'])
	@commands.check(is_admin)
	async def reload(self, ctx, cog=None):
		await ctx.trigger_typing()
		if cog is None:
			cm_num = 0;  cm_log = ''; cm_msg = ''
			await self.send_log(log = f"reloading {len(tt.cogs)} cogs ...")
			for cog in tt.cogs:
				await ctx.trigger_typing()
				try:
					self.bot.unload_extension('cogs.' + cog)
					self.bot.load_extension('cogs.' + cog)
					tt.loaded[cog] = True
					cm_num += 1
					cm_msg += f"✅ ⠀{cog}\n" 
					cm_log += f"    -- reloaded '{cog}'\n"
				except:
					try: 
						self.bot.load_extension('cogs.' + cog)
						tt.loaded[cog] = True
						cm_num += 1
						cm_msg += f"✅ ⠀{cog}\n" 
						cm_log += f"    -- reloaded '{cog}'\n"
					except Exception as error: 
						tt.loaded[cog] = False
						cm_msg += f"❌ ⠀{cog} [{error}]\n"
						cm_log = f"    == '{cog}' failed to reload [{error}]\n"
			cm_rld = f"[{cm_num}/{len(tt.cogs)}] cogs reloaded!"
			await self.send_log(f"{cm_log}[{tt._t()}] {cm_rld}", prefix = False)
			await ctx.send(f"{cm_rld}\n{cm_msg}")
		elif cog in tt.cogs:
			try:
				if tt.loaded[cog] == True: 
					self.bot.unload_extension('cogs.' + cog)
					self.bot.load_extension('cogs.' + cog)
				else: 
					self.bot.load_extension('cogs.' + cog)
					tt.loaded[cog] = True
				cm_msg = f"reloaded '{cog}'"
				await ctx.send(f"✅ ⠀{cm_msg}")
				await self.send_log(log = f"{cm_msg}")
			except Exception as error:
				cm_msg = f"'{cog}' failed to reload [{error}]"
				await ctx.send(f"❌ ⠀{cm_msg}")
				await self.send_log(log = f"{cm_msg}")
		else: 
			await ctx.send("⚠️ ⠀please specify a valid cog!")

# 		========================

def setup(bot):
	bot.add_cog(cogmanager(bot))