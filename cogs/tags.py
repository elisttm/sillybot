import discord
from discord.ext import commands
from a import checks
from a.funcs import funcs
import a.constants as tt

# json database structure
# 	'tag_name': {
# 		'content': 'tag content',
# 		'date':	'date and time of creation',
# 		'owner': tag owner ID,
# 	},
# }

class m_():
	charlimit = tt.w+"too many characters! {}"
	does_not_exist = tt.w+"the tag \"{}\" does not exist!"
	already_exists = tt.x+"the tag \"{}\" already exists!"
	not_owner = tt.x+"you are not the owner of this tag!"
	reserved = tt.x+"that tag is reserved!"
	
reserved_tags = [
	'create',
	'remove', 'delete',
	'edit',
	'transfer',
	'owner', 
	'random',
	'list', 'listall',
	'forceedit', 'forceremove', 'forcetransfer',
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
		self.smart_random = funcs.smart_random
		self.load_db = funcs.load_db
		self.dump_db = funcs.dump_db
		self.send_log = funcs.send_log

		self.tags_list = self.load_db(tt.tags_db)

# 		========================

	@commands.group(name = 'tag', aliases=['t'])
	@commands.guild_only()
	@checks.is_tag_disabled()
	@commands.cooldown(1, 1, commands.BucketType.user)
	async def tag(self, ctx):
		if ctx.invoked_subcommand is None:
			if ctx.subcommand_passed is None:
				raise(commands.UserInputError)
			tag_name = await commands.clean_content(use_nicknames=False).convert(ctx, ctx.subcommand_passed)
			await ctx.invoke(self.bot.get_command('tag view'), tag_name=tag_name)

	@tag.before_invoke
	async def tag_before_invoke(self, ctx):
		await ctx.trigger_typing()

	@tag.command(name = 'view')
	@checks.is_tag_disabled()
	async def tag_view(self, ctx, tag_name:commands.clean_content(use_nicknames=False)):
		tag_name = tag_name.lower()
		if tag_name in reserved_tags:
			await ctx.send(m_.reserved)
			return
		if tag_name not in self.tags_list:
			await ctx.send(m_.does_not_exist.format(tag_name))
			return
		tag_content = self.tags_list[tag_name]['content'] 
		tag_content = tt.sanitize(tag_content)
		await ctx.send(tag_content)

	@tag.command(name = 'create', aliases=['c'])
	@checks.is_tag_disabled()
	async def tag_create(self, ctx, tag_name:commands.clean_content(use_nicknames=False), *, tag_content:str=''):
		tag_name = tag_name.lower()
		if tag_name in reserved_tags:
			await ctx.send(m_.reserved)
			return
		if tag_name in self.tags_list: 
			await ctx.send(m_.already_exists.format(tag_name))
			return
		if ctx.message.attachments:
			for attachment in ctx.message.attachments:
				tag_content += ' '+attachment.url
		elif (tag_content == '') or (tag_name == '') or (is_visually_blank(tag_name)) or (is_visually_blank(tag_content)):
			raise(commands.UserInputError)
			return
		if (len(tag_name) > 100) or (len(tag_content) > 1000):
			await ctx.send(m_.charlimit.format('(max 100 for names and 1000 for contents)')) 
			return
		tag_content = tt.sanitize(tag_content)
		self.tags_list[tag_name] = {'content':tag_content, 'owner':ctx.author.id, 'date':tt.curtime()}
		self.dump_db(tt.tags_db, self.tags_list)
		await ctx.send(tt.y+f"created the tag \"{tag_name}\"!")
		await self.send_log(self, f"'{ctx.author.name}' created the tag '{tag_name}'")
				
	@tag.command(name = 'edit')
	@checks.is_tag_disabled()
	async def tag_edit(self, ctx, tag_name:commands.clean_content(use_nicknames=False), *, tag_content:str=''):
		tag_name = tag_name.lower()
		if tag_name not in self.tags_list:
			await ctx.send(m_.does_not_exist.format(tag_name))
			return
		if self.tags_list[tag_name]['owner'] != ctx.author.id:
			await ctx.send(m_.not_owner)
			return
		if ctx.message.attachments:
			for attachment in ctx.message.attachments:
				tag_content += ' '+attachment.url
		elif (tag_content == '') or (tag_name == '') or (is_visually_blank(tag_name)) or (is_visually_blank(tag_content)):
			raise(commands.UserInputError)
			return
		if len(tag_content) > 1000: 
			await ctx.send(m_.charlimit.format('(max of 1000 for tag contents)'))
			return
		tag_content = tt.sanitize(tag_content)
		self.tags_list[tag_name]['content'] = tag_content
		self.tags_list[tag_name]['date'] = f'{tt.curtime()} (edited)'
		self.dump_db(tt.tags_db, self.tags_list)
		await ctx.send(tt.y+f"updated the tag \"{tag_name}\"!")
		await self.send_log(self, f"'{ctx.author}' updated the tag '{tag_name}'")

	@tag.command(name = 'delete', aliases=['d'])
	@checks.is_tag_disabled()
	async def tag_remove(self, ctx, tag_name:commands.clean_content(use_nicknames=False)):
		tag_name = tag_name.lower()
		if tag_name not in self.tags_list:
			await ctx.send(m_.does_not_exist.format(tag_name))
			return
		if self.tags_list[tag_name]['owner'] != ctx.author.id:
			await ctx.send(m_.not_owner)
			return
		del self.tags_list[tag_name]
		self.dump_db(tt.tags_db, self.tags_list)
		await ctx.send(tt.y+f"deleted the tag \"{tag_name}\"!")
		await self.send_log(self, f"'{ctx.author}' deleted the tag '{tag_name}'")

	@tag.command(name = 'transfer')
	@checks.is_tag_disabled()
	async def tag_transfer(self, ctx, tag_name:commands.clean_content(use_nicknames=False), user:discord.Member):
		tag_name = tag_name.lower()
		if tag_name not in self.tags_list:
			await ctx.send(m_.does_not_exist.format(tag_name))
			return
		if self.tags_list[tag_name]['owner'] != ctx.author.id:
			await ctx.send(m_.not_owner)
			return
		self.tags_list[tag_name]['owner'] = user.id
		self.tags_list[tag_name]['date'] = f'{tt.curtime()} (transferred)'
		self.dump_db(tt.tags_db, self.tags_list)
		await ctx.send(tt.y+f"ownership of tag \"{tag_name}\" has been transferred to **{user}**!")
		await self.send_log(self, f"'{ctx.author}' transferred the tag '{tag_name}' to '{user}'")

	@tag.command(name = 'forceedit', aliases=['fe'])
	@checks.is_tag_disabled()
	@checks.is_admin()
	async def tag_force_edit(self, ctx, tag_name:commands.clean_content(use_nicknames=False), *, tag_content:str=None):
		tag_name = tag_name.lower()
		if tag_name not in self.tags_list:
			await ctx.send(m_.does_not_exist.format(tag_name))
			return
		if ctx.message.attachments:
			for attachment in ctx.message.attachments:
				tag_content += ' '+attachment.url
		if (tag_content == '') or (tag_name == '') or (is_visually_blank(tag_name)) or (is_visually_blank(tag_content)):
			raise(commands.UserInputError)
			return
		tag_content = tt.sanitize(tag_content)
		self.tags_list[tag_name]['content'] = tag_content
		self.tags_list[tag_name]['date'] = f'{tt.curtime()} (edited)'
		self.dump_db(tt.tags_db, self.tags_list)
		await ctx.send(tt.y+f"tag \"{tag_name}\" forcefully updated!")
		await self.send_log(self, f"'{ctx.author}' forcefully updated the tag '{tag_name}'")

	@tag.command(name = 'forceremove', aliases=['fr'])
	@checks.is_tag_disabled()
	@checks.is_admin()
	async def tag_force_remove(self, ctx, tag_name:commands.clean_content(use_nicknames=False)):
		tag_name = tag_name.lower()			
		if tag_name not in self.tags_list:
			await ctx.send(m_.does_not_exist.format(tag_name))
			return
		del self.tags_list[tag_name]
		self.dump_db(tt.tags_db, self.tags_list)
		await ctx.send(tt.y+f"tag \"{tag_name}\" was forcefully deleted!")
		await self.send_log(self, f"'{ctx.author}' forcefully deleted the tag '{tag_name}'")

	@tag.command(name = 'forcetransfer', aliases=['ft'])
	@checks.is_tag_disabled()
	@checks.is_admin()
	async def tag_force_transfer(self, ctx, tag_name:commands.clean_content(use_nicknames=False), user:discord.Member):
		tag_name = tag_name.lower()
		if tag_name not in self.tags_list:
			await ctx.send(m_.does_not_exist.format(tag_name))
			return
		self.tags_list[tag_name]['owner'] = user.id
		self.tags_list[tag_name]['date'] = f'{tt.curtime()} (transferred)'
		self.dump_db(tt.tags_db, self.tags_list)
		await ctx.send(tt.y+f"ownership of tag \"{tag_name}\" has been forcefully transferred to **{user}**!")
		await self.send_log(self, f"'{ctx.author}' forcefully transferred the tag '{tag_name}' to '{user}'")

	@tag.command(name = 'owner')
	@checks.is_tag_disabled()
	async def tag_owner(self, ctx, tag_name:commands.clean_content(use_nicknames=False)):
		tag_name = tag_name.lower()		
		if tag_name not in self.tags_list:
			await ctx.send(m_.does_not_exist.format(tag_name))
			return
		if tag_name in reserved_tags:
			await ctx.send(m_.reserved)
			return
		user = self.bot.get_user(self.tags_list[tag_name]['owner'])
		await ctx.send(tt.i+f"tag \"{tag_name}\" is owned by **{user}** ({user.id})")

	@tag.command(name = 'random')
	@checks.is_tag_disabled()
	async def tag_random(self, ctx):
		random_tag = self.smart_random(list(self.tags_list.keys()), 'tag')
		await ctx.send(f"**`tag: {random_tag}`**\n{self.tags_list[random_tag]['content']}")

	@tag.command(name = 'list')
	@checks.is_tag_disabled()
	async def tag_list(self, ctx, user:discord.Member=None):
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
	@checks.is_tag_disabled()
	async def tag_listall(self, ctx):
		tags_num = 0
		for tag in self.tags_list: 
			tags_num += 1	
		await ctx.send(tt.i+f"there are **{tags_num}** public tags in the database:\n{tt.tags_list}")

# 		========================

def setup(bot):
	bot.add_cog(tags(bot))