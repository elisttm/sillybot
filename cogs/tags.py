import discord
import pickle
import random 
import time, datetime
from pytz import timezone
from discord.ext import commands
import data.constants as tt

# 		========================

# tags_list = {
# 	'tag': {
# 		'content': 'test',
# 		'date':	'yeah',
# 		'owner': 0,
# 	},
# }

#pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
tags_list = pickle.load(open(tt.tags_pkl, "rb"))

reserved_args = [
	'create', 'c', 'remove', 'r', 'edit', 'transfer', 'owner', 'random', 'forceedit', 'fe', 'forceremove', 'fr', 'forcetransfer', 'ft',
	'@everyone', '@here',
]

def curtime():
	return datetime.datetime.now(timezone('US/Eastern')).strftime('%m/%d/%y %I:%M:%S %p')

class tags(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def is_admin(ctx):
		return ctx.author.id in tt.admins

	async def send_log(self, log:str):
		log_msg = f"[{tt._t()}] [TAGS] {log}"
		print(log_msg)
		await self.bot.get_channel(tt.logs).send(f"```{log_msg}```")

# 		========================

	@commands.group(aliases=['t'])
	@commands.guild_only()
	@commands.cooldown(1, 2)
	async def tag(self, ctx):
		if ctx.invoked_subcommand is None:
			if ctx.subcommand_passed is None:
				await ctx.send("⚠️ ⠀invalid tag/subcommand provided!")
			else:
				tag_name = ctx.subcommand_passed.lower()
				tags_list = pickle.load(open(tt.tags_pkl, "rb"))
				if tag_name not in reserved_args:
					if tag_name in tags_list:
						tag_content = tags_list[tag_name]['content'] 
						tag_content = tt.sanitize(text = tag_content)
						await ctx.send(tag_content)
					else: 
						await ctx.send(f"⚠️ ⠀tag \"{tag_name}\" does not exist!")

	@tag.before_invoke
	async def taglist_load(self, ctx):
		await ctx.trigger_typing()

	@tag.command(aliases=['c'])
	@commands.cooldown(1, 2)
	async def create(self, ctx, tag_name:str, *, tag_content:str):
		tags_list = pickle.load(open(tt.tags_pkl, "rb"))
		tag_name = tag_name.lower()
		if tag_name in tags_list: 
			await ctx.send(f"❌ ⠀tag \"{tag_name}\" already exists!")
		else:
			if len(tag_name) > 100:
				await ctx.send("⚠️ ⠀too many characters! (up to 1000 for tag contents)") 
			elif len(tag_content) > 999: 
				await ctx.send("⚠️ ⠀too many characters! (up to 100 for tag names)")
			else:
				tag_content = tt.sanitize(text = tag_content)
				tags_list[tag_name] = {'content':'', 'owner':0, 'date':''}
				tags_list[tag_name]['content'] = tag_content
				tags_list[tag_name]['owner'] = ctx.author.id
				tags_list[tag_name]['date'] = curtime()
				pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
				await ctx.send(f"✅ ⠀tag \"{tag_name}\" created!")
				await self.send_log(log = f"'{ctx.author.name}' created the tag '{tag_name}'")
				
	@tag.command()
	@commands.cooldown(1, 2)
	async def edit(self, ctx, tag_name:str, *, tag_content:str):
		tags_list = pickle.load(open(tt.tags_pkl, "rb"))
		tag_name = tag_name.lower()
		if tag_name in tags_list:
			if tags_list[tag_name]['owner'] == ctx.author.id:
				if len(tag_content) > 999: 
					await ctx.send("⚠️ ⠀too many characters! (up to 1000 for tag contents)")
				else:
					tag_content = tt.sanitize(text = tag_content)
					tags_list[tag_name]['content'] = tag_content
					tags_list[tag_name]['date'] = f'{curtime()} (edited)'
					pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
					await ctx.send(f"✅ ⠀tag \"{tag_name}\" updated!")
					await self.send_log(log = f"'{ctx.author}' updated the tag '{tag_name}'")
			else: 
				await ctx.send("❌ ⠀you are not the owner of this tag!")
		else: 
			await ctx.send(f"⚠️ ⠀tag \"{tag_name}\" does not exist!")

	@tag.command(aliases=['r'])
	@commands.cooldown(1, 2)
	async def remove(self, ctx, tag_name:str):
		tags_list = pickle.load(open(tt.tags_pkl, "rb"))
		tag_name = tag_name.lower()
		if tag_name in tags_list:
			if tags_list[tag_name]['owner'] == ctx.author.id:
				del tags_list[tag_name]
				pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
				await ctx.send(f"✅ ⠀tag \"{tag_name}\" deleted!")
				await self.send_log(log = f"'{ctx.author}' deleted the tag '{tag_name}'")
			else: 
				await ctx.send("❌ ⠀you are not the owner of this tag!")
		else: 
			await ctx.send(f"⚠️ ⠀tag \"{tag_name}\" does not exist!")

	@tag.command()
	@commands.cooldown(1, 2)
	async def transfer(self, ctx, tag_name, user: discord.Member):
		tags_list = pickle.load(open(tt.tags_pkl, "rb"))
		tag_name = tag_name.lower()
		if tag_name in tags_list:
			if tags_list[tag_name]['owner'] == ctx.author.id:
				tags_list[tag_name]['owner'] = user.id
				tags_list[tag_name]['date'] = f'{curtime()} (transferred)'
				pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
				await ctx.send(f"✅ ⠀ownership of tag \"{tag_name}\" has been transferred to **{user}**!")
				await self.send_log(log = f"'{ctx.author}' transferred the tag '{tag_name}' to '{user}'")
			else: 
				await ctx.send("❌ ⠀you are not the owner of this tag!")
		else: 
			await ctx.send(f"⚠️ ⠀tag \"{tag_name}\" does not exist!")

	@tag.command()
	async def random(self, ctx):		
		tags_list = pickle.load(open(tt.tags_pkl, "rb"))
		random_tag = random.choice(list(tags_list.keys()))
		await ctx.send(f"**`tag: {random_tag}`**\n{tags_list[random_tag]['content']}")

	@tag.command()
	async def owner(self, ctx, tag_name:str):
		tags_list = pickle.load(open(tt.tags_pkl, "rb"))
		tag_name = tag_name.lower()		
		if tag_name in tags_list:
			if tag_name not in reserved_args:
				user = self.bot.get_user(tags_list[tag_name]['owner'])
				await ctx.send(f"ℹ️ ⠀tag \"{tag_name}\" is owned by **{user}** ({user.id})")
			else:
				await ctx.send("⚠️ ⠀invalid or reserved tag given!")
		else: 
			await ctx.send(f"⚠️ ⠀tag \"{tag_name}\" does not exist!")

	@tag.command()
	@commands.check(is_admin)
	async def forceedit(self, ctx, tag_name:str, *, tag_content:str):
		tags_list = pickle.load(open(tt.tags_pkl, "rb"))
		tag_name = tag_name.lower()
		if tag_name in tags_list:
			tag_content = tt.sanitize(text = tag_content)
			tags_list[tag_name]['content'] = tag_content
			tags_list[tag_name]['date'] = f'{curtime()} (edited)'
			pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
			await ctx.send(f"✅ ⠀tag \"{tag_name}\" forcefully updated!")
			await self.send_log(log = f"'{ctx.author}' forcefully updated the tag '{tag_name}'")
		else: 
			await ctx.send(f"⚠️ ⠀tag \"{tag_name}\" does not exist!")

	@tag.command(aliases=['fr'])
	@commands.check(is_admin)
	async def forceremove(self, ctx, tag_name:str):
		tags_list = pickle.load(open(tt.tags_pkl, "rb"))
		tag_name = tag_name.lower()			
		if tag_name in tags_list:
			del tags_list[tag_name]
			pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
			await ctx.send(f"✅ ⠀tag \"{tag_name}\" was forcefully deleted!")
			await self.send_log(log = f"'{ctx.author}' forcefully deleted the tag '{tag_name}'")
		else: 
			await ctx.send(f"⚠️ ⠀tag \"{tag_name}\" does not exist!")

	@tag.command(aliases=['ft'])
	@commands.check(is_admin)
	async def forcetransfer(self, ctx, tag_name, user: discord.Member):
		tags_list = pickle.load(open(tt.tags_pkl, "rb"))
		tag_name = tag_name.lower()
		if tag_name in tags_list:
			tags_list[tag_name]['owner'] = user.id
			tags_list[tag_name]['date'] = f'{curtime()} (transferred)'
			pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
			await ctx.send(f"✅ ⠀ownership of tag \"{tag_name}\" has been forcefully transferred to **{user}**!")
			await self.send_log(log = f"'{ctx.author}' forcefully transferred the tag '{tag_name}' to '{user}'")
		else: 
			await ctx.send(f"⚠️ ⠀tag \"{tag_name}\" does not exist!")

	@tag.command()
	async def list(self, ctx, user: discord.Member = None):
		tags_list = pickle.load(open(tt.tags_pkl, "rb"))
		user = ctx.author if not user else user
		tags_num = 0
		for tag in tags_list:
			if tags_list[tag]['owner'] == user.id:
				tags_num += 1	
		if tags_num == 0:
			await ctx.send(f"ℹ️ ⠀**{user.name}** does not own any tags!")
		else:
			user_tags_link = tt.tags_list + "?search=" + str(user.id)
			list_tags_msg = f"ℹ️ ⠀**{user}** owns **{tags_num}** tags:\n{user_tags_link}"
			await ctx.send(list_tags_msg)

	@tag.command()
	async def listall(self, ctx):
		tags_list = pickle.load(open(tt.tags_pkl, "rb"))
		tags_num = 0
		for tag in tags_list: 
			tags_num += 1	
		list_tags_msg = f"ℹ️ ⠀there are **{tags_num}** tags in the database:\n{tt.tags_list}"
		await ctx.send(list_tags_msg)

# 		========================

def setup(bot):
	bot.add_cog(tags(bot))