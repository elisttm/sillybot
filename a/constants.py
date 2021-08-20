import discord, time, datetime, urllib, urllib.request
from pytz import timezone
import a.constants as tt

p = 't!'
desc = 'a simple discord bot by @elisttm'
#presence = discord.Game('currently testing a ton of changes! please excuse any bugs and errors')
presence = discord.Activity(type=discord.ActivityType.listening, name=f'{tt.p}help')

cogs = ('admin', 'errors', 'events', 'customization', 'utilities', 'fun', 'tags',)

owner_id = 216635587837296651
admins = (owner_id,)

servers = {'rhc':695967253900034048, 'tmh':822582352861593611, 'test':439187286278537226,}
channels = {'logs':686638005083308126}

# important bot urls
website = 'https://elisttm.space/trashbot'
github = 'https://github.com/elisttm/trashbot'
invite = 'https://discordapp.com/oauth2/authorize?client_id=439166087498825728&scope=bot&permissions=8'

# trashbot website urls
cat_url = 'http://e.elisttm.space:7777/'
site = 'https://trashbotwebsite.elisttm.repl.co/'
localhost = 'http://e.elisttm.space:42069/'
help_list = site+'commands'
tags_list = site+'tags'
rhcooc_list = site+'rhcooc'
guild_config = site+''

# database file paths
db_ = 'db/'
blacklist_db = db_+'blacklist.json'
reminders_db = db_+'reminders.json'
rhcooc_db = db_+'rhcooc.json'
tags_db = db_+'tags.json'

guild_data_path = db_+'guilds/config/{}.json'
guild_nicknames_path = db_+'guilds/nicknames/{}.json'
guild_stickyroles_path = db_+'guilds/stickyroles/{}.json'
guild_starboard_path = db_+'guilds/starboard/{}.json'

# time formats n other time stuff
time0 = '%m/%d/%y %I:%M:%S %p'	# 01/31/20 12:34:56 PM
time1 = '%H:%M:%S'						  # 12:34:56
time2 = '%I:%M:%S %p'					  # 12:34:56 PM
time3 = '%m/%d/%y' 							# 01/31/20

start_time = time.time()
def uptime(): return str(datetime.timedelta(seconds=int(round(time.time() - start_time))))
def curtime(): return datetime.datetime.now(timezone('US/Eastern')).strftime(tt.time0)
def _t(): return datetime.datetime.now(timezone('US/Eastern')).strftime(tt.time0)

# misc functions
def get_url(url:str): return urllib.request.urlopen(url).read().decode('utf8')

def sanitize(text: str): return text.replace('@here', '@\u200bhere').replace('@everyone', '@\u200beveryone')

def split_list(_list, and_or='and'):
	if len(_list) > 2: msg = f"{', '.join(_list[:-1])}, {and_or} {_list[-1]}"
	else: msg = f" {and_or} ".join(_list)
	return msg

loaded = {}; error_guild_ids = []; smart_random_dict = {}

# message formatting stuff
markdown_characters = ['*','~','_','`','\\']
whitespace_characters = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','　']

icod = localhost+'static/icons/'
ico = {'info':icod+'info.png', 'cog':icod+'cog.png', 'warn':icod+'warn.png', 'deny':icod+'deny.png', 'good':icod+'check.png', 'empty':icod+'empty.png',}
clr = {'pink':0xff78d3, 'red':0xff0000, 'blue':0x0000ff, 'green':0x00ff00, 'yellow':0xffac33,}
e = {
	'check':'✅', 'x': '❌', 'warn':'⚠️', 'info':'ℹ️',
	'thumbsup':'👍', 'thumbsdown':'👎', 'uparrow':'🔼', 'downarrow':'🔽',
	'hourglass':'⌛', 'dice':'🎲', 'neutral':'😐',
}

load_ascii = "\n  ___/-\___    Online\n |---------|   {}#{} ({})\n  | | | | |  _                 _     _           _   \n  | | | | | | |_ _ __ __ _ ___| |__ | |__   ___ | |_ \n  | | | | | | __| '__/ _` / __| '_ \| '_ \ / _ \| __|\n  | | | | | | |_| | | (_| \__ \ | | | |_) | (_) | |_ \n  |_______|  \__|_|  \__,_|___/_| |_|_.__/ \___/ \__|\n"

# error message stuff

s=" ⠀"; y=e['check']+s; w=e['warn']+s; x=e['x']+s; i=e['info']+s; h=e['hourglass']+s
msg_e = w+'{}'

class m_err(): # errors
	no_permission = x+"you do not have permission to use this command!"
	no_permission_perms = x+"{} need the permissions {} to use this command!"
	on_cooldown = x+"please wait `{}s` before using this command again!"
	invalid_params = w+"invalid command parameter(s) provided! {}"
	disabled_in_dm = x+"that command only avaialable in servers!"
	guild_command_disabled = x+"that command is disabled in this server!"