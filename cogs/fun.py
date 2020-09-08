import discord
import json
import random
import urbandict
import time, datetime
import urllib, urllib.request
from discord.ext import commands
from utils import checks
from utils.funcs import funcs
import data.constants as tt

# 		========================

with open(tt.rhcooc_db) as rhcooc_list_json:
	rhcooc_list = json.load(rhcooc_list_json)

def urban_sanitize(text:str):
	text = text.replace("\n", " ").replace("\r", " ").replace("[", "").replace("]", "").replace("`", "\`")
	text = (text[:500] + f' ... (+{len(text) - 500})') if len(text) > 500 else text
	return text

class fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.load_db = funcs.load_db
		self.dump_db = funcs.dump_db
		self.send_log = funcs.send_log
		self.log_prefix = "[FUN] "

# 		========================

	@commands.command()
	async def say(self, ctx, *, message:str):
		await ctx.trigger_typing()
		try:
			message = tt.sanitize(message)
			await self.send_log(self, log = f"'{ctx.author}' in '{ctx.guild.name}' said '{message}'", prefix = self.log_prefix)
			await ctx.send(message)
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@checks.is_server_or_bot_admin()
	async def echo(self, ctx, channel:discord.TextChannel, *, message:str):
		try:
			message = tt.sanitize(message)
			await channel.send(message)
			await self.send_log(self, f"'{ctx.author}' in '{ctx.guild.name}' echoed '{message}' to '{channel}'", self.log_prefix)
			await ctx.message.add_reaction('✅')
		except Exception as e: 
			await ctx.send(tt.msg_e.format(e))

	@commands.command()
	async def urban(self, ctx, *, word:str):
		await ctx.trigger_typing()
		try:
			urban_list = json.loads(urllib.request.urlopen(f"https://api.urbandictionary.com/v0/define?term={urllib.parse.quote(word)}").read().decode('utf8'))
			if len(dict(urban_list)['list']) == 0:
				return await ctx.send("⚠️ ⠀the provided word does not have any definitions!")
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

	@commands.group(name = 'rhcooc')
	@commands.guild_only()
	@checks.is_in_guild([tt.srv['rhc'], tt.srv['test']])
	async def rhcooc(self, ctx):
		await ctx.trigger_typing()
		if ctx.invoked_subcommand is None:
			try:
				rhcooc_list = self.load_db(tt.rhcooc_db)
				await ctx.send(random.choice(rhcooc_list))
			except Exception as error:
				await ctx.send(tt.msg_e.format(error))

	@rhcooc.command(name = 'add')
	@checks.is_admin()
	async def rhcooc_add(self, ctx, *, rhcooc_url = None):
		rhcooc_list = self.load_db(tt.rhcooc_db)
		rhcooc_additions = []
		try:
			if rhcooc_url is not None:
				rhcooc_url = rhcooc_url.split(" ")
				rhcooc_additions.extend(rhcooc_url)
			if ctx.message.attachments:
				for attachment in ctx.message.attachments:
					rhcooc_additions.append(attachment.url)
			if not rhcooc_additions:
				return await ctx.send("⚠️ ⠀unable to get urls! (none provided)")
			for url in rhcooc_additions:
				rhcooc_list.append(url)
			self.dump_db(tt.rhcooc_db, rhcooc_list)
			await ctx.send(f"✅ ⠀added `{', '.join(rhcooc_additions)}` to rhcooc database!")
			await self.send_log(self, log = f"'{ctx.author}' added '{', '.join(rhcooc_additions)}' to the rhcooc database", prefix = self.log_prefix)
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	@rhcooc.command(name = 'remove')
	@checks.is_admin()
	async def rhcooc_remove(self, ctx, rhcooc_url:str):
		rhcooc_list = self.load_db(tt.rhcooc_db)
		try:
			rhcooc_list.remove(rhcooc_url)
			self.dump_db(tt.rhcooc_db, rhcooc_list)
			await ctx.send(f"✅ ⠀removed '{rhcooc_url}' from rhcooc database!")
			await self.send_log(self, log = f"'{ctx.author}' removed '{rhcooc_url}' from the rhcooc database", prefix = self.log_prefix)
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