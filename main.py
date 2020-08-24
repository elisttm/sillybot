import discord
import os
import pickle
import logging
from flask import Flask, render_template, request
from threading import Thread
from discord.ext import commands
import data.constants as tt
from data.commands import help_list

# 		========================

async def determine_prefix(bot, message):
	try:
		custom_prefixes = pickle.load(open(tt.prefixes_pkl, "rb"))
		if message.guild.id in custom_prefixes:
			return custom_prefixes.get(message.guild.id)
		else:
			return tt.p
	except:
		return tt.p

bot = commands.Bot(
	command_prefix = determine_prefix,
	case_insensitive = True,
)

ctx = commands.Context
bot.remove_command('help')

app = Flask('', static_folder='flaskapp/static', template_folder='flaskapp/templates')
log = logging.getLogger('werkzeug'); log.setLevel(logging.ERROR); logging.getLogger('werkzeug').disabled = True; os.environ['WERKZEUG_RUN_MAIN'] = 'true'

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
		except Exception as error:
			tt.loaded[cog] = False
			print(f"   -- unable to load '{cog}' [{error}]")
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

@bot.event
async def on_message(message):
	if message.author.bot:
		pass
	await bot.process_commands(message)

@bot.event
async def on_guild_remove(guild):
	tt.l = f"[{tt._t()}] removed from guild '{guild}' ({guild.id})"
	await bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)

@bot.event
async def on_guild_join(guild):
	tt.l = f"[{tt._t()}] added to guild '{guild}' ({guild.id})"
	await bot.get_channel(tt.logs).send(f"```{tt.l}```"); print(tt.l)

@bot.command()
async def help(ctx):
	await ctx.trigger_typing()
	try:
		custom_prefixes = pickle.load(open(tt.prefixes_pkl, "rb"))
		if ctx.message.guild.id in custom_prefixes: 
			desc_prefix = f"'{custom_prefixes[ctx.message.guild.id]}' (custom)"
		else: 
			desc_prefix = f"'{tt.p}'"
	except:
		desc_prefix = f"'{tt.p}'"
	e_invite = discord.Embed(title=f"click here to see a list of commands", url=tt.helplist, description=f"command prefix: {desc_prefix}", color=tt.clr['pink'])
	e_invite.set_author(name="help menu", icon_url=tt.ico['info'])
	e_invite.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.avatar_url_as(format='png'))
	await ctx.send(embed=e_invite)

def get_user(user_id:int):
	user = bot.get_user(user_id)
	return user

# 		========================

@app.route('/')
@app.route('/commands')
def main(): return render_template('helplist.html', cmd = help_list(), version = tt.v)	

@app.route('/tags', defaults={'search': None})
@app.route('/tags/', defaults={'search': None})
@app.route('/tags/<search>')
def tags(search):
	if not search:
		search = request.args.get('search')
	if not search:
		return render_template('tags.html', search = False, title = f"trashbot tag list", header = "list of all tags in the database", og_name = "list of tags", og_description = "a list of every tag in trashbot's database", tags_list = pickle.load(open(tt.tags_pkl, "rb")))
	try:
		user_id = int(search)
		user = get_user(user_id = user_id)
	except:
		return render_template('tags.html', search = True, title = f"trashbot tag list :: invalid ID", header = "invalid user ID provided in search", og_name = "invalid tag owner", og_description = "invalid user provided for tag list search")
	if user is None:
		return render_template('tags.html', search = True, title = f"trashbot tag list :: invalid ID", header = "invalid user ID provided in search", og_name = "invalid tag owner", og_description = "invalid user provided for tag list search")
	return render_template('tags.html', search = True, title = f"trashbot tag list :: {user}", header = f"all tags owned by ID {user} ({user.id})", og_name = f"list of tags owned by {user}", og_description = f"", user = user, user_id = user_id, tags_list = pickle.load(open(tt.tags_pkl, "rb")))

# 		========================

if __name__ == '__main__':
	def run(): 
		app.run(host="0.0.0.0", port=8080)
	server = Thread(target=run)
	server.start()
	bot.run(os.getenv("TOKEN"))