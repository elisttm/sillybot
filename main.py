import discord, os
from discord.ext import commands
from a import checks
from a.funcs import f
import a.constants as tt

intents = discord.Intents.default()
intents.members = True
intents.typing = False
intents.presences = False

async def get_prefix(bot, message): 
	return commands.when_mentioned_or(f.data(tt.config, message.guild.id, 'prefix', {'prefix':tt.p})['prefix'])(bot, message)

bot = commands.Bot(
	command_prefix = get_prefix,
	case_insensitive = True,
	intents = intents,
	allowed_mentions=discord.AllowedMentions(everyone=False, roles=False,),
)
ctx = commands.Context
bot.remove_command('help')

print(f"[{f._t()}] starting ...")
for cog in tt.cogs:
	try: 
		bot.load_extension('cogs.'+cog)
		tt.loaded.append(cog)
		print(f"    [+] loaded '{cog}'")
	except Exception as e:
		print(f"    [x] failed to load '{cog}' [{e}]")
if not tt.testing:
	for command in f.data(tt.misc, 'misc', 'disabled')['disabled']:
		command = bot.get_command(command)
		command.enabled = False
		print('    [-] disabled '+command.qualified_name)

@bot.event
async def on_connect(): 
	print(f"[{f._t()}] connected!")

@bot.event
async def on_ready():
	f.log('bot ready!')
	print(f"\n  ___/-\___    Online\n |---------|   {bot.user.name}#{bot.user.discriminator} ({bot.user.id})\n  | | | | |  _                 _     _           _   \n  | | | | | | |_ _ __ __ _ ___| |__ | |__   ___ | |_ \n  | | | | | | __| '__/ _` / __| '_ \| '_ \ / _ \| __|\n  | | | | | | |_| | | (_| \__ \ | | | |_) | (_) | |_ \n  |_______|  \__|_|  \__,_|___/_| |_|_.__/ \___/ \__|\n")
	await bot.change_presence(status=tt.presence.default[1], activity=discord.Activity(type=tt.presence.default[2],name=tt.presence.default[0]))

	if not tt.testing:
		f.data_update(tt.misc, 'misc', 'guilds', [guild.id for guild in bot.guilds])
	tt.blacklist = f.data(tt.misc, 'misc', 'blacklist')['blacklist']
	tt.start_time = f._t(False)
	tt.e.upvote = bot.get_emoji(tt.e.upvote)
	tt.e.downvote = bot.get_emoji(tt.e.downvote)

@bot.check_once
def blacklist_check(ctx):
	if ctx.message.author.id not in tt.blacklist:
		return True

@bot.check
def command_disabled_check(ctx):
	data = f.data(tt.config, ctx.guild.id, 'disabled', {})
	if checks.dm_channel(ctx.message) or 'disabled' not in data or ctx.command.name not in data['disabled']:
		return True
	raise checks.GuildCommandDisabled()

@bot.event
async def on_message(message):
	if message.author.bot:
		pass
	await bot.process_commands(message)

if __name__ == '__main__':
	bot.run(os.environ["token"])
