import discord, json, random, urllib, urllib.request, datetime
from discord.ext import commands
from a import checks
from a.funcs import f
import a.constants as tt

def urban_sanitize(text:str):
	text = text.replace("\n", " ").replace("\r", " ").replace("[", "").replace("]", "").replace("`", "\`")
	return (text[:500] + f' ... (+{len(text) - 500})') if len(text) > 500 else text

class fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.cat_url = 'http://e.elisttm.space:7777/'
		try:
			self.cat_json = json.loads(f.open_url(self.cat_url+'/api/all'))
			self.cat_dirs = json.loads(f.open_url(self.cat_url+'/directories/'))
		except:
			self.cat_json = None 
			self.cat_dirs = None
				
	async def get_cat_url(self, cat_name:str):
		if urllib.request.urlopen(self.cat_url).getcode() != 200:
			return None
		if self.cat_json == None or self.cat_dirs == None:
			self.cat_json = json.loads(f.open_url(self.cat_url+'/api/all'))
			self.cat_dirs = json.loads(f.open_url(self.cat_url+'/directories/'))
		if cat_name == '':
			cat_name = random.choice(self.cat_dirs)
		return f"{self.cat_url}/static/cat/{cat_name}/{f.smart_random(self.cat_json[cat_name], 'cat'+cat_name)}"

# 		========================

	@commands.command()
	async def say(self, ctx, *, message:commands.clean_content()):
		message = f.sanitize(message)
		f.log(f"{ctx.author} in '{ctx.guild.name}' used say '{message}'")
		await ctx.send(message)
		
	@commands.command()
	@checks.is_guild_admin()
	async def echo(self, ctx, channel:discord.TextChannel, *, message:commands.clean_content()):
		message = f.sanitize(message)
		await channel.send(message)
		f.log(f"{ctx.author} in '{ctx.guild.name}' to #{channel} {'('+channel.guild.name+')' if channel.guild.name != ctx.guild.name else ''} echoed '{message}'")
		await ctx.message.add_reaction(tt.e['check'])

	@commands.command()
	async def roll(self, ctx):
		await ctx.send(tt.e['dice']+tt.s+'you rolled a '+str(random.randint(1, 6)))

	@commands.command()
	async def urban(self, ctx, *, word:str):
		await ctx.trigger_typing()
		urban_list = json.loads(f.open_url('https://api.urbandictionary.com/v0/define?term='+urllib.parse.quote(word)))
		if len(dict(urban_list)['list']) == 0:
			await ctx.send(tt.w+"the provided word does not have any definitions!")
			return
		urban_dict = dict(random.choice(urban_list['list']))
		e_urban = discord.Embed(title=f"**{urban_sanitize(urban_dict['word']).upper()}**", color=tt.clr['pink'])
		e_urban.add_field(name=f"__**definition**__", value=f"{urban_sanitize(urban_dict['definition'])}\n", inline = False)
		e_urban.add_field(name=f"__**example**__", value=f"{urban_sanitize(urban_dict['example'])}", inline = False)
		e_urban.set_footer(text=f"created {datetime.datetime.strptime(urban_dict['written_on'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%m/%d/%y')} by {urban_dict['author']}\n{tt.e['thumbsup']} {urban_dict['thumbs_up']}  {tt.e['thumbsdown']} {urban_dict['thumbs_down']}")
		await ctx.send(embed=e_urban)

	@commands.command()
	async def cat(self, ctx, cat_name:str = ''):
		await ctx.trigger_typing()
		cat_name = cat_name.lower()
		if self.cat_dirs is None or self.cat_json is None:
			try:
				self.cat_json = json.loads(f.open_url(self.cat_url+'/api/all'))
				self.cat_dirs = json.loads(f.open_url(self.cat_url+'/directories/'))
			except:
				await ctx.send(tt.w+'the cat api is currently offline!')
				return
		if (cat_name == 'list') or ((cat_name not in self.cat_dirs) and (cat_name != '')):
			await ctx.send(tt.i+f"list of valid cat directories: {', '.join(self.cat_dirs)}")
			return
		cat_image = await self.get_cat_url(cat_name)
		await ctx.send(cat_image)

	# i want it to be known this is the stupidest workaround i have ever made and the fact it works baffles me
	@commands.command(aliases=[
		'floppa','tommy','gloop','mish','spock','marley','lucas','nori','thomas','max','jim','gupitaro','mona','xena'
		])
	async def _cat_name(self, ctx):
		await ctx.invoke(self.bot.get_command('cat'), cat_name=ctx.invoked_with)

# 		========================

def setup(bot):
	bot.add_cog(fun(bot))