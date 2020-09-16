import discord
import json
import random
import math
import urbandict
import time, datetime
import urllib, urllib.request
from discord.ext import commands
from utils import checks
from utils.funcs import funcs
import data.constants as tt

# 		========================

penis_leaderboard = {}

def penis_eqn(user_id:int): 
	return math.floor((100-int(str(user_id)[-2:]))/int(str(user_id)[:1]))

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
		self.log_prefix = "[FUN]"
		
		self.rhcooc_list = self.load_db(tt.rhcooc_db)

# 		========================

	@commands.command()
	async def say(self, ctx, *, message:str):
		await ctx.trigger_typing()
		try:
			message = tt.sanitize(message)
			await self.send_log(self, f"'{ctx.author}' in '{ctx.guild.name}' said '{message}'", self.log_prefix)
			await ctx.send(message)
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@checks.is_server_or_bot_admin()
	async def echo(self, ctx, channel:discord.TextChannel, *, message:str):
		await ctx.trigger_typing()
		try:
			message = tt.sanitize(message)
			await channel.send(message)
			await self.send_log(self, f"'{ctx.author}' echoed '{message}' from '{ctx.guild.name}' to '{channel}' ({channel.guild.name})", self.log_prefix)
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
	async def urbanshit(self, ctx, *, word:str):
		await ctx.trigger_typing()
		try:
			await ctx.send(f"```fix\n    {word.upper()}\n\n{urbandict.define(word)[0]['def']}\nEXAMPLE: {urbandict.define(word)[0]['example']}```")
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command() 
	@checks.is_admin()
	async def blackdude(self, ctx):
		blackdude_server = self.bot.get_guild(747195327530139759)
		for emoji in blackdude_server.emojis:
			await ctx.message.add_reaction(self.bot.get_emoji(emoji.id))

	@commands.command()
	async def penis(self, ctx, user:discord.User=None):
		await ctx.trigger_typing()
		user = ctx.author if not user else user
		try:
			await ctx.send(f"**{user.name}'s penis**:\n"+"8"+"="*penis_eqn(user.id)+"D")
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.group()
	@commands.guild_only()
	async def penisrank(self, ctx, ranking:str = 'top'):
		await ctx.trigger_typing()
		ranking = ranking.lower()
		penis_leaderboard = {}
		if (ranking != 'top') and (ranking != 'bottom'):
			raise(commands.UserInputError)
			return
		for user in ctx.guild.members:
			penis_leaderboard[f"{user.name}"] = penis_eqn(user.id)
		penis_leaderboard_num = 0
		sort_reverse = True
		if ranking == 'bottom':
			sort_reverse = False
		sorted_penis_leaderboard = sorted(penis_leaderboard.items(), key=lambda x: x[1], reverse=sort_reverse)[:10]
		penis_leaderboard_msg = f"**list of this guilds {ranking} ranking penises:**\n"
		for stupid in sorted_penis_leaderboard:
			penis_leaderboard_num += 1
			penis_leaderboard_msg += f"**{penis_leaderboard_num}. {stupid[0]}**: {stupid[1]}\n"
		await ctx.send(penis_leaderboard_msg)

	@commands.group(name = 'rhcooc')
	@commands.guild_only()
	@checks.is_in_guilds([tt.srv['rhc'], tt.srv['test']])
	async def rhcooc(self, ctx):
		await ctx.trigger_typing()
		if ctx.invoked_subcommand is None:
			try:
				await ctx.send(self.smart_random(self.rhcooc_list, 'rhcooc'))
			except Exception as error:
				await ctx.send(tt.msg_e.format(error))

	@rhcooc.command(name = 'add')
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
			await self.send_log(self, f"'{ctx.author}' added '{', '.join(rhcooc_additions)}' to the rhcooc database", self.log_prefix)
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	@rhcooc.command(name = 'remove')
	@checks.is_admin()
	async def rhcooc_remove(self, ctx, rhcooc_url:str):
		try:
			self.rhcooc_list.remove(rhcooc_url)
			self.dump_db(tt.rhcooc_db, self.rhcooc_list)
			await ctx.send(tt.y+f"removed '{rhcooc_url}' from rhcooc database!")
			await self.send_log(self, f"'{ctx.author}' removed '{rhcooc_url}' from the rhcooc database", self.log_prefix)
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	@rhcooc.command(name = 'list')
	async def rhcooc_listall(self, ctx):
		rhcooc_list = self.load_db(tt.rhcooc_db)
		rhcooc_num = 0
		for url in rhcooc_list: 
			rhcooc_num += 1	
		await ctx.send(f"ℹ️ ⠀there are **{rhcooc_num}** rhcooc images in the database:\n{tt.rhcooc_list}")

# 		========================

def setup(bot):
	bot.add_cog(fun(bot))