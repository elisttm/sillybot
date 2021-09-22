import discord, re, datetime
from discord.ext import commands
from a import checks
from a.funcs import f
import a.constants as tt

re_tag = re.compile("^[a-z0-9_-]*$")
reserved = ['tag','view','create','c','edit','e','delete','d','transfer','forceedit','forcetransfer','forceremove','info','random']

class tags(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def tname(self, tag):
		return tag.lower().replace('.','')

	async def tag_check(self, tag_name, tagdata, ctx):
		cmd = ctx.command.name
		if tag_name in reserved:
			await ctx.channel.send(tt.x+"the provided tag is reserved!")
			return False
		if cmd != 'create' and tagdata == None:
			await ctx.channel.send(tt.w+f"the provided tag does not exist!")
			return False
		elif cmd == 'create' and tagdata != None:
			await ctx.channel.send(tt.x+f"the provided tag already exists!")
			return False
		if cmd in ['delete','edit','transfer'] and tagdata['owner'] != ctx.message.author.id:
			await ctx.channel.send(tt.x+"you are not the owner of this tag!")
			return False
		return True

	async def manage_content(self, tag_name, tag_content, ctx):
		if ctx.message.attachments:
			tag_content += (' ' if tag_content != '' else '') + ctx.message.attachments[0].url
		if not re_tag.match(tag_name):
			await ctx.channel.send(tt.x+"tag names cannot contain special characters except - and _!")
			return False
		if len(tag_name) > 20 or len(tag_content) > 1000:
			await ctx.channel.send(tt.x+f"too many characters! (maximum 20 for tag names and 1000 for tag contents)")
			return False
		return tag_content

	@commands.group(name='tag', aliases=['t'])
	@commands.guild_only()
	@commands.cooldown(3, 1, commands.BucketType.user)
	async def tag(self, ctx):
		if ctx.invoked_subcommand is None:
			if ctx.subcommand_passed is None:
				raise(commands.UserInputError)
			await ctx.invoke(self.bot.get_command('tag view'), tag_name=ctx.subcommand_passed)

	@tag.before_invoke
	async def tag_before_invoke(self, ctx):
		await ctx.trigger_typing()

	@tag.command(name='view')
	async def tag_view(self, ctx, tag_name:str):
		tag = self.tname(tag_name)
		tagdata = f.data(tt.tags, tag)
		if not await self.tag_check(tag, tagdata, ctx):
			return
		await ctx.send(tagdata['content'])

	@tag.command(name='create', aliases=['c'])
	async def tag_create(self, ctx, tag_name:str, *, tag_content:str):
		tag = self.tname(tag_name)
		tagdata = f.data(tt.tags, tag)
		if not await self.tag_check(tag, tagdata, ctx):
			return
		content = await self.manage_content(tag, tag_content, ctx)
		if not content:
			return
		f.d_set(tt.tags, tag, {"$set":{'content':tag_content,'owner':ctx.author.id,'date':f._t(False)}})
		await ctx.send(tt.y+f"created the tag **{tag}**!")
		f.log(f"{ctx.author} created '{tag}' ({content})", '[TAGS]')
				
	@tag.command(name='edit', aliases=['e'])
	async def tag_edit(self, ctx, tag_name:str, *, tag_content:str):
		tag = self.tname(tag_name)
		tagdata = f.data(tt.tags, tag)
		if not await self.tag_check(tag, tagdata, ctx):
			return
		content = await self.manage_content(tag, tag_content, ctx)
		if not content:
			return
		f.d_set(tt.tags, tag, {"$set":{"content":content,"date":f._t(False)}})
		await ctx.send(tt.y+f"updated the tag **{tag}**!")
		f.log(f"{ctx.author} updated '{tag}' ({content})", '[TAGS]')

	@tag.command(name='delete', aliases=['d'])
	async def tag_remove(self, ctx, tag_name:str):
		tag = self.tname(tag_name)
		tagdata = f.data(tt.tags, tag)
		if not await self.tag_check(tag, tagdata, ctx):
			return
		f.d_del(tt.tags, tag)
		await ctx.send(tt.y+f"deleted the tag **{tag}**!")
		f.log(f"{ctx.author} deleted '{tag}'", '[TAGS]')

	@tag.command(name='transfer')
	async def tag_transfer(self, ctx, tag_name:str, user:discord.Member):
		tag = self.tname(tag_name)
		tagdata = f.data(tt.tags, tag)
		if not await self.tag_check(tag, tagdata, ctx):
			return
		f.d_set(tt.tags, tag, {"$set":{"owner":user.id}})
		await ctx.send(tt.y+f"transferred ownership of the tag **{tag}** to **{user}**!")
		f.log(f"transferred {tag}' ({ctx.author} -> {user})", '[TAGS]')

	@tag.command(name='forceedit', aliases=['fe'])
	@checks.is_bot_admin()
	async def tag_force_edit(self, ctx, tag_name:str, *, tag_content:str):
		tag = self.tname(tag_name)
		tagdata = f.data(tt.tags, tag)
		if not await self.tag_check(tag, tagdata, ctx):
			return
		content = await self.manage_content(tag, tag_content, ctx)
		if not content:
			return
		f.d_set(tt.tags, tag, {"$set":{"content":content,"date":f._t(False)}})
		await ctx.send(tt.y+f"forcefully updated the tag **{tag}**!")
		f.log(f"{ctx.author} forcefully updated '{tag}' ({content})", '[TAGS]')

	@tag.command(name='forceremove', aliases=['fr'])
	@checks.is_bot_admin()
	async def tag_force_remove(self, ctx, tag_name:str):
		tag = self.tname(tag_name)
		tagdata = f.data(tt.tags, tag)
		if not await self.tag_check(tag, tagdata, ctx):
			return
		f.d_del(tt.tags, tag)
		await ctx.send(tt.y+f"forcefully deleted the tag **{tag}**!")
		f.log(f"{ctx.author} forcefully deleted '{tag}'", '[TAGS]')

	@tag.command(name='forcetransfer')
	@checks.is_bot_admin()
	async def tag_force_transfer(self, ctx, tag_name:str, user:discord.Member):
		tag = self.tname(tag_name)
		tagdata = f.data(tt.tags, tag)
		if not await self.tag_check(tag, tagdata, ctx):
			return
		before = self.bot.get_user(tagdata['owner'])
		f.d_set(tt.tags, tag, {"$set":{"owner":user.id}})
		await ctx.send(tt.y+f"forcefully transferred ownership of the tag **{tag}** to **{user}**!")
		f.log(f"{ctx.author} forcefully transferred {tag}' ({before} -> {user})", '[TAGS]')

	@tag.command(name='info')
	async def tag_info(self, ctx, tag_name:str):
		tag = self.tname(tag_name)
		tagdata = f.data(tt.tags, tag)
		if not await self.tag_check(tag, tagdata, ctx):
			return
		await ctx.send(tt.i+f"the tag **{tag}** was created on **{datetime.datetime.utcfromtimestamp(tagdata['date']).strftime(tt.ti.swag)} UTC** by **{self.bot.get_user(tagdata['owner'])}**")

	@tag.command(name='random')
	async def tag_random(self, ctx):
		random_tag = list(tt.tags.aggregate([{"$sample":{"size":1}}]))[0]
		await ctx.send(f"**`tag: {random_tag['_id']}`**\n{random_tag['content']}")

	@tag.command(name='list')
	async def tag_list(self, ctx, user:discord.Member=None):
		user = ctx.author if not user else user
		user_tags = list(tt.tags.find({'owner':user.id},{'_id':1}))
		if not user_tags:
			await ctx.send(tt.i+f"**{user.name}** does not own any tags!")
			return
		await ctx.send(tt.i+f"**{user}** owns **{len(user_tags)}** tags:\n{tt.site}/tags/{user.id}")

def setup(bot):
	bot.add_cog(tags(bot))
