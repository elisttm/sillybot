import os, json, random
import a.constants as tt

class funcs():
	def __init__(self, bot):
		self.bot = bot

	async def send_log(self, log:str, prefix:str = '', show_prefix = True):
		if prefix != '': 
			prefix += ' '
		log_msg = f"[{tt._t()}] {prefix}{log}"
		print(log_msg)
		await self.bot.get_channel(tt.channels['logs']).send(f"```{log_msg.replace('`', '<')}```")

	def determine_prefix(self, message):
		try:
			guild_data_path = tt.guild_data_path.format(str(message.guild.id))
			if os.path.exists(guild_data_path):
				guild_data = funcs.load_db(guild_data_path)
				if 'prefix' in guild_data:
					return guild_data['prefix']
			return tt.p
		except:
			return tt.p

	def smart_random(_list_, list_id:str, max_per:int=None):
		if max_per is None:
			max_per = ((round(len(_list_)/2))+1)
		if list_id not in tt.smart_random_dict:
			tt.smart_random_dict[list_id] = []
		choice = random.choice(_list_)
		while choice in tt.smart_random_dict[list_id]:
			choice = random.choice(_list_)
		tt.smart_random_dict[list_id].append(choice)
		if len(tt.smart_random_dict[list_id]) > max_per:
			tt.smart_random_dict[list_id].pop(0)
		return choice

	def load_db(path:str):
		with open(path) as data_json: 
			return json.load(data_json)

	def dump_db(path:str, data):
		with open(path, 'w') as outfile: 
			json.dump(data, outfile)

	def check_for_db(path:str):
		if not os.path.exists(path):
			#if guild_id:
			#	if not os.path.exists(f'db/guilds/{guild_id}'):	
			#		os.mkdir(f'db/guilds/{guild_id}')
			os.mknod(path)	
			data = {}
			with open(path, 'w') as outfile: 
				json.dump(data, outfile)
			print(f"[{tt._t()}] created file '{path}'")