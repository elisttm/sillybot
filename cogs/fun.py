import discord
import urbandict
import json
import urllib
import random
import pickle
import datetime
from urllib import request
from discord.ext import commands
from utils import checks
from utils.funcs import funcs
import data.constants as tt

# 		========================

def urban_sanitize(text:str):
	text = text.replace("\n", " ").replace("\r", " ").replace("[", "").replace("]", "").replace("`", "\`")
	text = (text[:500] + f' ... (+{len(text) - 500})') if len(text) > 500 else text
	return text

class fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
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
	async def urban(self, ctx, *, word:str):
		await ctx.trigger_typing()
		try:
			urban_list = json.loads(request.urlopen(f"https://api.urbandictionary.com/v0/define?term={urllib.parse.quote(word)}").read().decode('utf8'))
			if len(dict(urban_list)['list']) == 0:
				await ctx.send("⚠️ ⠀the provided word does not have any definitions!")
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
			urb = urbandict.define(word)
			msg = f"```fix\n    {word.upper()}\n\n"
			msg += "{0}".format(urb[0]['def'].replace("\n", ""))
			msg += "\n\nEXAMPLE: {0}```".format(urb[0]['example'].replace("\n", ""))
			await ctx.send(msg)
		except Exception as error: 
			await ctx.send(tt.msg_e.format(error))

	@commands.group(name = 'rhcooc')
	@commands.guild_only()
	@checks.is_in_guild([tt.srv['rhc'], tt.srv['test']])
	async def rhcooc(self, ctx):
		await ctx.trigger_typing()
		if ctx.invoked_subcommand is None:
			try:
				rhcooc_list = pickle.load(open(tt.rhcooc_pkl, "rb"))
				await ctx.send(random.choice(rhcooc_list))
			except Exception as error:
				await ctx.send(tt.msg_e.format(error))

	@rhcooc.command(name = 'add')
	@checks.is_admin()
	async def rhcooc_add(self, ctx, *, rhcooc_url = None):
		rhcooc_list = pickle.load(open(tt.rhcooc_pkl, "rb"))
		rhcooc_additions = []
		try:
			if rhcooc_url is not None:
				rhcooc_url = rhcooc_url.split(" ")
				rhcooc_additions.extend(rhcooc_url)
			if ctx.message.attachments:
				for attachment in ctx.message.attachments:
					rhcooc_additions.append(attachment.url)
			if not rhcooc_additions:
				await ctx.send("⚠️ ⠀unable to get urls! (none provided)")
				return
			for url in rhcooc_additions:
				rhcooc_list.append(url)
			pickle.dump(rhcooc_list, open(tt.rhcooc_pkl, "wb"))
			await ctx.send(f"✅ ⠀added `{', '.join(rhcooc_additions)}` to rhcooc database!")
			await self.send_log(self, log = f"'{ctx.author}' added '{', '.join(rhcooc_additions)}' to the rhcooc database", prefix = self.log_prefix)
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	@rhcooc.command(name = 'remove')
	@checks.is_admin()
	async def rhcooc_remove(self, ctx, rhcooc_url:str):
		rhcooc_list = pickle.load(open(tt.rhcooc_pkl, "rb"))
		try:
			rhcooc_list.remove(rhcooc_url)
			pickle.dump(rhcooc_list, open(tt.rhcooc_pkl, "wb"))
			await ctx.send(f"✅ ⠀removed '{rhcooc_url}' from rhcooc database!")
			await self.send_log(self, log = f"'{ctx.author}' removed '{rhcooc_url}' from the rhcooc database", prefix = self.log_prefix)
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	@rhcooc.command(name = 'list')
	async def rhcooc_list(self, ctx):
		rhcooc_list = pickle.load(open(tt.rhcooc_pkl, "rb"))
		rhcooc_num = 0
		for image in rhcooc_list: 
			rhcooc_num += 1	
		await ctx.send(f"ℹ️ ⠀there are **{rhcooc_num}** rhcooc images in the database:\n{tt.rhcooc_list}")

# 		========================

def setup(bot):
	bot.add_cog(fun(bot))