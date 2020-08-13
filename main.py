import discord
import sys, os
import pickle
from discord.ext import commands
from discord import opus
import keep_alive as keep_alive
import data.constants as tt
from data.commands import help_list; cmd = help_list()

# 		========================

async def determine_prefix(bot, message):
	custom_prefixes = pickle.load(open(tt.prefixes_pkl, "rb"))
	if message.guild.id in custom_prefixes:
		return custom_prefixes.get(message.guild.id)
	else:
		return tt.p

#bot = commands.Bot(command_prefix = determine_prefix, ...)

bot = commands.Bot(
	command_prefix = determine_prefix,
	case_insensitive = True)
ctx = commands.Context

bot.remove_command('help')

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

@bot.event
async def on_message(message):
	if message.author.bot:
		pass
	await bot.process_commands(message)

@bot.event
async def on_command(ctx):
	blacklist = pickle.load(open(tt.blacklist_pkl, "rb"))
	if ctx.message.author in blacklist:
		pass

@bot.event
async def on_guild_remove(guild):
	tt.l = f"[{tt._t()}] removed from guild '{guild}' ({guild.id})"
	await bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)

@bot.event
async def on_guild_join(guild):
	tt.l = f"[{tt._t()}] added to guild '{guild}' ({guild.id})"
	await bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)

# 		========================

keep_alive.keep_alive()
bot.run(os.getenv("TOKEN"))