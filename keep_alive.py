# this script starts a webpage that's hosted in parallel to the bot
# repls stay online for as long as they're accessed or ~1hr when idle 
# by using uptimerobot.com, the repl can be kept online indefinitely*
# *this doesnt necesarily mean 100% uptime; repls will restart but wont stay offline

# for more information, read this thread:
# https://repl.it/talk/learn/Hosting-discordpy-bots-with-replit/11008

# 		========================

from flask import Flask
from threading import Thread
import os, logging
import data.constants as tt
import data.commands as cmd

# 		========================

app = Flask('')
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
logging.getLogger('werkzeug').disabled = True
os.environ['WERKZEUG_RUN_MAIN'] = 'true'

__end			= f'</div></font></body></html>'
__start		= f'<html><body bgcolor="black"><font color="white" face="Monospace"><p align="center">trashbot is online! | v{tt.v}</p><div style="padding:0 10% 0 10%"><h1 align="center">trashbot command list</h1>'
__cmdlist	= f''

for cog in tt.cogs0:
	_cmds = ''
	__cmdlist = __cmdlist + f'</p><h3 style="margin-left:4%">{cog}</h3><p>'
	for _cogctg, _cmdctg in cmd.commands.items():
		if _cogctg == cog:
			for x, y in _cmdctg.items(): _cmds = _cmds + f"<b>{x}</b> - {y}<br>"
	__cmdlist = __cmdlist + _cmds

webpage = __start + __cmdlist + __end

# 		========================

@app.route('/')
def main(): return webpage
def run(): app.run(host="0.0.0.0", port=8080)
def keep_alive(): server = Thread(target=run); server.start()