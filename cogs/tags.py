import discord
import json
import random 
import time, datetime
from pytz import timezone
from discord.ext import commands
from utils import checks
from utils.funcs import funcs
from data.messages import _t
import data.constants as tt

# 		========================

# 	'tag_name': {
# 		'content': 'tag content',
# 		'date':	'date and time of creation',
# 		'owner': tag owner ID,
# 	},
# }

reserved_tags = [
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

def is_visually_blank(text:str):
	characters = tt.whitespace_characters + tt.markdown_characters
	for character in characters:
		text = text.replace(character, '')
	if text == '':
		return True

class tags(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.load_db = funcs.load_db
		self.dump_db = funcs.dump_db
		self.check_for_db = funcs.check_for_db
		self.send_log = funcs.send_log
		self.log_prefix = "[TAGS]"
		self.tags_list = self.load_db(tt.tags_db)

# 		========================

	@commands.group(name = 'tag', aliases=['t'])
	@commands.guild_only()
	@commands.cooldown(1, 2, commands.BucketType.user)
	async def tag(self, ctx):
		if ctx.invoked_subcommand is None:
			if ctx.subcommand_passed is None:
				raise(commands.UserInputError)
			await ctx.invoke(self.bot.get_command('tag view'), tag_name=ctx.subcommand_passed)

	@tag.before_invoke
	async def tag_before_invoke(self, ctx):
		await ctx.trigger_typing()

	@tag.command(name = 'view')
	async def tag_view(self, ctx, tag_name:str):
		tag_name = tag_name.lower()
		if tag_name in reserved_tags:
			await ctx.send(_t.reserved)
			return
		if tag_name not in self.tags_list:
			await ctx.send(_t.does_not_exist.format(tag_name))
			return
		tag_content = self.tags_list[tag_name]['content'] 
		tag_content = tt.sanitize(tag_content)
		await ctx.send(tag_content)

	@tag.command(name = 'create', aliases=['c'])
	async def tag_create(self, ctx, tag_name:str, *, tag_content:str = ''):
		tag_name = tag_name.lower()
		if tag_name in reserved_tags:
			await ctx.send(_t.reserved)
			return
		if tag_name in self.tags_list: 
			await ctx.send(_t.already_exists.format(tag_name))
			return
		if (is_visually_blank(tag_name)) or (is_visually_blank(tag_content)):
			await ctx.send(_t.cannot_be_blank)
			return
		if ctx.message.attachments:
			for attachment in ctx.message.attachments:
				tag_content += ' '+attachment.url
		if tag_content == '':
			raise(commands.UserInputError)
			return
		if (len(tag_name) > 100) or (len(tag_content) > 1000):
			await ctx.send(_t.charlimit.format('(max of 100 for names and 1000 for contents)')) 
			return
		tag_content = tt.sanitize(tag_content)
		self.tags_list[tag_name] = {'content':tag_content, 'owner':ctx.author.id, 'date':tt.curtime()}
		self.dump_db(tt.tags_db, self.tags_list)
		await ctx.send(tt.y+f"created the tag \"{tag_name}\"!")
		await self.send_log(self, f"'{ctx.author.name}' created the tag '{tag_name}'", self.log_prefix)
				
	@tag.command(name = 'edit')
	async def tag_edit(self, ctx, tag_name:str, *, tag_content:str = ''):
		tag_name = tag_name.lower()
		if tag_name not in self.tags_list:
			await ctx.send(_t.does_not_exist.format(tag_name))
			return
		if self.tags_list[tag_name]['owner'] != ctx.author.id:
			await ctx.send(_t.not_owner)
			return
		if is_visually_blank(tag_content):
			await ctx.send(_t.cannot_be_blank)
			return
		if ctx.message.attachments:
			for attachment in ctx.message.attachments:
				tag_content += ' '+attachment.url
		if tag_content == '':
			raise(commands.UserInputError)
			return
		if len(tag_content) > 1000: 
			await ctx.send(_t.charlimit.format('(max of 1000 for tag contents)'))
			return
		tag_content = tt.sanitize(tag_content)
		self.tags_list[tag_name]['content'] = tag_content
		self.tags_list[tag_name]['date'] = f'{tt.curtime()} (edited)'
		self.dump_db(tt.tags_db, self.tags_list)
		await ctx.send(tt.y+f"updated the tag \"{tag_name}\"!")
		await self.send_log(self, f"'{ctx.author}' updated the tag '{tag_name}'", self.log_prefix)

	@tag.command(name = 'remove', aliases=['r'])
	async def tag_remove(self, ctx, tag_name:str):
		tag_name = tag_name.lower()
		if tag_name not in self.tags_list:
			await ctx.send(_t.does_not_exist.format(tag_name))
			return
		if self.tags_list[tag_name]['owner'] != ctx.author.id:
			await ctx.send(_t.not_owner)
			return
		del self.tags_list[tag_name]
		self.dump_db(tt.tags_db, self.tags_list)
		await ctx.send(tt.y+f"deleted the tag \"{tag_name}\"!")
		await self.send_log(self, f"'{ctx.author}' deleted the tag '{tag_name}'", self.log_prefix)

	@tag.command(name = 'transfer')
	async def tag_transfer(self, ctx, tag_name, user: discord.Member):
		tag_name = tag_name.lower()
		if tag_name not in self.tags_list:
			await ctx.send(_t.does_not_exist.format(tag_name))
			return
		if self.tags_list[tag_name]['owner'] != ctx.author.id:
			await ctx.send(_t.not_owner)
			return
		self.tags_list[tag_name]['owner'] = user.id
		self.tags_list[tag_name]['date'] = f'{tt.curtime()} (transferred)'
		self.dump_db(tt.tags_db, self.tags_list)
		await ctx.send(tt.y+f"ownership of tag \"{tag_name}\" has been transferred to **{user}**!")
		await self.send_log(self, f"'{ctx.author}' transferred the tag '{tag_name}' to '{user}'", self.log_prefix)

	@tag.command(name = 'forceedit', aliases=['fe'])
	@checks.is_admin()
	async def tag_force_edit(self, ctx, tag_name:str, *, tag_content:str = None):
		tag_name = tag_name.lower()
		if tag_name not in self.tags_list:
			await ctx.send(_t.does_not_exist.format(tag_name))
			return
		if is_visually_blank(tag_content):
			await ctx.send(_t.cannot_be_blank)
			return
		if ctx.message.attachments:
			for attachment in ctx.message.attachments:
				tag_content += ' '+attachment.url
		if tag_content == '':
			raise(commands.UserInputError)
			return
		tag_content = tt.sanitize(tag_content)
		self.tags_list[tag_name]['content'] = tag_content
		self.tags_list[tag_name]['date'] = f'{tt.curtime()} (edited)'
		self.dump_db(tt.tags_db, self.tags_list)
		await ctx.send(tt.y+f"tag \"{tag_name}\" forcefully updated!")
		await self.send_log(self, f"'{ctx.author}' forcefully updated the tag '{tag_name}'", self.log_prefix)

	@tag.command(name = 'forceremove', aliases=['fr'])
	@checks.is_admin()
	async def tag_force_remove(self, ctx, tag_name:str):
		tag_name = tag_name.lower()			
		if tag_name not in self.tags_list:
			await ctx.send(_t.does_not_exist.format(tag_name))
			return
		del self.tags_list[tag_name]
		self.dump_db(tt.tags_db, self.tags_list)
		await ctx.send(tt.y+f"tag \"{tag_name}\" was forcefully deleted!")
		await self.send_log(self, f"'{ctx.author}' forcefully deleted the tag '{tag_name}'", self.log_prefix)

	@tag.command(name = 'forcetransfer', aliases=['ft'])
	@checks.is_admin()
	async def tag_force_transfer(self, ctx, tag_name, user: discord.Member):
		tag_name = tag_name.lower()
		if tag_name not in self.tags_list:
			await ctx.send(_t.does_not_exist.format(tag_name))
			return
		self.tags_list[tag_name]['owner'] = user.id
		self.tags_list[tag_name]['date'] = f'{tt.curtime()} (transferred)'
		self.dump_db(tt.tags_db, self.tags_list)
		await ctx.send(tt.y+f"ownership of tag \"{tag_name}\" has been forcefully transferred to **{user}**!")
		await self.send_log(self, f"'{ctx.author}' forcefully transferred the tag '{tag_name}' to '{user}'", self.log_prefix)

	@tag.command(name = 'owner')
	async def tag_owner(self, ctx, tag_name:str):
		tag_name = tag_name.lower()		
		if tag_name not in self.tags_list:
			await ctx.send(_t.does_not_exist.format(tag_name))
			return
		if tag_name in reserved_tags:
			await ctx.send(_t.reserved)
			return
		user = self.bot.get_user(self.tags_list[tag_name]['owner'])
		await ctx.send(tt.i+f"tag \"{tag_name}\" is owned by **{user}** ({user.id})")

	@tag.command(name = 'random')
	async def tag_random(self, ctx):
		random_tag = random.choice(list(self.tags_list.keys()))
		await ctx.send(f"**`tag: {random_tag}`**\n{self.tags_list[random_tag]['content']}")

	@tag.command(name = 'list')
	async def tag_list(self, ctx, user: discord.Member = None):
		user = ctx.author if not user else user
		tags_num = 0
		for tag in self.tags_list:
			if self.tags_list[tag]['owner'] == user.id:
				tags_num += 1	
		if tags_num == 0:
			await ctx.send(tt.i+f"**{user.name}** does not own any tags!")
			return
		await ctx.send(tt.i+f"**{user}** owns **{tags_num}** tags:\n{tt.tags_list}/{str(user.id)}")

	@tag.command(name = 'listall')
	async def tag_listall(self, ctx):
		tags_num = 0
		for tag in self.tags_list: 
			tags_num += 1	
		await ctx.send(tt.i+f"there are **{tags_num}** tags in the database:\n{tt.tags_list}")

# 		========================

def setup(bot):
	bot.add_cog(tags(bot))