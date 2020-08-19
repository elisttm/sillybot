import discord
from discord.ext import commands
import data.constants as tt

# 		========================

class fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	# 		========================

	@commands.command(aliases=['coglist'])
	async def cogs(self, ctx):
		cm_list, cm_num, = '', 0
		for cog, x in tt.loaded.items():
			if x == True: cm_list = f"{cm_list}'{cog}' : `Loaded`\n"; cm_num += 1
			if x == False: cm_list = f"{cm_list}'{cog}' : `Unloaded`\n"
		e_cm = discord.Embed(color=tt.clr['pink'])
		e_cm.add_field(name=f"cogs `[{cm_num}/{len(tt.cogs)}]`", value=cm_list)
		e_cm.set_author(name="cog manager", icon_url=tt.ico['cog'])
		await ctx.send(embed=e_cm)

	@commands.command()
	async def load(self, ctx, cog=None):
		await ctx.trigger_typing()
		if ctx.author.id != tt.owner_id: await ctx.send(tt.permdeny)
		else:
			if cog == None or cog not in tt.cogs: await ctx.send("⚠️ ⠀please specify a valid cog!")
			elif tt.loaded[cog] == True: await ctx.send(f"⚠️ ⠀'{cog}' is already loaded!")
			else:
				await ctx.trigger_typing()
				try:
					self.bot.load_extension('cogs.' + cog)
					tt.loaded[cog] = True
					await ctx.send(f"✅ ⠀loaded '{cog}'")
					tt.l = f"[{tt._t()}] COGMANAGER: loaded '{cog}'"
				except Exception as error:
					tt.loaded[cog] = False
					await ctx.send(f"❌ ⠀'{cog}' failed to load")
					tt.l = f"[{tt._t()}] COGMANAGER: '{cog}' failed to load [{error}]"
				await self.bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)

	@commands.command()
	async def unload(self, ctx, cog=None):
		await ctx.trigger_typing()
		if ctx.author.id != tt.owner_id: await ctx.send(tt.permdeny)
		else:
			if cog == None or cog not in tt.cogs: await ctx.send("⚠️ ⠀please specify a valid cog!")
			elif tt.loaded[cog] == False: await ctx.send(f"⚠️ ⠀'{cog}' is already unloaded!")
			else:
				await ctx.trigger_typing()
				try:
					self.bot.unload_extension('cogs.' + cog)
					tt.loaded[cog] = False
					await ctx.send(f"✅ ⠀unloaded '{cog}'")
					tt.l = f"[{tt._t()}] COGMANAGER: unloaded '{cog}'"
				except Exception as error:
					await ctx.send(f"❌ ⠀'{cog}' failed to unload")
					tt.l = f"[{tt._t()}] COGMANAGER: '{cog}' failed to unload [{error}]"
				await self.bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)

	@commands.command()
	async def unloadf(self, ctx, cog=None):
		await ctx.trigger_typing()
		if ctx.author.id != tt.owner_id: await ctx.send(tt.permdeny)
		else:
			if cog == None or cog not in tt.cogs: await ctx.send("⚠️ ⠀please specify a valid cog!")
			await ctx.trigger_typing()
			try:
				self.bot.unload_extension('cogs.' + cog)
				tt.loaded[cog] = False
				await ctx.send(f"✅ ⠀forcefully unloaded '{cog}'")
				tt.l = f"[{tt._t()}] COGMANAGER: forcefully unloaded '{cog}'"
			except Exception as error:
				tt.loaded[cog] = False
				await ctx.send(f"❌ ⠀'{cog}' failed to force unload")
				tt.l = f"[{tt._t()}] COGMANAGER: '{cog}' failed to force unload [{error}]"
			await self.bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)

	@commands.command()
	async def reload(self, ctx, cog=None):
		await ctx.trigger_typing()
		if ctx.author.id != tt.owner_id: await ctx.send(tt.permdeny)
		else:
			cog = 'all' if not cog else cog
			if cog == 'all' or cog in tt.cogs:
				if cog == 'all':
					cm_num, cm_msg = 0, ''
					tt.l = f"[{tt._t()}] COGMANAGER: reloading {len(tt.cogs)} cogs ..."
					for cog in tt.cogs:
						await ctx.trigger_typing()
						try:
							if tt.loaded[cog] == True: self.bot.unload_extension('cogs.' + cog); self.bot.load_extension('cogs.' + cog)
							if tt.loaded[cog] == False: self.bot.load_extension('cogs.' + cog)
							cm_num += 1; tt.loaded[cog] = True
							cm_msg = f"{cm_msg}✅ ⠀{cog}\n"; tt.l = f"{tt.l}\n   -- reloaded '{cog}'"
						except Exception as error:
							try: self.bot.load_extension('cogs.' + cog); cm_num += 1; tt.loaded[cog] = True
							except: tt.loaded[cog] = False
							cm_msg = f"{cm_msg}❌ ⠀{cog}\n"; tt.l = f"{tt.l}\n   -- '{cog}' failed to reload [{error}]"
					cm_msg = f"[`{cm_num}/{len(tt.cogs)}`] cogs reloaded]\n" + cm_msg
					tt.l = f"{tt.l}\n>[{cm_num}/{len(tt.cogs)}] cogs reloaded"
					await ctx.send(cm_msg)
				else:
					await ctx.trigger_typing()
					try:
						if tt.loaded[cog] == True: self.bot.unload_extension('cogs.' + cog); self.bot.load_extension('cogs.' + cog)
						else: self.bot.load_extension('cogs.' + cog); tt.loaded[cog] = True
						await ctx.send(f"✅ ⠀reloaded '{cog}'")
						tt.l = f"[{tt._t()}] COGMANAGER: reloaded '{cog}'"
					except Exception as error:
						await ctx.send(f"❌ ⠀'{cog}' failed to reload [{error}]")
						tt.l = f"[{tt._t()}] COGMANAGER: '{cog}' failed to reload [{error}]"
				await self.bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)
			else: 
				await ctx.send("⚠️ ⠀please specify a valid cog!")

# 		========================

def setup(bot):
	bot.add_cog(fun(bot))