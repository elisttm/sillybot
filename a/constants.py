import discord, os, time, pymongo, emoji

testing = False

p = 't!'
admins = (
	216635587837296651,
)
cogs = (
	'admin', 
	'errors', 
	'events', 
	'customization', 
	'utilities',  
	'tags',
	'fun',
)
cogs = ()
loaded = []
servers = {
	'tmh': 822582352861593611, 
	'test': 439187286278537226,
}
channels = {
	'logs': 686638005083308126
}

mongo = pymongo.MongoClient(os.environ['mongo'])
db = mongo['trashbot']
yeah = db['yeah']
config = db['config']
storage = db['storage']

blacklist_list = yeah.find_one({'_id':'misc'},{'_id':0})['blacklist']

error = 'misc/error.txt'
log = 'misc/log.txt'

infosite = 'https://elisttm.space/trashbot'
github = 'https://github.com/elisttm/trashbot'
invite = 'https://discordapp.com/oauth2/authorize?client_id=439166087498825728&scope=bot&permissions=8'

site = 'https://trashbot.elisttm.space/'
local = 'http://e.elisttm.space:42069/'
help_list = site+'commands'
tags_list = site+'tags'
settings_doc = site+'docs/settings'
guild_config = site+'/'

statuses = {
	'online': discord.Status.online,
	'idle': discord.Status.idle,
	'dnd': discord.Status.dnd,
	'invis': discord.Status.invisible,
}

ti = [
	'%m/%d/%y %I:%M:%S %p',	# 02/10/21 2:30:15 PM
	'%y%m%d%H%M%S',					# 210210263015
	'%I:%M:%S %p',					# 2:30:15 PM
	'%m/%d/%y', 						# 02/10/21
]
start_time = time.time()
log_time = ''

markdown_characters = ['*','~','_','`','\\']
whitespace_characters = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','　']

_ic = 'https://elisttm.space/static/images/trashbot/icons/'
ico = {
	'info': _ic+'info.png', 
	'cog': _ic+'cog.png', 
	'warn': _ic+'warn.png', 
	'deny': _ic+'deny.png', 
	'good': _ic+'check.png', 
	'empty': _ic+'empty.png',
}
clr = {
	'pink': 0xff78d3, 
	'red': 0xff0000, 
	'blue': 0x0000ff, 
	'green': 0x00ff00, 
	'yellow': 0xffac33,
}

# http://www.unicode.org/emoji/charts/full-emoji-list.html
e = {
	'check': 'check mark button', 
	'x': 'cross mark', 
	'warn': 'warning', 
	'info': 'information',
	'thumbsup': 'thumbsup',
	'thumbsdown': 'thumbsdown',
	'uparrow': 'upwards button',
	'downarrow': 'downwards button',
	'hourglass': 'hourglass not done', 
	'dice': 'game die', 
}
for em in e: e[em] = emoji.emojize(f":{e[em].replace(' ','_')}:")
s=" "
y=e['check']+s
w=e['warn']+s
x=e['x']+s
i=e['info']+s
h=e['hourglass']+s