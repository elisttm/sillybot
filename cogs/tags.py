import discord, re, datetime
from discord.ext import commands
from a import checks
from a.funcs import f
import a.constants as tt

re_tag = re.compile("^[a-z0-9_-]*$")
reserved = ['tag','view','create','c','edit','e','delete','d','transfer','forceedit','forcetransfer','forceremove','info','random']

def tname(tag):
	return str(tag).lower().replace('.','')

class tags(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.db = tt.db['tags']

	async def tag_check(self, tag, tagdata, ctx):
		if tag in reserved:
			await ctx.channel.send(tt.x+"the provided tag is reserved!")
			return False
		if ctx.command.name != 'create' and tagdata == None:
			await ctx.channel.send(tt.w+f"the provided tag does not exist!")
			return False
		if tagdata != None and 'owner' in tagdata and tagdata['owner'] != ctx.author.id:
			await ctx.channel.send(tt.x+"you are not the owner of this tag!")
			return False
		return True

	async def manage_content(self, tag, tag_content, ctx):
		if ctx.message.attachments:
			tag_content += '' if not tag_content else ' '+ctx.message.attachments[0].url
		if not re_tag.match(tag):
			await ctx.channel.send(tt.x+"tag names cannot contain special characters except hyphens and underscores!")
			return False
		if len(tag) > 20 or len(tag_content) > 1000:
			await ctx.channel.send(tt.x+f"too many characters! (maximum 20 for tag names and 1000 for tag contents)")
			return False
		return tag_content

	@commands.group(name='tag', aliases=['t'])
	@commands.guild_only()
	@commands.cooldown(3, 5, commands.BucketType.user)
	async def tag(self, ctx):
		if ctx.invoked_subcommand is None:
			if ctx.subcommand_passed is None:
				raise(commands.UserInputError)
			await ctx.invoke(self.bot.get_command('tag view'), tag=tname(ctx.subcommand_passed))

	@tag.before_invoke
	async def tag_before_invoke(self, ctx):
		await ctx.channel.typing()

	@tag.command(name='view')
	async def tag_view(self, ctx, tag:tname):
		tagdata = self.db.find_one({'_id':tag},{'content':1})
		if not await self.tag_check(tag, tagdata, ctx):
			return
		await ctx.send(tagdata['content'])

	@tag.command(name='create', aliases=['c'])
	async def tag_create(self, ctx, tag:tname, *, tag_content:str):
		tagdata = self.db.find_one({'_id':tag},{'_id':1})
		if tagdata != None:
			await ctx.channel.send(tt.x+f"the provided tag already exists!")
			return
		if not await self.tag_check(tag, tagdata, ctx):
			return
		content = await self.manage_content(tag, tag_content, ctx)
		if not content:
			return
		self.db.update_one({'_id':tag}, {"$set":{'content':tag_content,'owner':ctx.author.id,'date':datetime.datetime.utcnow().timestamp()}}, upsert=True)
		await ctx.send(tt.y+f"created the tag **{tag}**!")
		f.log(f"{ctx.author} created '{tag}' ({content})", '[TAGS]')
				
	@tag.command(name='edit', aliases=['e'])
	async def tag_edit(self, ctx, tag:tname, *, tag_content:str):
		tagdata = self.db.find_one({'_id':tag},{'owner':1,'content':1})
		if not await self.tag_check(tag, tagdata, ctx):
			return
		content = await self.manage_content(tag, tag_content, ctx)
		if not content:
			return
		self.db.update_one({'_id':tag}, {"$set":{"content":content,"date":datetime.datetime.utcnow().timestamp()}}, upsert=True)
		await ctx.send(tt.y+f"updated the tag **{tag}**!")
		f.log(f"{ctx.author} updated '{tag}' ({content})", '[TAGS]')

	@tag.command(name='delete', aliases=['d'])
	async def tag_remove(self, ctx, tag:tname):
		tagdata = self.db.find_one({'_id':tag},{'owner':1})
		if not await self.tag_check(tag, tagdata, ctx):
			return
		self.db.delete_one({'_id':tag})
		await ctx.send(tt.y+f"deleted the tag **{tag}**!")
		f.log(f"{ctx.author} deleted '{tag}'", '[TAGS]')

	@tag.command(name='transfer')
	async def tag_transfer(self, ctx, tag:tname, user:discord.Member):
		tagdata = self.db.find_one({'_id':tag},{'owner':1})
		if not await self.tag_check(tag, tagdata, ctx):
			return
		self.db.update_one({'_id':tag}, {"$set":{"owner":user.id}}, upsert=False)
		await ctx.send(tt.y+f"transferred ownership of the tag **{tag}** to **{user}**!")
		f.log(f"transferred {tag}' ({ctx.author} -> {user})", '[TAGS]')

	@tag.command(name='forceedit')
	@checks.is_bot_admin()
	async def tag_force_edit(self, ctx, tag:tname, *, tag_content:str):
		tagdata = self.db.find_one({'_id':tag},{'content':1,'owner':1})
		if not await self.tag_check(tag, tagdata, ctx):
			return
		content = await self.manage_content(tag, tag_content, ctx)
		if not content:
			return
		self.db.update_one({'_id':tag}, {"$set":{"content":content,"date":datetime.datetime.utcnow().timestamp()}}, upsert=True)
		await ctx.send(tt.y+f"forcefully updated the tag **{tag}**!")
		f.log(f"{ctx.author} forcefully updated '{tag}' ({content})", '[TAGS]')

	@tag.command(name='forceremove')
	@checks.is_bot_admin()
	async def tag_force_remove(self, ctx, tag:tname):
		tagdata = self.db.find_one({'_id':tag},{'owner':1})
		if not await self.tag_check(tag, tagdata, ctx):
			return
		self.db.delete_one({'_id':tag})
		await ctx.send(tt.y+f"forcefully deleted the tag **{tag}**!")
		f.log(f"{ctx.author} forcefully deleted '{tag}'", '[TAGS]')

	@tag.command(name='forcetransfer')
	@checks.is_bot_admin()
	async def tag_force_transfer(self, ctx, tag:tname, user:discord.Member):
		tagdata = self.db.find_one({'_id':tag},{'owner':1})
		if not await self.tag_check(tag, tagdata, ctx):
			return
		before = self.bot.get_user(tagdata['owner'])
		self.db.update_one({'_id':tag}, {"$set":{"owner":user.id}}, upsert=False)
		await ctx.send(tt.y+f"forcefully transferred ownership of the tag **{tag}** to **{user}**!")
		f.log(f"{ctx.author} forcefully transferred {tag}' ({before} -> {user})", '[TAGS]')

	@tag.command(name='info')
	async def tag_info(self, ctx, tag:tname):
		tagdata = self.db.find_one({'_id':tag},{'date':1,'owner':1})
		if not await self.tag_check(tag, tagdata, ctx):
			return
		await ctx.send(tt.i+f"the tag **{tag}** was created on **<t:{tagdata['date']}:f>** by **{self.bot.get_user(tagdata['owner'])}**")

	@tag.command(name='random')
	async def tag_random(self, ctx):
		random_tag = list(self.db.aggregate([{"$sample":{"size":1}}]))[0]
		await ctx.send(f"**`tag: {random_tag['_id']}`**\n{random_tag['content']}")

	@tag.command(name='list')
	async def tag_list(self, ctx, user:discord.Member=None):
		user = ctx.author if not user else user
		user_tags = list(self.db.find({'owner':user.id},{'_id':1}))
		if not user_tags:
			await ctx.send(tt.i+f"**{user.name}** does not own any tags!")
			return
		await ctx.send(tt.i+f"**{user}** owns **{len(user_tags)}** tags:\n{tt.site}/tags/{user.id}")

async def setup(bot):
	await bot.add_cog(tags(bot))
