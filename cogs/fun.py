import discord
import urbandict
import json
import urllib
import random
import datetime
from urllib import request
from discord.ext import commands
import data.constants as tt

# 		========================

urban_api_url = "https://api.urbandictionary.com/v0"

class fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	async def send_log(self, log:str):
		log_msg = f"[{tt._t()}] [FUN] {log}"
		print(log_msg)
		await self.bot.get_channel(tt.logs).send(f"```{log_msg}```")

# 		========================

	@commands.command()
	async def say(self, ctx, *, message:str):
		try:
			message = tt.sanitize(message)
			await self.send_log(log = f"'{ctx.author}' in '{ctx.guild.name}' said '{message}'")
			await ctx.send(message)
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	async def urban(self, ctx, *, word:str):
		try:
			url_encoded_word = urllib.parse.quote(word)
			url = f"{urban_api_url}/define?term={url_encoded_word}"
			urban_json = request.urlopen(url).read().decode('utf8')
			urban_list = json.loads(urban_json)
			try:
				urban_dict = dict(random.choice(urban_list['list']))
			except:
				await ctx.send("⚠️ ⠀the provided word does not have any definitions!")
				return
			urban_word = tt.urban_sanitize(urban_dict['word'].upper())
			urban_definition = tt.urban_sanitize(urban_dict['definition'])
			urban_example = tt.urban_sanitize(urban_dict['example'])
			urban_date = datetime.datetime.strptime(urban_dict['written_on'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime(tt.time3)
			urban_msg = f'```fix\n    {urban_word}\n\n{urban_definition}\n\nEXAMPLE: {urban_example}\n\n[{urban_date}]```'
			await ctx.send(urban_msg)
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	# this uses a really bad urbandictionary package but its funny so im keeping it
	async def urbanshit(self, ctx, *, word:str):
		try:
			urb = urbandict.define(word)
			msg = f"```fix\n    {word.upper()}\n\n"
			msg += "{0}".format(urb[0]['def'].replace("\n", ""))
			msg += "\n\nEXAMPLE: {0}```".format(urb[0]['example'].replace("\n", ""))
			await ctx.send(msg)
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

# 		========================

def setup(bot):
	bot.add_cog(fun(bot))