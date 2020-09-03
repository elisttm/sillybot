import discord
import pickle
import random 
import asyncio
import time, datetime
from pytz import timezone
from discord.ext import commands
from utils import checks
from utils.funcs import funcs
import data.constants as tt

# 		========================

# tags_list = {
# 	'tag name': {
# 		'content': 'tag content',
# 		'date':	'MM/DD/YY hh/mm/ss AM/PM (edited/transferred)',
# 		'owner': tag owner ID (int),
# 	},
# }

#pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
tags_list = pickle.load(open(tt.tags_pkl, "rb"))

reserved_args = [
	'create',
	'remove',
	'edit',
	'transfer',
	'forceedit',
	'forceremove',
	'forcetransfer',
	'owner', 
	'random',
	'list',
	'listall',
	'c', 'r', 'fe', 'fr', 'ft',

	'@everyone', '@here',
]

class tags(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.send_log = funcs.send_log
		self.log_prefix = "[TAGS] "

# 		========================

	@commands.group(name = 'tag', aliases=['t'])
	@commands.guild_only()
	@commands.cooldown(1, 2)
	async def tag(self, ctx):
		if ctx.invoked_subcommand is None:
			if ctx.subcommand_passed is None:
				await ctx.send("⚠️ ⠀invalid tag/subcommand provided!")
				return
			tag_name = ctx.subcommand_passed.lower()
			tags_list = pickle.load(open(tt.tags_pkl, "rb"))
			if tag_name not in reserved_args:
				if tag_name not in tags_list:
					await ctx.send(f"⚠️ ⠀tag \"{tag_name}\" does not exist!")
					return
				tag_content = tags_list[tag_name]['content'] 
				tag_content = tt.sanitize(tag_content)
				await ctx.send(tag_content)

	@tag.before_invoke
	async def tag_before_invoke(self, ctx):
		#await self.bot.wait_for(self.bot.get_command('tag'))
		await ctx.trigger_typing()

	@tag.command(name = 'create', aliases=['c'])
	@commands.cooldown(1, 2)
	async def tag_create(self, ctx, tag_name:str, *, tag_content:str):
		tags_list = pickle.load(open(tt.tags_pkl, "rb"))
		tag_name = tag_name.lower()
		if tag_name in tags_list: 
			await ctx.send(f"❌ ⠀tag \"{tag_name}\" already exists!")
			return
		if (len(tag_name) > 100) or (len(tag_content) > 1000):
			await ctx.send("⚠️ ⠀too many characters! (up to 100 for tag names and up to 1000 for tag contents)") 
			return
		tag_content = tt.sanitize(tag_content)
		tags_list[tag_name] = {'content':'', 'owner':0, 'date':''}
		tags_list[tag_name]['content'] = tag_content
		tags_list[tag_name]['owner'] = ctx.author.id
		tags_list[tag_name]['date'] = tt.curtime()
		pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
		await ctx.send(f"✅ ⠀tag \"{tag_name}\" created!")
		await self.send_log(self, log = f"'{ctx.author.name}' created the tag '{tag_name}'", prefix = self.log_prefix)
				
	@tag.command(name = 'edit')
	@commands.cooldown(1, 2)
	async def tag_edit(self, ctx, tag_name:str, *, tag_content:str):
		tags_list = pickle.load(open(tt.tags_pkl, "rb"))
		tag_name = tag_name.lower()
		if tag_name not in tags_list:
			await ctx.send(f"⚠️ ⠀tag \"{tag_name}\" does not exist!")
			return
		if tags_list[tag_name]['owner'] != ctx.author.id:
			await ctx.send("❌ ⠀you are not the owner of this tag!")
			return
		if len(tag_content) > 1000: 
			await ctx.send("⚠️ ⠀too many characters! (up to 1000 for tag contents)")
			return
		tag_content = tt.sanitize(tag_content)
		tags_list[tag_name]['content'] = tag_content
		tags_list[tag_name]['date'] = f'{tt.curtime()} (edited)'
		pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
		await ctx.send(f"✅ ⠀tag \"{tag_name}\" updated!")
		await self.send_log(self, log = f"'{ctx.author}' updated the tag '{tag_name}'", prefix = self.log_prefix)

	@tag.command(name = 'remove', aliases=['r'])
	@commands.cooldown(1, 2)
	async def tag_remove(self, ctx, tag_name:str):
		tags_list = pickle.load(open(tt.tags_pkl, "rb"))
		tag_name = tag_name.lower()
		if tag_name not in tags_list:
			await ctx.send(f"⚠️ ⠀tag \"{tag_name}\" does not exist!")
			return
		if tags_list[tag_name]['owner'] != ctx.author.id:
			await ctx.send("❌ ⠀you are not the owner of this tag!")
			return
		del tags_list[tag_name]
		pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
		await ctx.send(f"✅ ⠀tag \"{tag_name}\" deleted!")
		await self.send_log(self, log = f"'{ctx.author}' deleted the tag '{tag_name}'", prefix = self.log_prefix)

	@tag.command(name = 'transfer')
	@commands.cooldown(1, 2)
	async def tag_transfer(self, ctx, tag_name, user: discord.Member):
		tags_list = pickle.load(open(tt.tags_pkl, "rb"))
		tag_name = tag_name.lower()
		if tag_name not in tags_list:
			await ctx.send(f"⚠️ ⠀tag \"{tag_name}\" does not exist!")
			return
		if tags_list[tag_name]['owner'] != ctx.author.id:
			await ctx.send("❌ ⠀you are not the owner of this tag!")
			return
		tags_list[tag_name]['owner'] = user.id
		tags_list[tag_name]['date'] = f'{tt.curtime()} (transferred)'
		pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
		await ctx.send(f"✅ ⠀ownership of tag \"{tag_name}\" has been transferred to **{user}**!")
		await self.send_log(self, log = f"'{ctx.author}' transferred the tag '{tag_name}' to '{user}'", prefix = self.log_prefix)

	@tag.command(name = 'forceedit', aliases=['fe'])
	@checks.is_admin()
	async def tag_force_edit(self, ctx, tag_name:str, *, tag_content:str):
		tags_list = pickle.load(open(tt.tags_pkl, "rb"))
		tag_name = tag_name.lower()
		if tag_name not in tags_list:
			await ctx.send(f"⚠️ ⠀tag \"{tag_name}\" does not exist!")
			return
		tag_content = tt.sanitize(tag_content)
		tags_list[tag_name]['content'] = tag_content
		tags_list[tag_name]['date'] = f'{tt.curtime()} (edited)'
		pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
		await ctx.send(f"✅ ⠀tag \"{tag_name}\" forcefully updated!")
		await self.send_log(self, log = f"'{ctx.author}' forcefully updated the tag '{tag_name}'", prefix = self.log_prefix)

	@tag.command(name = 'forceremove', aliases=['fr'])
	@checks.is_admin()
	async def tag_force_remove(self, ctx, tag_name:str):
		tags_list = pickle.load(open(tt.tags_pkl, "rb"))
		tag_name = tag_name.lower()			
		if tag_name not in tags_list:
			await ctx.send(f"⚠️ ⠀tag \"{tag_name}\" does not exist!")
			return
		del tags_list[tag_name]
		pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
		await ctx.send(f"✅ ⠀tag \"{tag_name}\" was forcefully deleted!")
		await self.send_log(self, log = f"'{ctx.author}' forcefully deleted the tag '{tag_name}'", prefix = self.log_prefix)

	@tag.command(name = 'forcetransfer', aliases=['ft'])
	@checks.is_admin()
	async def tag_force_transfer(self, ctx, tag_name, user: discord.Member):
		tags_list = pickle.load(open(tt.tags_pkl, "rb"))
		tag_name = tag_name.lower()
		if tag_name not in tags_list:
			await ctx.send(f"⚠️ ⠀tag \"{tag_name}\" does not exist!")
			return
		tags_list[tag_name]['owner'] = user.id
		tags_list[tag_name]['date'] = f'{tt.curtime()} (transferred)'
		pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
		await ctx.send(f"✅ ⠀ownership of tag \"{tag_name}\" has been forcefully transferred to **{user}**!")
		await self.send_log(self, log = f"'{ctx.author}' forcefully transferred the tag '{tag_name}' to '{user}'", prefix = self.log_prefix)

	@tag.command(name = 'owner')
	async def tag_owner(self, ctx, tag_name:str):
		tags_list = pickle.load(open(tt.tags_pkl, "rb"))
		tag_name = tag_name.lower()		
		if tag_name not in tags_list:
			await ctx.send(f"⚠️ ⠀tag \"{tag_name}\" does not exist!")
			return
		if tag_name in reserved_args:
			await ctx.send("⚠️ ⠀invalid or reserved tag given!")
			return
		user = self.bot.get_user(tags_list[tag_name]['owner'])
		await ctx.send(f"ℹ️ ⠀tag \"{tag_name}\" is owned by **{user}** ({user.id})")

	@tag.command(name = 'random')
	async def tag_random(self, ctx):		
		tags_list = pickle.load(open(tt.tags_pkl, "rb"))
		random_tag = random.choice(list(tags_list.keys()))
		await ctx.send(f"**`tag: {random_tag}`**\n{tags_list[random_tag]['content']}")

	@tag.command(name = 'list')
	async def tag_list(self, ctx, user: discord.Member = None):
		tags_list = pickle.load(open(tt.tags_pkl, "rb"))
		user = ctx.author if not user else user
		tags_num = 0
		for tag in tags_list:
			if tags_list[tag]['owner'] == user.id:
				tags_num += 1	
		if tags_num == 0:
			await ctx.send(f"ℹ️ ⠀**{user.name}** does not own any tags!")
			return
		await ctx.send(f"ℹ️ ⠀**{user}** owns **{tags_num}** tags:\n{tt.tags_list}/{str(user.id)}")

	@tag.command(name = 'listall')
	async def tag_listall(self, ctx):
		tags_list = pickle.load(open(tt.tags_pkl, "rb"))
		tags_num = 0
		for tag in tags_list: 
			tags_num += 1	
		await ctx.send(f"ℹ️ ⠀there are **{tags_num}** tags in the database:\n{tt.tags_list}")

# 		========================

def setup(bot):
	bot.add_cog(tags(bot))