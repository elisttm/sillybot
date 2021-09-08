import os, json, random, urllib, urllib.request, datetime, pytz
from bson.json_util import dumps
import a.constants as tt

smd = {}

tt.log_time = datetime.datetime.now(pytz.timezone('US/Eastern')).strftime(tt.ti[1])
tt.yeah.update_one({'_id':'logs'}, {"$set":{tt.log_time:[]}}, upsert=False)

class f():
	def __init__(self, bot):
		self.bot = bot

	def log(text:str, prefix=True, file=None):
		if prefix != False:
			text = f"[{f._t()}]{'' if type(prefix) != str else ' '+prefix} {text}"
		print(text)
		tt.yeah.update_one({'_id':'logs'}, {"$push":{tt.log_time:{"$each":[text]}}}, upsert=False)
		if file != None:
			print(text, file=open(file[0],file[1]))

	async def send_log(self, log:str, prefix:str='', show_prefix=True):
		log_msg = f"[{f._t()}] {prefix+' ' if prefix != '' else prefix}{log}"
		print(log_msg)
		await self.bot.get_channel(tt.channels['logs']).send(f"{log_msg.replace('`', '<')}")

	def determine_prefix(self, message):
		try:
			return f.data(tt.config, message.guild.id)['prefix']
		except:
			return tt.p
		return tt.p

	def smart_random(_list_, id:str, lmax:int=None):
		if lmax is None:
			lmax = ((round(len(_list_)/2))+1)
		if id not in smd:
			smd[id] = []
		choice = random.choice(_list_)
		while choice in smd[id]:
			choice = random.choice(_list_)
		smd[id].append(choice)
		if len(smd[id]) > lmax:
			smd[id].pop(0)
		return choice

	def split_list(_list_:list, and_or:str='and', decor:str=''):
		if decor != '':
			for item in _list_:
				_list_[item] = decor+str(_list_[item])+decor
		if len(_list_) > 2: 
			msg = f"{', '.join(_list_[:-1])}, {and_or} {_list_[-1]}"
		else: 
			msg = f" {and_or} ".join(_list_)
		return msg

	def sanitize(text:str): 
		return text.replace('@here','@\u200bhere').replace('@everyone','@\u200beveryone')

	def is_visually_blank(text:str):
		while text != '':
			for x in tt.whitespace_characters+tt.markdown_characters: 
				text = text.replace(x,'')
			if text != '':
				return False
		return True
	
	def _t(format:str=tt.ti[0]):
		return datetime.datetime.now(pytz.timezone('US/Eastern')).strftime(format)

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


	# ===  mongodb database  ===

	def data(db, id, default=None):
		_data_ = db.find_one({'_id':id}, {'_id':0})
		if _data_ == None:
			return default
		return _data_

	def data_update(db, id, key, value, action='set'):
		if action == 'set':
			if type(key) == list and len(key) > 1:
				ukeyvals = {}
				for i in range(len(key)):
					ukeyvals[key[i]] = value[i]
				udata = {"$set":ukeyvals}
				print(udata)
			else:
				udata = {"$set":{key:value}}
		elif action == 'append': 
			udata = {"$push":{key:{"$each":value}}}
		elif action == 'remove': 
			udata = {"$pull":{key:{"$in":value}}}
		db.update_one({'_id':id}, udata, upsert=True)

	def data_remove(db, id, key):
		db.update_one({'_id':id}, {"$unset":{key:{}}})

	def backup_database():
		collections = tt.db.list_collection_names()
		for i, collection_name in enumerate(collections):
			with open('misc/backup/'+collection_name+'.json', 'wb') as jsonfile:
				jsonfile.write(dumps(getattr(tt.db,collections[i]).find()).encode())