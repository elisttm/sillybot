import os, json, random, urllib, urllib.request, datetime, tempfile
from dateutil.relativedelta import relativedelta
from colorthief import ColorThief
from io import BytesIO
import a.constants as tt

smd = {}

class f():
	def __init__(self, bot):
		self.bot = bot

	def log(text:str, prefix=True, file=None):
		if prefix != False:
			text = f"[{f._t()}]{'' if type(prefix) != str else ' '+prefix} {text}"
		print(text)
		tt.yeah.update_one({'_id':'logs'}, {"$push":{'log':{"$each":[text]}}}, upsert=False)
		if file != None:
			print(text, file=open(file[0],file[1]))

	def determine_prefix(self, message):
		try:
			return tt.config.find_one({'_id':message.guild.id},{'_id':0,'prefix':1})['prefix']
		finally:
			return tt.p

	def _t(format=tt.ti.log):
		if not format:
			return datetime.datetime.now(tt.tz.est)
		return datetime.datetime.now(tt.tz.est).strftime(format)

	def smart_random(_list, id:str):
		if id not in smd:
			smd[id] = []
		choice = random.choice(_list)
		while choice in smd[id]:
			choice = random.choice(_list)
		smd[id].append(choice)
		if len(smd[id]) > len(_list)//2:
			smd[id].pop(0)
		return choice

	def split_list(_list:list, and_or:str='and', decor:str=None):
		if decor:
			_list = [decor+x+decor for x in _list]
		if len(_list) > 2: 
			return f"{', '.join(_list[:-1])}, {and_or} {_list[-1]}" 
		return f" {and_or} ".join(_list)

	def sanitize(text:str): 
		return text.replace('@here','@\u200bhere').replace('@everyone','@\u200beveryone')

	def ctruncate(text:str, max:int):
		return (text[:max] + f' ... (+{len(text)-max})') if len(text) > max else text

	def seconds(sec:int):
		min=hr=0
		x = f"{sec}s"
		if sec > 60:
			min, sec = divmod(sec, 60)
			x = f"{min}m {sec}s"
		if min > 60:
			hr, min = divmod(min, 60)
			x = f"{hr}h {min}m {sec}s"
		return x

	def timediff(_1_, _2_, max=6, a=1):
		diff = relativedelta(_1_, _2_); text = []
		for x in [[diff.years,' year','yr'],[diff.months,' month','mo'],[diff.days,' day','d'],[diff.hours,' hour','h'],[diff.minutes,' minute','m'],[diff.seconds,' second','s']]:
			if x[0] > 0:
				text.append(f"{x[0]}{x[a]}{'s' if x[0] > 1 and a == 1 else ''}")
			if len(text) >= max:
				break
		return (', ' if a == 1 else ' ').join(text)

	def is_visually_blank(text:str):
		while text != '':
			for x in tt.whitespace_characters+tt.markdown_characters: 
				text = text.replace(x,'')
			if text != '':
				return False
		return True

	def empty(var):
		for x in [None,'',[],(),{}]:
			if var == x:
				return True
		return False

	def urltempfile(url):
		tfile = tempfile.NamedTemporaryFile()
		tfile.write(urllib.request.urlopen(url).read())
		return tfile

	def avgcolor(image):
		try: 
			if type(image) == 'str' and image.startswith('http'):
				image = urllib.request.urlopen(image).read()
			return int(hex(int('%02x%02x%02x' % ColorThief(BytesIO(image)).get_color(quality=10), 16)), 0)
		except:
			return tt.color.pink

	def open_url(url:str):
		return urllib.request.urlopen(url).read().decode('utf8')

	def load_json(path:str):
		with open(path) as data_json: 
			return json.load(data_json)

	def dump_json(path:str, data):
		with open(path, 'w') as outfile: 
			json.dump(data, outfile)

	def check_for_json(path:str):
		if not os.path.exists(path):
			os.mknod(path)
			if path.endswith('.json'):
				with open(path, 'w') as outfile: 
					json.dump({}, outfile)
			print(f"[{f._t()}] created file '{path}'")

	def data(db, id, p=None, d=None):
		x = {'_id':0}
		if p != None:
			if type(p) != list:
				p = [p]
			for p_ in p:
				x[p_] = 1
		data = db.find_one({'_id':id},x)
		if data == None:
			return d
		return data

	def data_update(db, id, key, value, action='set'):
		if action == 'set' or action == 'unset':
			if type(key) == list and len(key) > 1:
				ukeyvals = {}
				for i in range(len(key)):
					ukeyvals[key[i]] = value[i]
				udata = {"$"+action:ukeyvals}
			else:
				udata = {"$"+action:{key:value}}
		elif action == 'append': 
			udata = {"$push":{key:{"$each":[value] if type(value) != list else value}}}
		elif action == 'remove': 
			udata = {"$pull":{key:{"$in":[value] if type(value) != list else value}}}
		db.update_one({'_id':id}, udata, upsert=True)