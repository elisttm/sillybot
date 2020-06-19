# -- add modules for roles
# -- create a database system to store information (sqlite3)

# |[ trashbot | by elisttm ]|

import discord
import sys, os
from discord.ext import commands
import keep_alive as keep_alive
import data.constants as tt
import data.commands as cmd

# 		========================

bot = commands.Bot(
	command_prefix = commands.when_mentioned_or(tt.p), 
	case_insensitive = True
)
bot.remove_command('help')
ctx = commands.Context

# 		========================
	
sl_st = f'[{tt._t()}] starting trashbot ...\n'
print(f"\n{sl_st}")

if __name__ == '__main__':
	scm_num = 0
	print(f"[{tt._t()}] COGMANAGER: loading {len(tt.cogs)} cogs ...")
	for cog in tt.cogs:
		try: 
			bot.load_extension('cogs.' + cog)
			tt.loaded[cog] = True; scm_num += 1
			print(f"   -- loaded '{cog}'")
		except Exception as e:
			tt.loaded[cog] = False
			print(f"   -- unable to load '{cog}' [{e}]")
	scm_fin = f">> [{scm_num}/{len(tt.cogs)} cogs loaded]\n"; print(scm_fin)

@bot.event
async def on_connect():
	sl_pre = f"[{tt._t()}] preparing client ..."; print(sl_pre)

	@bot.event
	async def on_ready():
		sl_on = f"[{tt._t()}] trashbot is online!"; print(sl_on)
		await bot.change_presence(status=discord.Status.online, activity=tt.presence)
		print(f"\n  ___/-\___    Online | v{tt.v}\n |---------|   {bot.user.name}#{bot.user.discriminator} ({bot.user.id})\n  | | | | |  _                 _     _           _   \n  | | | | | | |_ _ __ __ _ ___| |__ | |__   ___ | |_ \n  | | | | | | __| '__/ _` / __| '_ \| '_ \ / _ \| __|\n  | | | | | | |_| | | (_| \__ \ | | | |_) | (_) | |_ \n  |_______|  \__|_|  \__,_|___/_| |_|_.__/ \___/ \__|\n")	
		tt.l = f"{sl_st}{scm_fin}\n{sl_pre}\n{sl_on} (v{tt.v})"; await bot.get_channel(tt.logs).send(f"```{tt.l}```")



# 		========================

@bot.command()
async def help(ctx, *, tag=None):
	await ctx.trigger_typing()
	try:
		cmds = ''
		if tag == None:
			e_h = discord.Embed(title=f"trashbot [v{tt.v}]", description=f"for more information, use the *'about'* command", color=tt.clr['pink'])
			for cog in tt.cogs0:
				if cog == 'general' or tt.loaded[cog] == True:
					cmds = ''
					for c_ctg, c_cmd in cmd.commands.items():
						if c_ctg == cog:
							for x, y in c_cmd.items(): cmds = f"{cmds}**{x}** - {y}\n"
					e_h.add_field(name=f"⠀__{cog}__", value=cmds, inline=False)
			e_h.set_author(name="help menu", icon_url=tt.ico['info'])
			await ctx.send(embed=e_h)
		if tag in tt.cogs:
			cmds = ''
			for c_ctg, c_cmdlist in cmd.commands.items():
				if c_ctg == tag:
					for x, y in c_cmdlist.items(): cmds = f"{cmds}**{x}** - {y}\n"
					ctg_loaded = '' if tag == 'general' or tt.loaded[tag] == True else '`[not loaded]`' 
					e_h = discord.Embed(title=f"**{c_ctg}** {ctg_loaded}", description=cmd.categories[tag], color=tt.clr['pink'])
					e_h.set_author(name=f"help menu :: {c_ctg}", icon_url=tt.ico['info'])
					e_h.add_field(name="⠀__commands__", value=cmds)
					await ctx.send(embed=e_h)
		elif tag != None and tag not in tt.cogs0: await ctx.send('> ⚠️ ⠀unknown command category!')
	except Exception as e: await ctx.send(tt.msg_e.format(e))

# 		========================

@bot.event
async def on_message(message):
  if message.author.bot:
    pass
  elif "doing stuff" in message.content:
    await ctx.send(message.channel, 'im stuff')
  else:
    if 'y/n' in message.content.lower():
      await message.add_reaction('👍')
      await message.add_reaction('👎')
    if 'yes or no' in message.content.lower():
      await message.add_reaction('👍')
      await message.add_reaction('👎')
  await bot.process_commands(message)

@bot.event
async def on_guild_remove(guild):
	tt.l = f"[{tt._t()}] removed from guild '{guild}' ({guild.id})"
	await bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)

@bot.event
async def on_guild_join(guild):
	tt.l = f"[{tt._t()}] added to guild '{guild}' ({guild.id})"
	await bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)

#@bot.event
#async def on_disconnect():
#	if tt.mrestart == True:
#		pass
#	else:
#		dc_1 = f"[{tt._t()}] trashbot disconnected";print(dc_1)
#		dc_2 = ">> attempting to reconnect ...";print(dc_2)
#		try: 
#			bot.run(os.getenv("TOKEN"), reconnect=True)
#			dc = f"{dc_1}\n{dc_2}"
#			@bot.event
#			async def on_resumed():
#				rc = f"[{tt._t()}] reconnected!";print(rc)
#				tt.l = f"{dc}\n{rc}"
#		except Exception as e: print(f">> unable to restart! [{e}]")

# 		========================

keep_alive.keep_alive()
bot.run(os.getenv("TOKEN"))