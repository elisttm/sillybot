import discord, re
from discord.ext import commands
from a import checks
from a.funcs import f
import a.constants as tt

def tlog(text): f.log(text, '[TAGS]')
def tag_update(tag, content): f.data_update(tt.yeah, 'tags', tag, content, 'set')
def tag_delete(tag): f.data_remove(tt.yeah, 'tags', tag)
tag_list = f.data(tt.yeah, 'tags')

class tags(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def tname(self, tag):
		return tag.lower().replace('.','')

	async def tag_check(self, tag_name, tag_list, cmd, channel, author):
		if tag_name in ['create','delete','edit','transfer','owner','random','list','listall','forceedit','forceremove','forcetransfer','c','fe','fr','ft']:
			await channel.send(tt.x+"this tag is reserved!")
			return False
		if cmd not in ['create','c'] and tag_name not in tag_list:
			await channel.send(tt.w+f"the tag '{tag_name}' does not exist!")
			return False
		elif cmd in ['create','c'] and tag_name in tag_list:
			await channel.send(tt.x+f"the tag '{tag_name}' already exists!")
			return False
		if cmd in ['delete','edit','transfer'] and tag_list[tag_name]['owner'] != author:
			await channel.send(tt.x+"you are not the owner of this tag!")
			return False
		return True

	async def manage_content(self, tag_name, tag_content, attachments, channel):
		if attachments:
			tag_content += ' '+attachments[0].url
		elif f.is_visually_blank(tag_name) or f.is_visually_blank(tag_content):
			raise(commands.UserInputError)
			return False
		if not re.match("^[a-z0-9]*$", tag_name):
			await channel.send(tt.x+"tag names cannot have special characters!")
			return False
		if len(tag_name) > 100:
			await channel.send(tt.x+"too many characters! (tag names can be a maximum of 100 characters)")
			return False
		if len(tag_content) > 1000:
			await channel.send(tt.x+"too many characters! (tag contents can be a maximum of 1000 characters)")
			return False
		return tag_content.replace('@here','@\u200bhere').replace('@everyone','@\u200beveryone')

# 		========================

	@commands.group(name='tag', aliases=['t'])
	@commands.guild_only()
	@checks.is_tag_disabled()
	@commands.cooldown(1, 1, commands.BucketType.user)
	async def tag(self, ctx):
		if ctx.invoked_subcommand is None:
			if ctx.subcommand_passed is None:
				raise(commands.UserInputError)
			await ctx.invoke(self.bot.get_command('tag view'), tag_name=await commands.clean_content(use_nicknames=False).convert(ctx, ctx.subcommand_passed))

	@tag.before_invoke
	async def tag_before_invoke(self, ctx):
		await ctx.trigger_typing()

	@tag.command(name='view')
	@checks.is_tag_disabled()
	async def tag_view(self, ctx, tag_name:commands.clean_content(use_nicknames=False)):
		tag = self.tname(tag_name)
		if not await self.tag_check(tag, tag_list, ctx.command.name, ctx.channel, ctx.message.author.id):
			return
		await ctx.send(tag_list[tag]['content'])

	@tag.command(name='create', aliases=['c'])
	@checks.is_tag_disabled()
	async def tag_create(self, ctx, tag_name:commands.clean_content(use_nicknames=False), *, tag_content:str=''):
		tag = self.tname(tag_name)
		if not await self.tag_check(tag, tag_list, ctx.command.name, ctx.channel, ctx.message.author.id):
			return
		content = await self.manage_content(tag, tag_content, ctx.message.attachments, ctx.channel)
		if not content:
			return
		tag_list[tag] = {'content':tag_content,'owner':ctx.author.id,'date':f._t(tt.ti[1])}
		tag_update(tag, tag_list[tag])
		await ctx.send(tt.y+f"created the tag \"{tag}\"!")
		tlog(f"{ctx.author} created '{tag}' ({content})")
				
	@tag.command(name='edit')
	@checks.is_tag_disabled()
	async def tag_edit(self, ctx, tag_name:commands.clean_content(use_nicknames=False), *, tag_content:str=''):
		tag = self.tname(tag_name)
		if not await self.tag_check(tag, tag_list, ctx.command.name, ctx.channel, ctx.message.author.id):
			return
		content = await self.manage_content(tag, tag_content, ctx.message.attachments, ctx.channel)
		if not content:
			return
		tag_list[tag]['content'] = content
		tag_list[tag]['edited'] = f'{f._t(tt.ti[1])}'
		tag_update([tag+'.content',tag+'.edited'], [tag_list[tag]['content'],tag_list[tag]['edited']])
		await ctx.send(tt.y+f"updated the tag \"{tag}\"!")
		tlog(f"{ctx.author} updated '{tag}' ({content})")

	@tag.command(name='delete', aliases=['d'])
	@checks.is_tag_disabled()
	async def tag_remove(self, ctx, tag_name:commands.clean_content(use_nicknames=False)):
		tag = self.tname(tag_name)
		if not await self.tag_check(tag, tag_list, ctx.command.name, ctx.channel, ctx.message.author.id):
			return
		del tag_list[tag]
		tag_delete(tag)
		await ctx.send(tt.y+f"deleted the tag \"{tag}\"!")
		tlog(f"{ctx.author} deleted '{tag}'")

	@tag.command(name='transfer')
	@checks.is_tag_disabled()
	async def tag_transfer(self, ctx, tag_name:commands.clean_content(use_nicknames=False), user:discord.Member):
		tag = self.tname(tag_name)
		if not await self.tag_check(tag, tag_list, ctx.command.name, ctx.channel, ctx.message.author.id):
			return
		tag_list[tag]['owner'] = user.id
		tag_update(tag+'.owner', tag_list[tag]['owner'])
		await ctx.send(tt.y+f"ownership of tag \"{tag}\" has been transferred to **{user}**!")
		tlog(f"transferred {tag}' ({ctx.author} -> {user})")

	@tag.command(name='forceedit', aliases=['fe'])
	@checks.is_tag_disabled()
	@checks.is_admin()
	async def tag_force_edit(self, ctx, tag_name:commands.clean_content(use_nicknames=False), *, tag_content:str=None):
		tag = self.tname(tag_name)
		if not await self.tag_check(tag, tag_list, ctx.command.name, ctx.channel, ctx.message.author.id):
			return
		content = await self.manage_content(tag, tag_content, ctx.message.attachments, ctx.channel, True)
		if not content:
			return
		tag_list[tag]['content'] = content
		tag_list[tag]['edited'] = f'{f._t(tt.ti[1])}'
		tag_update([tag+'.content',tag+'.edited'], [tag_list[tag]['content'],tag_list[tag]['edited']])
		await ctx.send(tt.y+f"tag \"{tag}\" forcefully updated!")
		tlog(f"{ctx.author} forcefully updated '{tag}' ({content})")

	@tag.command(name='forceremove', aliases=['fr'])
	@checks.is_tag_disabled()
	@checks.is_admin()
	async def tag_force_remove(self, ctx, tag_name:commands.clean_content(use_nicknames=False)):
		tag = self.tname(tag_name)
		if not await self.tag_check(tag, tag_list, ctx.command.name, ctx.channel, ctx.message.author.id):
			return
		del tag_list[tag]
		tag_delete(tag)
		await ctx.send(tt.y+f"tag \"{tag}\" was forcefully deleted!")
		tlog(f"{ctx.author} forcefully deleted '{tag}'")

	@tag.command(name='forcetransfer', aliases=['ft'])
	@checks.is_tag_disabled()
	@checks.is_admin()
	async def tag_force_transfer(self, ctx, tag_name:commands.clean_content(use_nicknames=False), user:discord.Member):
		tag = self.tname(tag_name)
		if not await self.tag_check(tag, tag_list, ctx.command.name, ctx.channel, ctx.message.author.id):
			return
		before = self.bot.get_user(tag_list[tag]['owner'])
		tag_list[tag]['owner'] = user.id
		tag_update(tag+'.owner', tag_list[tag]['owner'])
		await ctx.send(tt.y+f"ownership of tag \"{tag}\" has been forcefully transferred to **{user}**!")
		tlog(f"{ctx.author} forcefully transferred {tag}' ({before} -> {user})")

	@tag.command(name='owner')
	@checks.is_tag_disabled()
	async def tag_owner(self, ctx, tag_name:commands.clean_content(use_nicknames=False)):
		tag = self.tname(tag_name)
		if not await self.tag_check(tag, tag_list, ctx.command.name, ctx.channel, ctx.message.author.id):
			return
		user = self.bot.get_user(tag_list[tag]['owner'])
		await ctx.send(tt.i+f"tag \"{tag}\" is owned by **{user}**")

	@tag.command(name='random')
	@checks.is_tag_disabled()
	async def tag_random(self, ctx):
		random_tag = f.smart_random(list(tag_list.keys()), 'tag')
		await ctx.send(f"**`tag: {random_tag}`**\n{tag_list[random_tag]['content']}")

	@tag.command(name='list')
	@checks.is_tag_disabled()
	async def tag_list(self, ctx, user:discord.Member=None):
		user = ctx.author if not user else user; tags_num = 0
		for tag in tag_list:
			if tag_list[tag]['owner'] == ctx.author.id:
				tags_num += 1
		if tags_num == 0:
			await ctx.send(tt.i+f"**{user.name}** does not own any tags!")
			return
		await ctx.send(tt.i+f"**{user}** owns **{tags_num}** tags:\n{tt.tags_list}/{str(user.id)}")

# 		========================

def setup(bot):
	bot.add_cog(tags(bot))