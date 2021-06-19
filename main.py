import discord, asyncio
import os, logging
import json
import flask
import time, datetime, pytz
from flask import Flask, render_template, request, send_from_directory, jsonify
from threading import Thread
from discord.ext import commands
from utils import checks
from utils.funcs import funcs
from data.commands import cmdl
import data.constants as tt

# 		========================

intents = discord.Intents.default()
intents.members = True

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
	await bot.get_channel(tt.logs).send(f"```{log_msg}```")

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
		print(tt.load_ascii.format(bot.user.name, bot.user.discriminator, bot.user.id))	

		await bot.change_presence(status=discord.Status.online, activity=tt.presence)
		await bot.get_channel(tt.logs).send(f"```{startup_starting}\n{startup_cm_loading}\n{startup_cm_loaded}\n{startup_connected}\n{startup_ready}```")

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
	return render_template('helplist.html', ctgs = cmdl.ctgs)	

@app.route('/rhcooc')
def rhcooc(): 
	with open(tt.rhcooc_db) as rhcooc_list_json:
		rhcooc_list = json.load(rhcooc_list_json)
	return render_template('rhcooc.html', rhcooc_list = rhcooc_list)	

@app.route('/tags')
@app.route('/tags/')
def tags_all():
	return render_template('tags.html', search = False, header = "list of all tags in the database", desc = True, tags_list = funcs.load_db(tt.tags_db))

@app.route('/tags/<int:search>')
def tags_search(search):
	return render_template('tags.html', search = True, header = f"all tags owned by user ID {search}", user_id = search, tags_list = funcs.load_db(tt.tags_db))

@app.route('/tags/json')
def tags_json():
	return jsonify(funcs.load_db(tt.tags_db))

@app.route('/settings.txt')
def static_from_root():
	return send_from_directory(app.static_folder, request.path[1:])

# 		========================

if __name__ == '__main__':
	def run(): app.run(host="0.0.0.0", port=42069)
	server = Thread(target=run)
	server.start()
	bot.run("token")
