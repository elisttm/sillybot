import discord, os
from discord.ext import commands
from a.funcs import f
import a.configs as conf
import a.constants as tt

intents = discord.Intents.default()
intents.members = True
intents.typing = False
intents.presences = False

bot = commands.Bot(
	command_prefix = f.determine_prefix,
	case_insensitive = True,
	intents = intents,
)

bot.remove_command('help')
ctx = commands.Context
	
# 		========================

print(f"[{f._t()}] starting trashbot ...\n")
if __name__ == '__main__':
	startup_cm_num = 0
	print(f"[{f._t()}] loading {len(tt.cogs)} cogs ...")
	for cog in tt.cogs:
		try: 
			bot.load_extension('cogs.'+cog)
			tt.loaded.append(cog)
			print(f"    -- loaded '{cog}'")
		except Exception as error:
			print(f"    <> failed to load '{cog}' [{error}]")
	print(f"[{f._t()}] {len(tt.loaded)}/{len(tt.cogs)} cogs loaded!\n") 

@bot.event
async def on_connect(): print(f"[{f._t()}] connected!")

@bot.event
async def on_ready():

	f.log('trashbot is online!')
	print(f"\n  ___/-\___    Online\n |---------|   {bot.user.name}#{bot.user.discriminator} ({bot.user.id})\n  | | | | |  _                 _     _           _   \n  | | | | | | |_ _ __ __ _ ___| |__ | |__   ___ | |_ \n  | | | | | | __| '__/ _` / __| '_ \| '_ \ / _ \| __|\n  | | | | | | |_| | | (_| \__ \ | | | |_) | (_) | |_ \n  |_______|  \__|_|  \__,_|___/_| |_|_.__/ \___/ \__|\n")
	await bot.get_channel(tt.channels['logs']).send('trashbot is online!')

	if tt.testing: 
		await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.playing,name=f'testing! trashbot is currently being worked on; expect bugs, delays, and frequent downtime!'))
	else: 
		await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening,name=f'{tt.p}help'))

	guild_list = []
	for guild in bot.guilds: 
		guild_list.append(guild.id)
	f.data_update(tt.yeah, 'misc', 'guilds', guild_list)

@bot.check_once
def blacklist(ctx):
	return not ctx.message.author.id in tt.blacklist_list

@bot.check
def is_disabled(ctx):
	if ctx.command.name in conf.disable_commands:
		try:
			data = f.data(tt.config, ctx.guild.id)
			if data is not None and 'disable' in data and ctx.command.name in data['disable']:
				return False
		except:
			return True
	return True

@bot.event
async def on_message(message):
	if message.author.bot:
		pass
	await bot.process_commands(message)

# 		========================

if __name__ == '__main__':
	bot.run(os.environ['TOKEN'])