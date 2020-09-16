import discord
import time, datetime
import pytz
import re
import urllib, urllib.request
from pytz import timezone
import data.constants as tt

# 		========================

p = 't!'
v = "1.16.1"

desc = 'a simple discord bot made by elisttm | t!help for commands'
presence = discord.Game(f'{tt.p}help | v{tt.v}')

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
logs = 718646246482378782

admins = (
	owner_id,						# eli
	217663207895072768, # fluffer
	530937484218204172, # peter
	376813566591762444, # regaul
	462354301025779733, # grumm
	382648674263498752, # merms
	319101801012133889, # sharpz
	609059779805184001, # squidd

)
srv = {
	"rhc": 695967253900034048,
	"tmh": 379723217293803526,
	"test": 439187286278537226,
}

# important bot urls
website = 'https://elisttm.space/trashbot'
github = 'https://github.com/elisttm/trashbot'
invite = 'https://discordapp.com/oauth2/authorize?client_id=439166087498825728&scope=bot&permissions=8'

# trashbot website urls
help_list = 'https://trashbot.elisttm.space/commands'
tags_list = 'https://trashbot.elisttm.space/tags'
rhcooc_list = 'https://trashbot.elisttm.space/rhcooc'
names_list = 'https://trashbot.elisttm.space/names'
settings_page = 'https://trashbot.elisttm.space/settings.txt'

# database file paths
blacklist_db = 'data/db/users/blacklist.json'
reactions_db = 'data/db/reactions.json'
reminders_db = 'data/db/reminders.json'
rhcooc_db = 'data/db/rhcooc.json'
tags_db = 'data/db/tags/tags.json'
tags_queue = 'data/db/tags/tags_queue.json'
guild_data_path = 'data/db/guilds/{}.json'
guild_nicknames_path = 'data/db/guilds/nicknames/{}.json'
user_data_path = 'data/db/users/{}.json'

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
	'yellow': 0xbf993a,
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
	'up': '🔼',
	'down': '🔽',
	'neutral': '😐',
}

s = " ⠀"
y = e['check']+s
w = e['warn']+s
x = e['x']+s
i = e['info']+s
h = e['hourglass']+s

loaded = {}

load_ascii = "\n  ___/-\___    Online | v{}\n |---------|   {}#{} ({})\n  | | | | |  _                 _     _           _   \n  | | | | | | |_ _ __ __ _ ___| |__ | |__   ___ | |_ \n  | | | | | | __| '__/ _` / __| '_ \| '_ \ / _ \| __|\n  | | | | | | |_| | | (_| \__ \ | | | |_) | (_) | |_ \n  |_______|  \__|_|  \__,_|___/_| |_|_.__/ \___/ \__|\n"

msg_e = '⚠️ ⠀{}'

error_note = ''
error_guild_ids = []
error_noperm = ''
smart_random_dict = {}