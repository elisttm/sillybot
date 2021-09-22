import discord, json, random, urllib, urllib.request, datetime
from discord.ext import commands
from a import checks
from a.funcs import f
import a.constants as tt

def urban_sanitize(text:str):
	return f.ctruncate(text.replace("\r", "").replace("\n\n", "\n").replace("\n\n", "\n").replace("[", "").replace("]", "").replace("`", "\`"), 1500)

class fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.cat_url = 'http://e.elisttm.space:7777/'
		self.cat_data = None

	def get_cat_data(self):
		try:
			self.cat_data = [json.loads(f.open_url(self.cat_url+'/api/all')), json.loads(f.open_url(self.cat_url+'/directories/'))]
			return True
		except:
			self.cat_data = None
			return False

	def get_cat_url(self, cat_name):
		if urllib.request.urlopen(self.cat_url).getcode() != 200 or self.cat_data == None and self.get_cat_data() == False:
			return None
		if not cat_name:
			cat_name = random.choice(self.cat_data[1])
		return f"{self.cat_url}/static/cat/{cat_name}/{f.smart_random(self.cat_data[0][cat_name], 'cat'+cat_name)}"

	@commands.command()
	async def say(self, ctx, *, message:str):
		f.log(f"{ctx.author} in '{ctx.guild.name}' used say '{message}'")
		await ctx.send(message)
		
	@commands.command()
	@checks.is_guild_admin()
	async def echo(self, ctx, channel:discord.TextChannel, *, message:str):
		f.log(f"{ctx.author} in '{ctx.guild.name}' to #{channel} {'('+channel.guild.name+')' if channel.guild.name != ctx.guild.name else ''} echoed '{message}'")
		await channel.send(message)
		await ctx.message.add_reaction(tt.e.check)

	@commands.command()
	async def urban(self, ctx, *, word:str):
		await ctx.trigger_typing()
		urban_list = json.loads(f.open_url('https://api.urbandictionary.com/v0/define?term='+urllib.parse.quote(word)))
		if len(dict(urban_list)['list']) == 0:
			await ctx.send(tt.w+"the provided word does not have any definitions!")
			return
		urban_dict = dict(random.choice(urban_list['list']))
		e_urban = discord.Embed(title=f"**{urban_sanitize(urban_dict['word']).upper()}**", url=urban_dict['permalink'], description=f"**definition**\n{urban_sanitize(urban_dict['definition'])}\n**example**\n{urban_sanitize(urban_dict['example'])}", color=tt.color.pink)
		e_urban.set_footer(text=f"{datetime.datetime.strptime(urban_dict['written_on'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%-m/%-d/%y')} {urban_dict['author']} | {tt.e.thumbsup}{urban_dict['thumbs_up']} {tt.e.thumbsdown}{urban_dict['thumbs_down']}")
		await ctx.send(embed=e_urban)

	@commands.command()
	async def cat(self, ctx, cat_name=None):
		await ctx.trigger_typing()
		if not self.cat_data and not self.get_cat_data:
			await ctx.send(tt.w+'the cat api is currently offline!')
			return
		if cat_name != None and cat_name.lower() not in self.cat_data[1]:
			await ctx.send(tt.i+f"list of valid cat directories: {', '.join(self.cat_data[1])}")
			return
		await ctx.send(await self.get_cat_url(cat_name.lower()))

	# i want it to be known this is the stupidest workaround i have ever made and the fact it works baffles me
	#@commands.command(aliases=[
	#	'floppa','tommy','gloop','mish','spock','marley','lucas','nori','thomas','max','jim','gupitaro','mona','xena'
	#	])
	#async def _cat_name(self, ctx):
	#	await ctx.invoke(self.bot.get_command('cat'), cat_name=ctx.invoked_with)

def setup(bot):
	bot.add_cog(fun(bot))
