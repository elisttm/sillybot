import discord
import time, datetime
import pytz
from pytz import timezone
import data.constants as tt

# 		========================

p = 't!' 
v = "1.9.3:beta"

cogs = (
	'cogmanager',
	'admin', 
	'moderation',
	'fun', 
#	'soundboard',
	'utilities', 
)

cogs0 = (list(cogs))
cogs0.append('general'); cogs0.remove('cogmanager')
cogs0.reverse()

loaded = {}

desc = "a simple discord bot made by elisttm | t!help for commands"

l = ''; log0 = True
logs = 718646246482378782; 
owner_id = 216635587837296651

admins = [
	216635587837296651,	# eli (owner)
	609059779805184001, # squidd
	530937484218204172, # peter
	217663207895072768, # fluffer
	376813566591762444, # regaul
]

# 		========================

presence = discord.Game(f"{tt.p}help | v{tt.v}")
website = 'https://elisttm.space/trashbot'
invite = 'https://discordapp.com/oauth2/authorize?client_id=439166087498825728&scope=bot&permissions=8'

mrestart = False

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
#  return "fuck"

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

hr = "\n------------------------------------------------------\n"
msg_e = '> ⚠️ ⠀error:  `{}`'

permdeny = discord.Embed(title=" ", color=tt.clr['red'])
permdeny.set_author(name="you do not have permission to use this command!", icon_url=tt.ico['deny'])

# 	============================

#				---  important  ---

# p					: command prefix assigned to 'bot.Commands'
# v					: version number and build
# cogs			: list of cog extensions loaded during startup
# cogs0			: a "cosmetic" cog list to make displaying commands easier
# loaded		: defines cogs as true/false when loaded/unloaded
#
# l					: logging variable
# log0			: boolien that defines if every action should be logged
# logs			: "trashbot logs" channel ID
# owner_id	: user ID of the developer (eli) 
# admins		: list of managers' user IDs

#				---  cosmetic  ---

# presence	: shown as the discord "playing" status
# website		: link to trashbot.html on elisttm.space
# time0,1...: formats for datetime
# _t()			: function to get the current time in EST
# 
# ico				: definition list of icon urls for embeds
# clr				: definition list of color codes for embeds
# hr				: "horizontal-rule" for the console
# error			: sends errors in chat in a way that looks nice
# permdeny	: gives an "insufficient permissions" warning in chat

sex = [
	"h-hewwo >///<", "hiiiii x3", "hewwo! >w<", "fuck you dumbass", "hewwo!! ^w^", "hewwo~ uwu", "hii! >wo", "raawr x3","murrrr~ uwu",

	"Rawr x3 nuzzles how are you pounces on you you're so warm o3o notices you have a bulge o: someone's happy ;) nuzzles your necky wecky~ murr~ hehehe rubbies your bulgy wolgy you're so big :oooo rubbies more on your bulgy wolgy it doesn't stop growing ·///· kisses you and lickies your necky daddy likies (; nuzzles wuzzles I hope daddy really likes $: wiggles butt and squirms I want to see your big daddy meat~ wiggles butt I have a little itch o3o wags tail can you please get my itch~ puts paws on your chest nyea~ its a seven inch itch rubs your chest can you help me pwease squirms pwetty pwease sad face I need to be punished runs paws down your chest and bites lip like I need to be punished really good~ paws on your bulge as I lick my lips I'm getting thirsty. I can go for some milk unbuttons your pants as my eyes glow you smell so musky :v licks shaft mmmm~ so musky drools all over your cock your daddy meat I like fondles Mr. Fuzzy Balls hehe puts snout on balls and inhales deeply oh god im so hard~ licks balls punish me daddy~ nyea~ squirms more and wiggles butt I love your musky goodness bites lip please punish me licks lips nyea~ suckles on your tip so good licks pre of your cock salty goodness~ eyes role back and goes balls deep mmmm~ moans and suckles"
]