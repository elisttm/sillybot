import discord
import pickle
import traceback
import sys
from discord.ext import commands
import data.constants as tt
from data.commands import help_list; cmd = help_list()

# 		========================

class help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

# 		========================

	@commands.command()
	async def help(self, ctx, *, tag=None):
		await ctx.trigger_typing()
		try: 
			custom_prefixes = pickle.load(open(tt.prefixes_pkl, "rb"))
			cmds = '\u200b'
			if tag == None:
				if ctx.message.guild.id in custom_prefixes: 
					desc_prefix = f"'{custom_prefixes[ctx.message.guild.id]}' (custom)"
				else: 
					desc_prefix = f"'{tt.p}'"
				e_h = discord.Embed(title=f"trashbot [v{tt.v}]", description=f"command prefix: {desc_prefix}", color=tt.clr['pink'])
				for cog in cmd.commands:
					if cog == 'general' or tt.loaded[cog] == True: 
						cmds = '\u200b'
						for c_ctg, c_cmd in cmd.commands.items():
							if c_ctg == cog:
								for x, y in c_cmd.items(): cmds = f"{cmds}**{x}** - {y}\n"
						e_h.add_field(name=f"⠀{cog}", value=cmds, inline=False)
				e_h.set_author(name="help menu", icon_url=tt.ico['info'])
				await ctx.send(embed=e_h)
			if tag in cmd.commands: 
				cmds = '\u200b'
				for c_ctg, c_cmdlist in cmd.commands.items():
					if c_ctg == tag:
						for x, y in c_cmdlist.items(): cmds = f"{cmds}**{x}** - {y}\n"
						ctg_loaded = '\u200b' if tag == 'general' or tt.loaded[tag] == True else '`[not loaded]`' 
						e_h = discord.Embed(title=f"**{c_ctg}** {ctg_loaded}", description=cmd.categories[tag], color=tt.clr['pink'])
						e_h.set_author(name=f"help menu :: {c_ctg}", icon_url=tt.ico['info'])
						e_h.add_field(name="⠀commands", value=cmds)
						await ctx.send(embed=e_h)
			elif tag != None and tag not in cmd.commands: await ctx.send('⚠️ ⠀unknown command category!')
		except Exception as e: await ctx.send(tt.msg_e.format(e))

# 		========================

def setup(bot):
	bot.add_cog(help(bot))