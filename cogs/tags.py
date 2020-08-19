import discord
import pickle
import random
import time, datetime, pytz
from pytz import timezone
from discord.ext import commands
import data.constants as tt

# 		========================

# tags_list = {
# 	'tag': {
# 		'content': 'test',
# 		'date':	'yeah',
# 		'owner': 0,
#  },
# }

#pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
tags_list = pickle.load(open(tt.tags_pkl, "rb"))

reserved_args = ['owner', 'create', 'c', 'add', 'delete', 'remove', 'r', 'edit', 'random', '@everyone', '@here',]

tag_alreadyexists = "❌ ⠀tag **\"{}\"** already exists!"
tag_doesnotexist = "⚠️ ⠀tag **\"{}\"** does not exist!"
tag_invalidargs = "⚠️ ⠀invalid tag/subcommand provided!"
tag_invalidtag = "⚠️ ⠀invalid or reserved tag given!"
tag_charlimit = "⚠️ ⠀too many characters! ({})"
tag_notowner = "❌ ⠀you are not the owner of this tag!"

charlimit_content = "up to 1000 for tag contents"
charlimit_name = "up to 100 for tag names"

def curtime():
	return datetime.datetime.now(timezone('US/Eastern')).strftime('%m/%d/%y %I:%M:%S %p')

class tags(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

# 		========================

	@commands.group(aliases=['t'])
	#@commands.cooldown(1, 2)
	async def tag(self, ctx):
		if ctx.invoked_subcommand is None:
			if ctx.subcommand_passed is None:
				await ctx.send(tag_invalidargs)
			else:
				tag_name = ctx.subcommand_passed.lower()
				if tag_name not in reserved_args:
					if tag_name in tags_list:
						tag_content = tags_list[tag_name]['content'] 
						tag_content = tt.sanitize(text = tag_content)
						await ctx.send(tag_content)
					else: 
						await ctx.send(tag_doesnotexist.format(tag_name))

	@tag.before_invoke
	async def taglist_load(self, ctx):
		await ctx.trigger_typing()
		tags_list = pickle.load(open(tt.tags_pkl, "rb"))

	@tag.command(aliases=['c', 'add'])
	@commands.cooldown(1, 2)
	async def create(self, ctx, tag_name:str, tag_content:str):
		tag_name = tag_name.lower()
		if tag_name in tags_list: 
			await ctx.send(tag_alreadyexists.format(tag_name))
		else:
			if len(tag_name) > 100:
				await ctx.send(tag_charlimit.format(charlimit_name)) 
			elif len(tag_content) > 999: 
				await ctx.send(tag_charlimit.format(charlimit_content))
			else:
				tag_content = tt.sanitize(text = tag_content)
				tags_list[tag_name] = {'content':'', 'owner':0, 'date':''}
				tags_list[tag_name]['content'] = tag_content
				tags_list[tag_name]['owner'] = ctx.author.id
				tags_list[tag_name]['date'] = curtime()
				pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
				await ctx.send(f"✅ ⠀tag **\"{tag_name}\"** created!")

	@tag.command(aliases=['r', 'remove'])
	@commands.cooldown(1, 2)
	async def delete(self, ctx, tag_name:str):
		tag_name = tag_name.lower()
		if tag_name in tags_list:
			if tags_list[tag_name]['owner'] == ctx.author.id:
				del tags_list[tag_name]
				pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
				await ctx.send(f"✅ ⠀tag **\"{tag_name}\"** deleted!")
			else: 
				await ctx.send(tag_notowner)
		else: 
			await ctx.send(tag_doesnotexist.format(tag_name))

	@tag.command()
	@commands.cooldown(1, 2)
	async def edit(self, ctx, tag_name:str, tag_content:str):
		tag_name = tag_name.lower()
		if tag_name in tags_list:
			if tags_list[tag_name]['owner'] == ctx.author.id:
				if len(tag_content) > 999: 
					await ctx.send(tag_charlimit.format(charlimit_content))
				else:
					tag_content = tt.sanitize(text = tag_content)
					tags_list[tag_name]['content'] = tag_content
					tags_list[tag_name]['date'] = f'{curtime()} (edited)'
					pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
					await ctx.send(f"✅ ⠀tag **\"{tag_name}\"** updated!")
			else: 
				await ctx.send(tag_notowner)
		else: 
			await ctx.send(tag_doesnotexist.format(tag_name))
				
	@tag.command()
	@commands.cooldown(1, 2)
	async def transfer(self, ctx, tag_name, user: discord.Member):
		if tag_name in tags_list:
			if tags_list[tag_name]['owner'] == ctx.author.id:
				tags_list[tag_name]['owner'] = user.id
				tags_list[tag_name]['date'] = f'{curtime()} (transferred)'
				pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
				await ctx.send(f"✅ ⠀tag **\"{tag_name}\"** has been given to **{user}**!")
			else: 
				await ctx.send(tag_notowner)
		else: 
			await ctx.send(tag_doesnotexist.format(tag_name))

	@tag.command()
	async def random(self, ctx):
		random_tag = random.choice(list(tags_list.keys()))
		await ctx.send(f"**`tag: {random_tag}`**\n{tags_list[random_tag]['content']}")

	@tag.command()
	async def owner(self, ctx, tag_name:str):
		if tag_name in tags_list:
			if tag_name not in reserved_args:
				user = self.bot.get_user(tags_list[tag_name]['owner'])
				await ctx.send(f"ℹ️ ⠀tag **\"{tag_name}\"** is owned by **{user}** ({user.id})")
			else:
				await ctx.send(tag_invalidtag)
		else: 
			await ctx.send(tag_doesnotexist.format(tag_name))

	@tag.command()
	async def list(self, ctx, user: discord.Member = None):
		user = ctx.author if not user else user
		tags_num = 0
		for tag in tags_list:
			if tags_list[tag]['owner'] == user.id:
				tags_num += 1	
		if tags_num == 0:
			await ctx.send(f"ℹ️ ⠀**{user.name}** does not own any tags!")
		else:
			user_tags_link = tt.taglist + "?search=" + str(user.id)
			list_tags_msg = f"ℹ️ ⠀**{user}** owns **{tags_num}** tags:\n{user_tags_link}"
			await ctx.send(list_tags_msg)

# 		========================

def setup(bot):
	bot.add_cog(tags(bot))