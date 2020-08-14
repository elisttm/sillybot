import discord
import time, datetime
import pytz
from pytz import timezone
import tinydb
from tinydb import TinyDB, Query
from tinydb.operations import increment
import data.constants as tt

# 		========================

p = 't!'
v = "1.12.0:beta"

cogs = (
	'help',
	'cogmanager',
	'errors',
	'admin', 
	'utilities', 
	'moderation',
	'reactions',
	'fun', 
	'tags',
)

loaded = {}

l = ''; log0 = True; logs = 718646246482378782; 

owner_id = 216635587837296651

admins = [
	216635587837296651,	# eli (owner)
	609059779805184001, # squidd
	530937484218204172, # peter
	217663207895072768, # fluffer
	376813566591762444, # regaul
]

blacklist_pkl = "data/blacklist.pkl"
prefixes_pkl = "data/prefixes.pkl"
tags_pkl = "data/tags.pkl"


presence = discord.Game(f"{tt.p}help | v{tt.v}")
#presence = discord.Game(f"MAINTENANCE | v{tt.v}")

desc = "a simple discord bot made by elisttm | t!help for commands"

website = 'https://elisttm.space/trashbot'
invite = 'https://discordapp.com/oauth2/authorize?client_id=439166087498825728&scope=bot&permissions=8'

taglist = 'https://trashbot.elisttm.repl.co/tags'

time0 = '%m-%d-%y %H:%M:%S'		  # 01-31-05 12:34:56
time1 = '%H:%M:%S'						  # 12:34:56
time2 = '%I:%M:%S %p'					  # 12:34:56 PM
time3 = '%B %d, %Y %I:%M:%S %p' # January 31, 2005, 12:34:56 PM

start_time = time.time()

def uptime():
	current_time = time.time() 
	difference = int(round(current_time - start_time))
	return str(datetime.timedelta(seconds=difference))

def _t():
	return datetime.datetime.now(timezone('US/Eastern')).strftime(tt.time2)

def sanitize(text):
	text.replace('@everyone', '@\u200beveryone')
	text.replace('@here', '@\u200bhere')

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

# 		========================

msg_e = '```⚠️ ⠀{}```'

permdeny = discord.Embed(title=" ", color=tt.clr['red'])
permdeny.set_author(name="you do not have permission to use this command!", icon_url=tt.ico['deny'])
