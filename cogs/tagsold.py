import discord
import pickle
import random
import time, datetime, pytz
from pytz import timezone
from discord.ext import commands
import data.constants as tt

# 		========================

# TAG LIST FORMAT

# tags_list = {
# 	'tag': {
# 		'content': 'test',
# 		'date':	'yeah',
# 		'owner': 0,
#  },
# }

#pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
tags_list = pickle.load(open(tt.tags_pkl, "rb"))

reserved_args = [
	'owner', 'create', 'c', 'add', 'delete', 'remove', 'r', 'edit', 'random', '@everyone', '@here',
]

create_args = ['add', 'create', 'c']
delete_args = ['delete', 'remove', 'r']

tag_doesnotexist = "⚠️ ⠀tag '{}' does not exist!"
tag_charlimit = "⚠️ ⠀too many characters! (1000 limit)"
tag_invalidcontent = "⚠️ ⠀invalid tag content!"
tag_invaliduserid = "⚠️ ⠀the provided user ID is invalid or does not exist!"
tag_listtoolong = "⚠️ ⠀your list too long!"
tag_alreadyexists = "❌ ⠀tag '{}' already exists!"
tag_invalidorreserved = "❌ ⠀invalid or reserved tag given!"
tag_reserved = "❌ ⠀that tag is reserved!"
tag_notowner = "❌ ⠀you are not the owner of this tag!"
tag_invalidargs = "❌ ⠀invalid tag/subcommand provided!"

def curtime():
	return datetime.datetime.now(timezone('US/Eastern')).strftime('%m/%d/%y %I:%M:%S %p')

#tags_list = pickle.load(open(tt.tags_pkl, "rb"))

