import discord
from discord.ext import commands
from utils import checks
from utils.funcs import funcs
import data.constants as tt

# 		========================

class cogmanager(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.send_log = funcs.send_log
		self.log_prefix = "[ADMIN] "

	# 		========================

	@commands.command(aliases=['coglist'])
	async def cogs(self, ctx):
		cm_list_loaded = ''; cm_list_unloaded = ''; cm_num = 0
		for cog, status in tt.loaded.items():
			if status == True: 
				cm_num += 1
				cm_list_loaded += f"{cog}\n"
			if status == False: 
				cm_list_unloaded += f"{cog}\n"
		e_cm = discord.Embed(color=tt.clr['pink'])
		e_cm.add_field(name=f"loaded cogs `[{cm_num}/{len(tt.cogs)}]`", value=cm_list_loaded)
		e_cm.add_field(name=f"unloaded cogs", value=cm_list_unloaded)
		e_cm.set_author(name="cog manager", icon_url=tt.ico['cog'])
		await ctx.send(embed=e_cm)

	@commands.command(aliases=['l'])
	@checks.is_admin()
	async def load(self, ctx, cog:str):
		await ctx.trigger_typing()
		if cog not in tt.cogs: 
			await ctx.send("⚠️ ⠀please specify a valid cog!")
			return
		try:
			self.bot.load_extension('cogs.' + cog)
			tt.loaded[cog] = True
			cm_msg = f"loaded '{cog}'"
			await ctx.send(f"✅ ⠀{cm_msg}")
		except Exception as error:
			cm_msg = f"'{cog}' failed to load [{error}]"
			await ctx.send(f"❌ ⠀{cm_msg}")
		await self.send_log(self, log = f"{cm_msg}", prefix = self.log_prefix)
			
	@commands.command(aliases=['u', 'ul'])
	@checks.is_admin()
	async def unload(self, ctx, cog:str):
		await ctx.trigger_typing()
		if cog not in tt.cogs:
			await ctx.send("⚠️ ⠀please specify a valid cog!")
			return 
		try:
			self.bot.unload_extension('cogs.' + cog)
			tt.loaded[cog] = False
			cm_msg = f"unloaded '{cog}'"
			await ctx.send(f"✅ ⠀{cm_msg}")
		except Exception as error:
			cm_msg = f"'{cog}' failed to unload [{error}]"
			await ctx.send(f"❌ ⠀{cm_msg}")
		await self.send_log(self, log = f"{cm_msg}", prefix = self.log_prefix)

	@commands.command(aliases=['rl'])
	@checks.is_admin()
	async def reload(self, ctx, cog=None):
		await ctx.trigger_typing()
		if cog is None:
			cm_num = 0;  cm_log = ''; cm_msg = ''
			await self.send_log(self, log = f"reloading {len(tt.cogs)} cogs ...", prefix = self.log_prefix)
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
						cm_log += f"    == '{cog}' failed to reload [{error}]\n"
			cm_rld = f"[{cm_num}/{len(tt.cogs)}] cogs reloaded!"
			await self.send_log(self, log = f"{cm_log}[{tt._t()}] {cm_rld}", show_prefix = False)
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
			except Exception as error:
				cm_msg = f"'{cog}' failed to reload [{error}]"
				await ctx.send(f"❌ ⠀{cm_msg}")
			await self.send_log(self, log = f"{cm_msg}", prefix = self.log_prefix)
		else: 
			await ctx.send("⚠️ ⠀please specify a valid cog!")

# 		========================

def setup(bot):
	bot.add_cog(cogmanager(bot))