import discord, asyncio
import os, logging
import json
import flask
import time, datetime, pytz
from flask import Flask, render_template, request, send_from_directory
from threading import Thread
from discord.ext import commands
from utils import checks
from utils.funcs import funcs
from data.commands import cmdl
import data.constants as tt

# 		========================

async def send_log(log:str):
	log_msg = f"[{tt._t()}] {log}"
	print(log_msg)
	await bot.get_channel(tt.logs).send(f"```{log_msg}```")

bot = commands.Bot(
	command_prefix = funcs.determine_prefix,
	case_insensitive = True,
	owner_id = tt.owner_id,
)

bot.remove_command('help')
ctx = commands.Context

# 		========================
	
startup_starting = f"\n[{tt._t()}] starting trashbot ...\n"
print(startup_starting)

if __name__ == '__main__':
	startup_cm_num = 0
	startup_cm_loading = f"[{tt._t()}] loading {len(tt.cogs)} cogs ..."
	print(startup_cm_loading)
	for cog in tt.cogs:
		try: 
			bot.load_extension('cogs.' + cog)
			tt.loaded[cog] = True 
			startup_cm_num += 1
			print(f"    -- loaded '{cog}'")
		except Exception as error:
			tt.loaded[cog] = False
			print(f"    == unable to load '{cog}' [{error}]")
	startup_cm_loaded = f"[{tt._t()}] {startup_cm_num}/{len(tt.cogs)} cogs loaded!\n" 
	print(startup_cm_loaded)

@bot.event
async def on_connect(): 
	startup_connected = f"[{tt._t()}] connected!"
	print(startup_connected)

	@bot.event
	async def on_ready(): 
		startup_ready = f"[{tt._t()}] trashbot is online!"; 
		print(startup_ready)
		print(tt.load_ascii.format(tt.v, bot.user.name, bot.user.discriminator, bot.user.id))	

		await bot.change_presence(status=discord.Status.online, activity=tt.presence)
		await bot.get_channel(tt.logs).send(f"```{startup_starting}\n{startup_cm_loading}\n{startup_cm_loaded}\n{startup_connected}\n{startup_ready} (v{tt.v})```")

#			-----  EVENTS  -----

@bot.check_once
def blacklist(ctx):
	blacklist_list = funcs.load_db(tt.blacklist_db)
	return not ctx.message.author.id in blacklist_list

@bot.event
async def on_message(message):
	if message.author.bot:
		pass
	await bot.process_commands(message)

@bot.event
async def on_guild_remove(guild):
	await send_log(f"removed from guild '{guild}' ({guild.id})")

@bot.event
async def on_guild_join(guild):
	await send_log(f"added to guild '{guild}' ({guild.id})")

#			-----  HELP COMMAND  -----

@bot.command()
async def help(ctx):
	await ctx.trigger_typing()
	e_help = discord.Embed(title=f"click here to see a list of commands", url=tt.help_list, color=tt.clr['pink'])
	e_help.set_author(name="help menu", icon_url=tt.ico['info'])
	await ctx.send(embed=e_help)

#			-----  FLASK APP  -----

app = Flask(
	'trashbot_flask', 
	static_folder='flaskapp/static', 
	template_folder='flaskapp/templates'
)

# disables flask logs
logging.getLogger('werkzeug').setLevel(logging.ERROR)
logging.getLogger('werkzeug').disabled = True
os.environ['WERKZEUG_RUN_MAIN'] = 'true'

@app.route('/')
@app.route('/commands')
def main(): 
	ctgs = cmdl.ctgs
	return render_template('helplist.html', ctgs = ctgs, version = tt.v)	

@app.route('/rhcooc')
def rhcooc(): 
	with open(tt.rhcooc_db) as rhcooc_list_json:
		rhcooc_list = json.load(rhcooc_list_json)
	return render_template('rhcooc.html', rhcooc_list = rhcooc_list)	

@app.route('/tags', defaults={'search': None})
@app.route('/tags/', defaults={'search': None})
@app.route('/tags/<search>')
def tags(search):
	invalid_user = False
	tags_list = funcs.load_db(tt.tags_db)
	if not search:
		search = request.args.get('search')
	if not search:
		return render_template('tags.html', search = False, title = f"trashbot tag list", header = "list of all tags in the database", og_name = "list of tags", og_description = "a list of every tag in trashbot's database", tags_list = tags_list)
	try:
		user = bot.get_user(int(search))
	except:
		invalid_user = True
	if (user is None) or (invalid_user == True):
		return render_template('tags.html', search = True, title = f"trashbot tag list :: invalid ID", header = "invalid user ID provided in search", og_name = "invalid tag owner", og_description = "invalid user provided for tag list search")
	return render_template('tags.html', search = True, title = f"trashbot tag list :: {user}", header = f"all tags owned by {user} ({user.id})", og_name = f"list of tags owned by {user}", og_description = f"", user = user, user_id = user.id, tags_list = tags_list)

@app.route('/settings.txt')
def static_from_root():
	return send_from_directory(app.static_folder, request.path[1:])

# 		========================

if __name__ == '__main__':
	def run(): app.run(host="0.0.0.0", port=8080)
	server = Thread(target=run)
	server.start()
	bot.run(os.getenv("TOKEN"))