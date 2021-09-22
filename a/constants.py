import discord, pymongo, pytz, emoji, os

testing = True

p = "t!!"
admins = (
	216635587837296651, # eli
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
loaded = []

mongo = pymongo.MongoClient(os.environ["mongo"])
db = mongo['trashbot']
config = db['config']
storage = db['storage']
misc = db['misc']
tags = db['tags']

blacklist_list = []
start_time = ''

github = 'https://github.com/elisttm/trashbot'
infopage = 'https://elisttm.space/trashbot'
site = 'https://trashbot.elisttm.space/'
help_list = site+'commands'
settings_doc = site+'docs/settings'
guild_config = site+'/'

class servers:
	test = 439187286278537226
	
class channels:
	log = 686638005083308126

class ti:
	log = '%m/%d/%y %I:%M:%S %p'	# 02/10/21 2:30:15 PM
	swag = '%-m/%-d/%y @ %I:%M%P'	# 2/10/21 2:30pm
	data = '%y%m%d%H%M%S'					# 210210263015
	hms = '%I:%M:%S %p'						# 2:30:15 PM
	mdy = '%-m/%-d/%y'						# 2/10/21

class tz:
	est = pytz.timezone('US/Eastern')

class presence:
	activity = {'playing':discord.ActivityType.playing, 'listening':discord.ActivityType.listening}
	status = {'online':discord.Status.online, 'idle':discord.Status.idle, 'dnd':discord.Status.dnd, 'invisible':discord.Status.invisible,}
	default = [p+'help', status['online'], activity['listening']] if not testing else ['maintinence mode; expect bugs delays and frequent downtime!', status['dnd'], activity['playing']]

class icon:
	_url_ = 'https://elisttm.space/static/images/trashbot/icons/'
	info = _url_+'info.png'
	cog = _url_+'cog.png'
	warn = _url_+'warn.png'
	deny = _url_+'deny.png'
	good = _url_+'check.png'
	empty = _url_+'empty.png'

class color:
	pink = 0xffaec9
	red = 0xff0000
	green = 0x00ff00
	blue = 0x0000ff
	yellow = 0xffac33

# http://www.unicode.org/emoji/charts/full-emoji-list.html
class e:
	blank = "<:e_:682011306618126381>"
	upvote = 886041781047803934
	downvote = 88604178103939898
	check = emoji.emojize(':check_mark_button:')
	x = emoji.emojize(':cross_mark:')
	warn = emoji.emojize(':warning:')
	info = emoji.emojize(':information:')
	thumbsup = emoji.emojize(':thumbs_up:')
	thumbsdown = emoji.emojize(':thumbs_down:')
	hourglass = emoji.emojize(':hourglass_not_done:')
	dice = emoji.emojize(':game_die:')
	star = emoji.emojize(':star:')
	star2 = emoji.emojize(':glowing_star:')
	star3 = emoji.emojize(':dizzy:')

s=e.blank
y=e.check+e.blank
w=e.warn+e.blank
x=e.x+e.blank
i=e.info+e.blank
h=e.hourglass+e.blank
n='\n'
