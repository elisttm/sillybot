import config as c
import discord, pymongo, pytz, emoji, datetime

testing = c.testing

admins = (
	216635587837296651, # eli
)
cogs = (
	'admin', 
	'errors', 
	'events', 
	'customization',
	'starboard',
	'utilities',  
	'tags',
	'fun',
#	'voice',
)
loaded = []

db = pymongo.MongoClient(c.mongo)['trashbot']
config = db['config']
storage = db['storage']
misc = db['misc']

blacklist = misc.find_one({'_id':'misc'},{'blacklist':1}).get('blacklist', [])
start_time = datetime.datetime.utcnow()
#pytz.timezone('US/Eastern')

github = 'https://github.com/elisttm/elibot'
infopage = 'https://elisttm.space/bot'
site = 'https://bot.elisttm.space/'
settings_doc = site+'docs/settings'

class servers:
	test = 439187286278537226
	
class channels:
	log = 686638005083308126

class presence:
	activity = {'playing':discord.ActivityType.playing, 'listening':discord.ActivityType.listening}
	status = {'online':discord.Status.online, 'idle':discord.Status.idle, 'dnd':discord.Status.dnd, 'invisible':discord.Status.invisible,}
	default = [c.prefix+'help', status['online'], activity['listening']] if not testing else ['maintinence mode; expect bugs delays and frequent downtime!', status['dnd'], activity['playing']]

class icon:
	_url_ = 'https://elisttm.space/static/images/elibot/icons/'
	info = _url_+'info.png'
	cog = _url_+'cog.png'
	warn = _url_+'warn.png'
	deny = _url_+'deny.png'
	good = _url_+'check.png'
	empty = _url_+'empty.png'

class ansi:
	pink = '\033[95m'
	blue = '\033[94m'
	cyan = '\033[96m'
	green = '\033[92m'
	yellow = '\033[93m'
	red = '\033[91m'
	bold = '\033[1m'
	under = '\033[4m'
	end = '\033[0m'

class filetypes:
	img = ['.png','.jpg','.jpeg','.gif','.webp']
	vid = ['.mp4','.webm','.mov']
	snd = ['.mp3','.ogg','.wav']

# http://www.unicode.org/emoji/charts/full-emoji-list.html
class e:
	blank = "<:e_:682011306618126381>"
	check = emoji.emojize(':check_mark_button:')
	x = emoji.emojize(':cross_mark:')
	warn = emoji.emojize(':warning:')
	info = emoji.emojize(':information:')
	thumbsup = emoji.emojize(':thumbs_up:')
	thumbsdown = emoji.emojize(':thumbs_down:')
	hourglass = emoji.emojize(':hourglass_not_done:')
	pingpong = emoji.emojize(':ping_pong:')
	dice = emoji.emojize(':game_die:')
	star = emoji.emojize(':star:')
	star2 = emoji.emojize(':glowing_star:')
	star3 = emoji.emojize(':dizzy:')
	upvote = 886041781047803934
	downvote = 886041781039398982

s=e.blank
y=e.check+e.blank
w=e.warn+e.blank
x=e.x+e.blank
i=e.info+e.blank
h=e.hourglass+e.blank
n='\n'

dcolor = 0xffaec9