import discord
import time, datetime
import pytz
from pytz import timezone
import data.constants as tt

# 		========================

p = 't!'
v = "1.13.8"

desc = 'a simple discord bot made by elisttm | t!help for commands'
presence = discord.Game(f'{tt.p}help | v{tt.v}')

cogs = (
	'cogmanager',
	'errors',
	'admin', 
	'utilities', 
	'moderation',
	'fun',
	'cats', 
	'tags',
	'reactions',
)

owner_id = 216635587837296651
logs = 718646246482378782
admins = (
	owner_id,						# eli
	609059779805184001, # squidd
	530937484218204172, # peter
	217663207895072768, # fluffer
	376813566591762444, # regaul
)

website = 'https://elisttm.space/trashbot'
github = 'https://github.com/elisttm/trashbot'
invite = 'https://discordapp.com/oauth2/authorize?client_id=439166087498825728&scope=bot&permissions=8'

cat_site = 'http://cat.elisttm.space:7777'
help_list = 'https://trashbot.elisttm.space/commands'
tags_list = 'https://trashbot.elisttm.space/tags'

mcserver = 'mc.elisttm.space'

blacklist_pkl = 'data/pickles/blacklist.pkl'
prefixes_pkl = 'data/pickles/prefixes.pkl'
tags_pkl = 'data/pickles/tags.pkl'

time0 = '%m-%d-%y %H:%M:%S'		  # 01-31-05 12:34:56
time1 = '%H:%M:%S'						  # 12:34:56
time2 = '%I:%M:%S %p'					  # 12:34:56 PM
time3 = '%B %d, %Y' 						# January 31, 2005, 12:34:56 PM

start_time = time.time()

def uptime():
	current_time = time.time() 
	difference = int(round(current_time - start_time))
	return str(datetime.timedelta(seconds=difference))

def _t():
	return datetime.datetime.now(timezone('US/Eastern')).strftime(tt.time2)

def sanitize(text: str):
	text = text.replace('@everyone', '@\u200beveryone')
	text = text.replace('@here', '@\u200bhere')
	return text

def urban_sanitize(text:str):
	text = text.replace("\n", " ").replace("\r", " ").replace("[", "").replace("]", "").replace("`", "\`")
	return text

ico = {
	'info' : 'https://i.imgur.com/3AccYL9.png',
	'cog'	 : 'https://i.imgur.com/6kiSbJl.png',
	'warn' : 'https://i.imgur.com/MXbitfx.png',
	'deny' : 'https://i.imgur.com/9g29yLh.png',
	'good' : 'https://i.imgur.com/54DgIma.png',
}
clr = {
	'red'		: 0xff0000,
	'green'	: 0x00ff00,
	'blue'	: 0x0000ff,
	'pink'	: 0xff78d3,
	'yellow': 0xbf993a,
}

loaded = {}

load_ascii = "\n  ___/-\___    Online | v{}\n |---------|   {}#{} ({})\n  | | | | |  _                 _     _           _   \n  | | | | | | |_ _ __ __ _ ___| |__ | |__   ___ | |_ \n  | | | | | | __| '__/ _` / __| '_ \| '_ \ / _ \| __|\n  | | | | | | |_| | | (_| \__ \ | | | |_) | (_) | |_ \n  |_______|  \__|_|  \__,_|___/_| |_|_.__/ \___/ \__|\n"

msg_e = '⚠️ ⠀{}'



#		BASIC INFO
# p : default prefix
# v : bot version
# desc : simple bot description
# presence : default bot discord presence/status
# cogs : list of modules to load from the cogs dir

#		DISCORD IDs
# owner_id : bot owner id (me)
# logs : log channel id
# admins : list of bot admins

#		URLS AND PATHS
# website : elisttm.space trashbot page url
# github : trashbot github page url 
# invite : oauth2 trashbot invite url
# cat_site : url of my random cat website
# help_list : url of the command list page hosted by trashbot 
# tags_list : url of the tag list page hosted by trashbot
# *_pkl : path to pickle db file

#		FUNCTIONS AND WHATEVER
# time0,1,2... : different strftime formats
# start_time : timestamp of when the bot started
# uptime() : function that calculates the bots uptime
# _t() : function that gets the time in est (used in logs)
# sanitize() : function that removes unwanted parts of a string

#		COSMETIC
# ico : dict of embed icon urls
# clr : dict of embed color hexes
# loaded : dict that stores the loaded/unloaded status of a cog
# load_ascii : the ascii art shown in console when trashbot starts
# msg_e : basic format of errors sent as messages
# permdeny : basic format of a "permission denied" error