class tags(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

# 		========================

	@commands.command(aliases=['t'])
	@commands.cooldown(1, 2) #, commands.BucketType.guild
	async def tag(self, ctx, arg1=None, arg2=None, *, arg3=None):
		await ctx.trigger_typing()
		tags_list = pickle.load(open(tt.tags_pkl, "rb"))
		try:
			if arg1 == None:
				await ctx.send(tag_invalidargs)
			else:
				arg1 = arg1.lower()
				if arg2 != None:
					arg2 = arg2.lower()
				if arg1 in reserved_args:
					if arg2 in reserved_args: 
						await ctx.send(tag_reserved)


					elif arg1 == 'random':
						random_tag = random.choice(list(tags_list.keys()))
						await ctx.send(f"**`tag: {random_tag}`**\n{tags_list[random_tag]['content']}")


					elif arg1 in create_args:
						if arg2 in tags_list: 
							await ctx.send(tag_alreadyexists.format(arg2))
						else:
							if arg3 == None: 
								await ctx.send(tag_invalidcontent) 
							elif len(arg2) > 999 or len(arg3) > 999: 
								await ctx.send(tag_charlimit)
							else:
								arg3 = tt.sanitize(text = arg3)
								tags_list[arg2] = {'content':'', 'owner':0, 'date':''}
								tags_list[arg2]['content'] = arg3
								tags_list[arg2]['owner'] = ctx.author.id
								tags_list[arg2]['date'] = curtime()
								pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
								await ctx.send(f"✅ ⠀tag '{arg2}' created!")


					elif arg1 in delete_args:
						if arg2 in tags_list:
							if tags_list[arg2]['owner'] == ctx.author.id:
								del tags_list[arg2]
								pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
								await ctx.send(f"✅ ⠀tag '{arg2}' deleted!")
							else: 
								await ctx.send(tag_notowner)
						else: 
							await ctx.send(tag_doesnotexist.format(arg2))


					elif arg1 == 'edit':
						if arg2 in tags_list:
							if tags_list[arg2]['owner'] == ctx.author.id:
								if arg3 == None: 
									await ctx.send(tag_invalidcontent)
								elif len(arg3) > 999: 
									await ctx.send(tag_charlimit)
								else:
									arg3 = tt.sanitize(text = arg3)
									tags_list[arg2]['content'] = arg3
									tags_list[arg2]['date'] = f'{curtime()} (edited)'
									pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
									await ctx.send(f"✅ ⠀tag '{arg2}' updated!")
							else: 
								await ctx.send(tag_notowner)
						else: 
							await ctx.send(tag_doesnotexist.format(arg2))


					elif arg1 == 'owner':
						if arg2 in tags_list:
							if arg2 != None:
								if arg2 not in reserved_args:
									user = self.bot.get_user(tags_list[arg2]['owner'])
									await ctx.send(f"ℹ️ ⠀tag '{arg2}' is owned by `{user} ({user.id})`")
								else:
									await ctx.send(tag_invalidorreserved)
							else:
								await ctx.send(tag_invalidorreserved)
						else: 
							await ctx.send(tag_doesnotexist.format(arg2))


				else: 
					if arg1 in tags_list:
						tag_content = tags_list[arg1]['content'] 
						tag_content = tt.sanitize(text = tag_content)
						await ctx.send(tag_content)
					else: 
						await ctx.send(tag_doesnotexist.format(arg1))
				

		except Exception as error:
			await ctx.send(tt.msg_e.format(error))


	@commands.command(aliases=['ta'])
	async def tagadmin(self, ctx, arg1=None, arg2=None, *, arg3=None):
		await ctx.trigger_typing()
		if ctx.author.id == tt.owner_id:
			tags_list = pickle.load(open(tt.tags_pkl, "rb"))

			if arg1 in delete_args:
				if arg2 in tags_list:
					del tags_list[arg2]
					pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
					await ctx.send(f"✅ ⠀tag '{arg2}' deleted!")
				else: 
					await ctx.send(tag_doesnotexist.format(arg2))

			elif arg1 == 'edit':
				if arg2 in tags_list:
					if arg3 == None: 
						await ctx.send(tag_invalidcontent)
					elif len(arg3) > 999: 
						await ctx.send(tag_charlimit)
					else:
						arg3 = tt.sanitize(text = arg3)
						tags_list[arg2]['content'] = arg3
						tags_list[arg2]['date'] = f'{curtime()} (force edited)'
						pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
						await ctx.send(f"✅ ⠀tag '{arg2}' updated!")

			else:
				await ctx.send("kjbsadjkhsdgjldsfgjlhdfsg")

		else: await ctx.send(tt.permdeny)

				
	@commands.command()
	async def transfer(self, ctx, arg1, user: discord.Member):
		await ctx.trigger_typing()
		try:
			tags_list = pickle.load(open(tt.tags_pkl, "rb"))
			if arg2 in tags_list:
				if tags_list[arg1]['owner'] == ctx.author.id:
					tags_list[arg1]['owner'] = user.id
					tags_list[arg1]['date'] = f'{curtime()} (transferred)'
					pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
					await ctx.send(f"✅ ⠀tag '{arg1}' has had its ownership transferred to {user.name}!")
				else: 
					await ctx.send(tag_notowner)
			else: 
				await ctx.send(tag_doesnotexist.format(arg1))
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))


	@commands.command()
	async def taglist(self, ctx, user: discord.Member = None):
		await ctx.trigger_typing()
		user = ctx.author if not user else user
		try:
			tags_list = pickle.load(open(tt.tags_pkl, "rb"))
			tags_num = 0
			for tag in tags_list:
				if tags_list[tag]['owner'] == user.id:
					tags_num += 1	
			if tags_num == 0:
				await ctx.send(f"ℹ️ ⠀{user.name} does not own any tags!")
			else:
				user_tags_link = tt.taglist + "?search=" + str(user.id)
				list_tags_msg = f"ℹ️ ⠀**{user}** owns **{tags_num}** tags:\n{user_tags_link}"
				await ctx.send(list_tags_msg)
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

# 		========================

def setup(bot):
	bot.add_cog(tags(bot))