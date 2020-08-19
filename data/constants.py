import discord
import time, datetime
import pytz
from pytz import timezone
from discord.utils import escape_mentions
import data.constants as tt

# 		========================

p = 't!'
v = "1.12.6:beta"

cogs = (
	'help',
	'cogmanager',
	'errors',
	'admin', 
	'utilities', 
	'reactions',
	'fun', 
	'tags',
)

loaded = {}

l = ''; log0 = True; logs = 718646246482378782; 

owner_id = 216635587837296651

admins = (
	owner_id,						# eli
	609059779805184001, # squidd
	530937484218204172, # peter
	217663207895072768, # fluffer
	376813566591762444, # regaul
)

blacklist_pkl = "data/pickles/blacklist.pkl"
prefixes_pkl = "data/pickles/prefixes.pkl"
tags_pkl = "data/pickles/tags.pkl"


presence = discord.Game(f"{tt.p}help | v{tt.v}")
#presence = discord.Game(f"MAINTENANCE | v{tt.v}")

desc = "a simple discord bot made by elisttm | t!help for commands"

website = 'https://elisttm.space/trashbot'
invite = 'https://discordapp.com/oauth2/authorize?client_id=439166087498825728&scope=bot&permissions=8'

cmdlist = 'https://trashbot.elisttm.repl.co'
taglist = 'https://trashbot.elisttm.repl.co/tags'


time0 = '%m/%d/%y %H:%M:%S'		  # 01-31-05 12:34:56
time1 = '%H:%M:%S'						  # 12:34:56
time2 = '%I:%M:%S %p'					  # 12:34:56 PM
time3 = '%B %d, %Y %I:%M:%S %p' # January 31, 2005, 12:34:56 PM

start_time = time.time()

def uptime():  # calculates the bots uptime
	current_time = time.time() 
	difference = int(round(current_time - start_time))
	return str(datetime.timedelta(seconds=difference))

def _t():  # gets current time in EST
	return datetime.datetime.now(timezone('US/Eastern')).strftime(tt.time2)

def tagtime():
	return datetime.datetime.now(timezone('US/Eastern')).strftime(tt.time0)

def sanitize(text: str):  # attempts to remove mentions from text
	text = text.replace('@everyone', '@\u200beveryone')
	text = text.replace('@here', '@\u200bhere')
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

msg_e = '⚠️ ⠀{}'
permdeny = '❌ ⠀you do not have permission to use this command!'
