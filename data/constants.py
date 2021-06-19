import discord
import time, datetime
import pytz
import re
import urllib, urllib.request
from pytz import timezone
import data.constants as tt

# 		========================

p = 't!'
v = "0"

desc = 'a simple discord bot made by elisttm | t!help for commands'
presence = discord.Game(f'{tt.p}help')

cogs = (
	'cogmanager',
	'errors',
	'events',
	'admin',
	'utilities',
	'customization',
	'moderation',
	'fun',
	'cats',
	'tags',
)

owner_id = 216635587837296651
logs = 686638005083308126

admins = (
	owner_id,
)
srv = {
	"rhc": 695967253900034048,
	"tmh": 822582352861593611,
	"test": 439187286278537226,
}

# important bot urls
website = 'https://elisttm.space/trashbot'
github = 'https://github.com/elisttm/trashbot'
invite = 'https://discordapp.com/oauth2/authorize?client_id=439166087498825728&scope=bot&permissions=8'

# trashbot website urls
help_list = 'http://e.elisttm.space:42069/'
tags_list = 'http://e.elisttm.space:42069/tags'
rhcooc_list = 'http://e.elisttm.space:42069/rhcooc/'
settings_page = 'http://e.elisttm.space:42069/settings.txt'
cat_url = 'http://e.elisttm.space:7777'

# database file paths
db_ = 'db/'
blacklist_db = db_+'users/blacklist.json'
reactions_db = db_+'reactions.json'
reminders_db = db_+'reminders.json'
rhcooc_db = db_+'rhcooc.json'
tags_db = db_+'tags.json'

guild_data_path = db_+'guilds/{}.json'
guild_nicknames_path = db_+'guilds/nicknames/{}.json'
guild_stickyroles_path = db_+'guilds/stickyroles/{}.json'
guild_starboard_path = db_+'guilds/starboard/{}.json'
user_data_path = db_+'users/{}.json'

time0 = '%m/%d/%y %I:%M:%S %p'	# 01/31/20 12:34:56 PM
time1 = '%H:%M:%S'						  # 12:34:56
time2 = '%I:%M:%S %p'					  # 12:34:56 PM
time3 = '%m/%d/%y' 							# 01/31/20

start_time = time.time()

def uptime(): return str(datetime.timedelta(seconds=int(round(time.time() - start_time))))
def curtime(): return datetime.datetime.now(timezone('US/Eastern')).strftime(tt.time0)
def _t(): return datetime.datetime.now(timezone('US/Eastern')).strftime(tt.time2)

def get_url(url:str): return urllib.request.urlopen(url).read().decode('utf8')

def sanitize(text: str): return text.replace('@here', '@\u200bhere').replace('@everyone', '@\u200beveryone')

def split_list(_list, and_or='and'):
	if len(_list) > 2:
		msg = f"{', '.join(_list[:-1])}, {and_or} {_list[-1]}"
	else:
		msg = f" {and_or} ".join(_list)
	return msg

markdown_characters = ['*','~','_','`','\\']
whitespace_characters = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','　']

ico = {
	'info' : 'https://i.imgur.com/3AccYL9.png',
	'cog'	 : 'https://i.imgur.com/6kiSbJl.png',
#	'warn' : 'https://i.imgur.com/MXbitfx.png',
#	'deny' : 'https://i.imgur.com/9g29yLh.png',
#	'good' : 'https://i.imgur.com/54DgIma.png',
#	'empty': 'https://i.imgur.com/TjsJ4Tv.png',
}
clr = {
	'red'		: 0xff0000,
	'green'	: 0x00ff00,
	'blue'	: 0x0000ff,
	'pink'	: 0xff78d3,
	'yellow': 0xffac33,
}

e = {
	'check': '✅',
	'warn': '⚠️',
	'x': '❌',
	'info': 'ℹ️',
	'hourglass': '⌛',
	'dice': '🎲',
	'thumbsup': '👍',
	'thumbsdown': '👎',
	'uparrow': '🔼',
	'downarrow': '🔽',
	'neutral': '😐',
}

s = " ⠀"
y = e['check']+s
w = e['warn']+s
x = e['x']+s
i = e['info']+s
h = e['hourglass']+s

loaded = {}

load_ascii = "\n  ___/-\___    Online\n |---------|   {}#{} ({})\n  | | | | |  _                 _     _           _   \n  | | | | | | |_ _ __ __ _ ___| |__ | |__   ___ | |_ \n  | | | | | | __| '__/ _` / __| '_ \| '_ \ / _ \| __|\n  | | | | | | |_| | | (_| \__ \ | | | |_) | (_) | |_ \n  |_______|  \__|_|  \__,_|___/_| |_|_.__/ \___/ \__|\n"

msg_e = '⚠️ ⠀{}'

error_guild_ids = []
smart_random_dict = {}
