# this script starts a webpage that's hosted in parallel to the bot
# repls stay online for as long as they're accessed or ~1hr when idle 
# by using a repl pinger, the bot can stay up 24/7

# repl pinger: http://ping.mat1.repl.co/

# for more information, read this thread:
# https://repl.it/talk/learn/Hosting-discordpy-bots-with-replit/11008

# 		========================

from flask import Flask, render_template
from threading import Thread
import os
import logging
import pickle
import data.constants as tt
from data.commands import help_list

# 		========================

app = Flask('')
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
logging.getLogger('werkzeug').disabled = True
os.environ['WERKZEUG_RUN_MAIN'] = 'true'

# 		========================

@app.route('/')
def main(): 
	return render_template('commands.html', cmd = help_list(), version = tt.v)

@app.route('/tags')
def tags(): 
	return render_template('tags.html', tags_list = pickle.load(open(tt.tags_pkl, "rb")))

# 		========================

def run(): app.run(host="0.0.0.0", port=8080)
def keep_alive(): server = Thread(target=run); server.start()