import os, io, json, random, urllib, urllib.request, datetime, pytz, tempfile, colorthief
import a.constants as tt

smart_dict = {}

class f():
	def __init__(self, bot):
		self.bot = bot

	def log(text:str, prefix=True, file=None, ansi=''):
		text = f"[{datetime.datetime.now(pytz.timezone('US/Eastern')).strftime('%m/%d/%y %I:%M:%S %p')}]{'' if type(prefix) != str else ' '+prefix} {text}" if prefix else text
		print(f"{ansi}{text}\033[0m")
		tt.misc.update_one({'_id':'logs'},{"$push":{'trashbot' if not tt.testing else 'tbtest':{"$each":[text]}}})
		if file:
			print(text, file=open(file[0],file[1]))

	def _t(format='%m/%d/%y %I:%M:%S %p', tz=pytz.timezone('US/Eastern')):
		return datetime.datetime.now(tz).strftime(format)

	def smart_random(_list_, id:str):
		choice = random.choice(_list_)
		while choice in smart_dict[id]:
			choice = random.choice(_list_)
		if id not in smart_dict:
			smart_dict[id] = [choice]
		else:
			smart_dict[id].append(choice)
		if len(smart_dict[id]) >= len(_list_)//2:
			smart_dict[id].pop(0)
		return choice

	def split_list(_list_:list, and_or:str="and", decor:str=None):
		if decor:
			_list_ = [decor+item+decor for item in _list_]
		return f"{', '.join(_list_[:-1])}, {and_or} {_list_[-1]}" if len(_list_) > 2 else f" {and_or} ".join(_list_)

	def seconds(sec:int):
		min = hr = 0
		x = f"{sec}s"
		if sec >= 60:
			min, sec = divmod(sec, 60)
			x = f"{min}m {sec}s"
		if min >= 60:
			hr, min = divmod(min, 60)
			x = f"{hr}h {min}m {sec}s"
		return x

	def urltempfile(url):
		tfile = tempfile.NamedTemporaryFile()
		tfile.write(urllib.request.urlopen(url).read())
		return tfile

	def avgcolor(image):
		try: 
			if type(image) == str and image.startswith('http'):
				image = urllib.request.urlopen(image).read()
			return int(hex(int('%02x%02x%02x' % colorthief.ColorThief(io.BytesIO(image)).get_color(quality=10),16)),0)
		except:
			return tt.dcolor

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
	
	def data(db, id, p=None, d=None):
		projection = {'_id':0}
		if p != None:
			for _p_ in [p] if type(p) != list else p:
				projection[_p_] = 1
		data = db.find_one({'_id':id},projection)
		if not data: return d
		return data

	def _set(db, id, keyvals):
		db.update_one({'_id':id}, keyvals, upsert=True)

	def _unset(db, id, keys):
		keys = [keys] if type(keys) != list else keys
		db.update_one({'_id':id}, {"$unset":{x:0 for x in keys}}, upsert=False)

	def _list(db, id, key, value, a='add'):
		x = {'add':['$push','$each'], 'remove':['$pull','$in']}
		db.update_one({'_id':id}, {x[a][0]:{key:{x[a][1]:[value] if type(value) != list else value}}}, upsert=True)