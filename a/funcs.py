import os, io, json, random, urllib, urllib.request, datetime, tempfile, colorthief
from dateutil.relativedelta import relativedelta
import a.constants as tt

smd = {}

class f():
	def __init__(self, bot):
		self.bot = bot

	def log(text:str, prefix=True, file=None):
		if prefix != False:
			text = f"[{f._t()}]{'' if type(prefix) != str else ' '+prefix} {text}"
		print(text)
		tt.misc.update_one({'_id':'logs'}, {"$push":{'log':{"$each":[text]}}})
		if file != None:
			print(text, file=open(file[0],file[1]))

	def _t(format=tt.ti.log, tz=tt.tz.est):
		if format == False:
			return round(datetime.datetime.utcnow().timestamp())
		elif format == None:
			return datetime.datetime.now(tz)
		return datetime.datetime.now(tz).strftime(format)

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
		diff = relativedelta(_1_, _2_) 
		text = []
		for x in [[diff.years,' year','yr'],[diff.months,' month','mo'],[diff.days,' day','d'],[diff.hours,' hour','h'],[diff.minutes,' minute','m'],[diff.seconds,' second','s']]:
			if x[0] > 0:
				text.append(f"{x[0]}{x[a]}{'s' if x[0] > 1 and a == 1 else ''}")
			if len(text) >= max:
				break
		return (', ' if a == 1 else ' ').join(text)

	def urltempfile(url):
		tfile = tempfile.NamedTemporaryFile()
		tfile.write(urllib.request.urlopen(url).read())
		return tfile

	def avgcolor(image):
		try: 
			if type(image) == 'str' and image.startswith('http'):
				image = urllib.request.urlopen(image).read()
			return int(hex(int('%02x%02x%02x' % colorthief.ColorThief(io.BytesIO(image)).get_color(quality=10),16)),0)
		except:
			return tt.color.pink

	def open_url(url:str):
		return urllib.request.urlopen(url).read().decode('utf8')

	def load_json(path:str):
		if os.path.exists(path):
			return {}
		with open(path) as data_json: 
			return json.load(data_json)

	def dump_json(path:str, data):
		with open(path, 'w') as outfile: 
			json.dump(data, outfile)

	def data_update(db, id, key, value, action='set'):
		actlist = {'append':['$push','$each'],'remove':['$pull','$in']}
		if action in ['set','unset','inc']:
			if type(key) == list and len(key) > 1:
				ukeyvals = {}
				for i in range(len(key)):
					ukeyvals[key[i]] = value[i]
				udata = {"$"+action:ukeyvals}
			else:
				udata = {"$"+action:{key:value}}
		elif action in actlist:
			udata = {actlist[action][0]:{key:{actlist[action][1]:[value] if type(value) != list else value}}}
		db.update_one({'_id':id}, udata, upsert=True)


	def data(db, id, p=None, d=None):
		projection = {'_id':0}
		if p != None:
			for _p_ in [p] if type(p) != list else p:
				projection[_p_] = 1
		data = db.find_one({'_id':id},projection)
		if not data: 
			return d
		return data

	def d_set(db, id, keyvals):
		db.update_one({'_id':id}, keyvals, upsert=True)
	#f.d_set(tt.config, ctx.guild.id, {"$set":{key:value[0]}})

	def d_unset(db, id, key):
		db.update_one({'_id':id}, {"$unset":{x:0 for x in key}} if type(key) == list else {"$unset":{key:0}}, upsert=False)

	def d_list(db, id, action, key, value):
		x = ['$push','$each'] if action == 'push' else ['$pull','$in']
		db.update_one({'_id':id}, {x[0]:{key:{x[1]:[value] if type(value) != list else value}}}, upsert=True)

	def d_del(db, id):
		db.delete_one({'_id':id})