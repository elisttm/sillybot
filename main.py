import discord, asyncio, flask, os, json, logging, threading, time, datetime, pytz
from discord.ext import commands
from a.funcs import funcs
import a.commands as cmds
import a.configs as conf
import a.constants as tt

intents = discord.Intents.default()
intents.members = True
intents.typing = False
intents.presences = False

bot = commands.Bot(
	command_prefix = funcs.determine_prefix,
	case_insensitive = True,
	owner_id = tt.owner_id,
	intents = intents,
)

bot.remove_command('help')
ctx = commands.Context

async def send_log(log:str):
	log_msg = f"[{tt._t()}] {log}"
	print(log_msg)
	await bot.get_channel(tt.channels['logs']).send(f"{log_msg}")

# 		========================

print(f"\n[{tt._t()}] starting trashbot ...\n")

if __name__ == '__main__':
	startup_cm_num = 0
	print(f"[{tt._t()}] loading {len(tt.cogs)} cogs ...")
	for cog in tt.cogs:
		try: 
			bot.load_extension('cogs.'+cog)
			tt.loaded[cog] = True 
			startup_cm_num += 1
			print(f"    -- loaded '{cog}'")
		except Exception as error:
			tt.loaded[cog] = False
			print(f"    <> unable to load '{cog}' [{error}]")
	print(f"[{tt._t()}] {startup_cm_num}/{len(tt.cogs)} cogs loaded!\n") 

@bot.event
async def on_connect(): 
	print(f"[{tt._t()}] connected!")

@bot.event
async def on_ready(): 
	startup_ready = f"[{tt._t()}] trashbot is online!"; print(startup_ready)
	print(tt.load_ascii.format(bot.user.name, bot.user.discriminator, bot.user.id))	

	await bot.change_presence(status=discord.Status.online, activity=tt.presence)
	await bot.get_channel(tt.channels['logs']).send(f"{startup_ready}")

@bot.check_once
def blacklist(ctx):
	blacklist_list = funcs.load_db(tt.blacklist_db)
	return not ctx.message.author.id in blacklist_list

@bot.event
async def on_message(message):
	if message.author.bot:
		pass
	await bot.process_commands(message)

# 		========================

app = flask.Flask('tbwebserver', static_folder='web/static',)
app.config['JSON_SORT_KEYS'] = False

logging.getLogger('werkzeug').setLevel(logging.ERROR)
logging.getLogger('werkzeug').disabled = True
os.environ['WERKZEUG_RUN_MAIN'] = 'true'

@app.route('/')
def index(): return 'meow'

@app.route('/api/botguilds')
def botguilds():
	bot_guilds = []
	for guild in bot.guilds:
		bot_guilds.append(guild.id)
	return flask.jsonify(bot_guilds)

@app.route('/api/guilds')
def db_guildlist(): return flask.jsonify(os.listdir(tt.db_+'/guilds/config'))	

@app.route('/api/guild/<int:id>')
def db_guilds(id): return flask.jsonify(funcs.load_db(tt.guild_data_path.format(id)))	

@app.route('/api/commands')
def commands_json(): return flask.jsonify(cmds._c_)

@app.route('/api/tags')
def tags_json(): return flask.jsonify(funcs.load_db(tt.tags_db))

@app.route('/api/rhcooc')
def rhcooc_json(): return flask.jsonify(funcs.load_db(tt.rhcooc_db))

# 		========================

if __name__ == '__main__':
	def run(): app.run(host="0.0.0.0", port=42069)
	server = threading.Thread(target=run)
	server.start()
	#bot.run(os.environ['TOKEN'])