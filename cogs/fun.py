import discord, json, random, datetime, urllib, urllib.request
from discord.ext import commands
from a import checks
from a.funcs import funcs
import a.constants as tt

def urban_sanitize(text:str):
	text = text.replace("\n", " ").replace("\r", " ").replace("[", "").replace("]", "").replace("`", "\`")
	return (text[:500] + f' ... (+{len(text) - 500})') if len(text) > 500 else text

class fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.smart_random = funcs.smart_random
		self.load_db = funcs.load_db
		self.dump_db = funcs.dump_db
		self.check_for_db = funcs.check_for_db
		self.send_log = funcs.send_log

		self.cat_url = 'http://e.elisttm.space:7777/'
		self.cat_json = None 
		self.cat_dirs = None
		if urllib.request.urlopen(self.cat_url).getcode() == 200:
			self.cat_json = json.loads(tt.get_url(self.cat_url+'/api/all'))
			self.cat_dirs = json.loads(tt.get_url(self.cat_url+'/directories/'))
		
		self.rhcooc_list = self.load_db(tt.rhcooc_db)
		
	async def get_cat_url(self, cat_name:str):
		if urllib.request.urlopen(self.cat_url).getcode() != 200:
			return None
		if self.cat_json == None or self.cat_dirs == None:
			self.cat_json = json.loads(tt.get_url(self.cat_url+'/api/all'))
			self.cat_dirs = json.loads(tt.get_url(self.cat_url+'/directories/'))
		if cat_name == '':
			cat_name = random.choice(self.cat_dirs)
		label = 'cat' + cat_name
		return f'{self.cat_url}/static/cat/{cat_name}/{self.smart_random(self.cat_json[cat_name], label)}'

# 		========================

	@commands.command()
	async def say(self, ctx, *, message:commands.clean_content()):
		await ctx.trigger_typing()
		try:
			message = tt.sanitize(message)
			await self.send_log(self, f"'{ctx.author}' in '{ctx.guild.name}' said '{message}'")
			await ctx.send(message)
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@checks.is_guild_admin()
	async def echo(self, ctx, channel:discord.TextChannel, *, message:commands.clean_content()):
		await ctx.trigger_typing()
		try:
			message = tt.sanitize(message)
			await channel.send(message)
			await self.send_log(self, f"'{ctx.author}' echoed '{message}' from '{ctx.guild.name}' to '{channel}' ({channel.guild.name})")
			await ctx.message.add_reaction(tt.e['check'])
		except Exception as e: 
			await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def roll(self, ctx):
		await ctx.send(tt.e['dice']+tt.s+str(random.randint(1, 6)))

	@commands.command()
	async def urban(self, ctx, *, word:str):
		await ctx.trigger_typing()
		try:
			urban_list = json.loads(tt.get_url('https://api.urbandictionary.com/v0/define?term='+urllib.parse.quote(word)))
			if len(dict(urban_list)['list']) == 0:
				await ctx.send(tt.w+"the provided word does not have any definitions!")
				return
			urban_dict = dict(random.choice(urban_list['list']))
			e_urban = discord.Embed(title=f"**{urban_sanitize(urban_dict['word']).upper()}**", color=tt.clr['pink'])
			e_urban.add_field(name=f"__**definition**__", value=f"{urban_sanitize(urban_dict['definition'])}\n", inline = False)
			e_urban.add_field(name=f"__**example**__", value=f"{urban_sanitize(urban_dict['example'])}", inline = False)
			e_urban.set_footer(text=f"created on {datetime.datetime.strptime(urban_dict['written_on'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime(tt.time3)} by {urban_dict['author']} ⠀| ⠀👍 {urban_dict['thumbs_up']}  👎 {urban_dict['thumbs_down']}")
			await ctx.send(embed=e_urban)
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	async def cat(self, ctx, cat_name:str = ''):
		await ctx.trigger_typing()
		cat_name = cat_name.lower()
		try:
			if (cat_name == 'list') or ((cat_name not in self.cat_dirs) and (cat_name != '')):
				await ctx.send(tt.i+f"list of valid cat directories: {', '.join(self.cat_dirs)}")
				return
			cat_image = await self.get_cat_url(cat_name)
			if cat_image is None:
				await ctx.send(tt.w+'the cat api is currently offline!')
			await ctx.send(cat_image)
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	# i want it to be known this is the stupidest workaround i have ever made and the fact it works baffles me
	@commands.command(aliases=[
		'floppa', 'tommy', 'gloop', 'mish', 'spock', 'marley', 'lucas', 'nori', 'thomas', 'max', 'jim', 'gupitaro', 'mona', 'xena'
		])
	async def _cat_name(self, ctx):
		await ctx.invoke(self.bot.get_command('cat'), cat_name=ctx.invoked_with)

	@commands.group(name='rhcooc')
	@commands.guild_only()
	@checks.is_in_guilds([tt.servers['rhc'], tt.servers['test']])
	async def rhcooc(self, ctx):
		await ctx.trigger_typing()
		if ctx.invoked_subcommand is None:
			try:
				await ctx.send(self.smart_random(self.rhcooc_list, 'rhcooc'))
			except Exception as error:
				await ctx.send(tt.msg_e.format(error))

	@rhcooc.command(name='add')
	@checks.is_admin()
	async def rhcooc_add(self, ctx, *, rhcooc_url=None):
		rhcooc_additions = []
		try:
			if rhcooc_url is not None:
				rhcooc_url = rhcooc_url.split(" ")
				rhcooc_additions.extend(rhcooc_url)
			if ctx.message.attachments:
				for attachment in ctx.message.attachments:
					rhcooc_additions.append(attachment.url)
			if not rhcooc_additions:
				await ctx.send(tt.w+"no urls provided!")
				return
			for url in rhcooc_additions:
				self.rhcooc_list.append(url)
			self.dump_db(tt.rhcooc_db, self.rhcooc_list)
			await ctx.send(tt.y+f"added `{', '.join(rhcooc_additions)}` to rhcooc database!")
			await self.send_log(self, f"'{ctx.author}' added '{', '.join(rhcooc_additions)}' to the rhcooc database")
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	@rhcooc.command(name='remove')
	@checks.is_admin()
	async def rhcooc_remove(self, ctx, rhcooc_url:str):
		try:
			self.rhcooc_list.remove(rhcooc_url)
			self.dump_db(tt.rhcooc_db, self.rhcooc_list)
			await ctx.send(tt.y+f"removed '{rhcooc_url}' from rhcooc database!")
			await self.send_log(self, f"'{ctx.author}' removed '{rhcooc_url}' from the rhcooc database")
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	@rhcooc.command(name='list')
	async def rhcooc_listall(self, ctx):
		rhcooc_list = self.load_db(tt.rhcooc_db)
		rhcooc_num = 0
		for url in rhcooc_list: 
			rhcooc_num += 1	
		await ctx.send(f"ℹ️ ⠀there are **{rhcooc_num}** rhcooc images in the database:\n{tt.rhcooc_list}")

# 		========================

def setup(bot):
	bot.add_cog(fun(bot))