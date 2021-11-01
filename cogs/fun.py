import discord, json, random, urllib, urllib.request, datetime
from discord.ext import commands
from a import checks
from a.funcs import f
import a.constants as tt

def urban_sanitize(text:str):
	text = text.replace("\r", "").replace("\n\n", "\n").replace("\n\n", "\n").replace("[", "").replace("]", "").replace("`", "\`")
	return (text[:1500] + f' ... (+{len(text)-1500})') if len(text) > 1500 else text

class fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

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
		urban_list = json.loads(f.open_url(f'https://api.urbandictionary.com/v0/define?term={urllib.parse.quote(word)}'))
		if not dict(urban_list)['list']:
			await ctx.send(tt.w+"the provided word does not have any definitions!")
			return
		urban_dict = dict(random.choice(urban_list['list']))
		e_urban = discord.Embed(title=f"**{urban_sanitize(urban_dict['word']).upper()}**", url=urban_dict['permalink'], description=f"**definition**\n{urban_sanitize(urban_dict['definition'])}\n**example**\n{urban_sanitize(urban_dict['example'])}", color=tt.dcolor, timestamp=datetime.datetime.strptime(urban_dict['written_on'], '%Y-%m-%dT%H:%M:%S.%fZ'))
		e_urban.set_footer(text=f"by {urban_dict['author']} | {tt.e.thumbsup}{urban_dict['thumbs_up']} {tt.e.thumbsdown}{urban_dict['thumbs_down']}")
		await ctx.send(embed=e_urban)

def setup(bot):
	bot.add_cog(fun(bot))
