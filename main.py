import discord, traceback, config, datetime, pytz
from discord.ext import commands
from a import checks
from a.funcs import f
from a.stuff import conf
import a.constants as tt

async def get_prefix(bot, message):
	data = tt.config.find_one({'_id':message.guild.id},{'prefix':1}) if message.guild != None else None
	return commands.when_mentioned_or(config.prefix if not data else data.get('prefix', config.prefix))(bot, message)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
	command_prefix = get_prefix,
	case_insensitive = True,
	intents = intents,
	allowed_mentions = discord.AllowedMentions(everyone=False,roles=False),
)
ctx = commands.Context
bot.remove_command('help')

print(f"[{f._t()}] starting ...")
for cog in tt.cogs:
	try: 
		bot.load_extension('cogs.'+cog)
		tt.loaded.append(cog)
		print(f"    \033[92m[+] loaded '{cog}'\033[0m")
	except Exception as error:
		print(f"    \033[91m[x] failed to load '{cog}' \033[1m\n{''.join(traceback.format_exception(type(error), error, error.__traceback__))}\033[0m")
if not tt.testing:
	for command in tt.misc.find_one({'_id':'misc'},{'disabled':1}).get('disabled', []):
		command = bot.get_command(command)
		command.enabled = False
		print(f"    \033[92m[-] disabled {command.qualified_name}\033[0m")

@bot.event
async def on_connect(): 
	print(f"[{f._t()}] connected!")

@bot.event
async def on_ready():
	f.log('ready!')

	await bot.change_presence(status=tt.presence.default[1], activity=discord.Activity(type=tt.presence.default[2],name=tt.presence.default[0]))
	tt.e.upvote = bot.get_emoji(tt.e.upvote)
	tt.e.downvote = bot.get_emoji(tt.e.downvote)
	if not tt.testing:
		tt.misc.update_one({'_id':'misc'}, {"$set":{"guilds":[guild.id for guild in bot.guilds]}}, upsert=True)

	print(f"\n  ___/-\___    Online\n |---------|   {bot.user.name}#{bot.user.discriminator} ({bot.user.id})\n  | | | | |  _                 _     _           _   \n  | | | | | | |_ _ __ __ _ ___| |__ | |__   ___ | |_ \n  | | | | | | __| '__/ _` / __| '_ \| '_ \ / _ \| __|\n  | | | | | | |_| | | (_| \__ \ | | | |_) | (_) | |_ \n  |_______|  \__|_|  \__,_|___/_| |_|_.__/ \___/ \__|\n")

@bot.check
def command_disabled_check(ctx):
	if ctx.command.name not in conf.keys['disabledcmds']['valid'] or checks.dm_channel(ctx.message):
		return True
	data = tt.config.find_one({'_id':ctx.guild.id},{'disabledcmds':1}) if ctx.guild != None else None
	if not data or ctx.command.name not in data.get('disabledcmds', []):
		return True
	raise checks.GuildCommandDisabled()

@bot.event
async def on_message(message):
	if message.author.bot or message.author.id in tt.blacklist:
		pass
	await bot.process_commands(message)

if __name__ == '__main__':
	bot.run(config.token)
