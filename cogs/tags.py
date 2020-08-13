import discord
import pickle
from discord.ext import commands
import data.constants as tt

# 		========================

#tags_list = {
#	'tag': {
#		'content': 'test',
#		'owner': 0,
#	},
#}

#pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
tags_list = pickle.load(open(tt.tags_pkl, "rb"))

reserved_args = ['list', 'owner', 'add', 'delete', 'edit', '@everyone', '@here']


class tags(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

# 		========================

	@commands.command(aliases=['t'])
	async def tag(self, ctx, arg1=None, arg2=None, *, arg3=None):
		await ctx.trigger_typing()
		tags_list = pickle.load(open(tt.tags_pkl, "rb"))
		try:
			if arg1 == None:
				await ctx.send("⚠️ ⠀please provide a valid tag or subcommand!")
			else:
				if arg1 in reserved_args:
					if arg2 in reserved_args: await ctx.send("❌ ⠀that tag is reserved!")
					elif arg1 == 'list':
						arg2 = ctx.author.id if not arg2 else arg2
						user = self.bot.get_user(arg2)
						list_tags_num = 0; list_tags = ''
						for tag in tags_list:
							if tags_list[tag]['owner'] == arg2:
								list_tags_num += 1	
								list_tags = list_tags + f"{list_tags_num}. \"{tag}\"\n"
						await ctx.send(f"```tags owned by {user} ({list_tags_num}):\n{list_tags}```")
					elif arg1 == 'add':
						if arg2 in tags_list: await ctx.send(f"⚠️ ⠀tag '{arg2}' already exists!")
						else:
							if arg3 == None: await ctx.send(f"⚠️ ⠀please provide content for the tag!") 
							elif len(arg2) > 999 or len(arg3) > 999: await ctx.send("️⚠️ ⠀too many characters! (1000 limit)")
							else:
								tt.sanitize(arg3)
								tags_list[arg2] = {'content':'', 'owner':0}
								tags_list[arg2]['content'] = arg3
								tags_list[arg2]['owner'] = ctx.author.id
								pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
								await ctx.send(f"✅ ⠀tag '{arg2}' created!")
					elif arg1 == 'delete':
						if arg2 in tags_list:
							if tags_list[arg2]['owner'] == ctx.author.id:
								del tags_list[arg2]
								pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
								await ctx.send(f"✅ ⠀tag '{arg2}' deleted!")
							else: await ctx.send("❌ ⠀you are not the owner of this tag!")
						else: await ctx.send(f"⚠️ ⠀tag '{arg2}' does not exist!")
					elif arg1 == 'edit':
						if arg2 in tags_list:
							if tags_list[arg2]['owner'] == ctx.author.id:
								if arg3 == None: await ctx.send(f"⚠️ ⠀please provide content for the tag!")
								elif len(arg3) > 999: await ctx.send("️⚠️ ⠀too many characters! (1000 limit)")
								else:
									tt.sanitize(arg3)
									tags_list[arg2]['content'] = arg3
									pickle.dump(tags_list, open(tt.tags_pkl, "wb"))
									await ctx.send(f"✅ ⠀tag '{arg2}' updated!")
							else: await ctx.send("❌ ⠀you are not the owner of this tag!")
						else: await ctx.send(f"⚠️ ⠀tag '{arg2}' does not exist!")
					elif arg1 == 'owner':
						if arg2 in tags_list:
							user = self.bot.get_user(tags_list[arg2]['owner'])
							await ctx.send(f"ℹ️ ⠀tag '{arg2}' is owned by `{user} ({user.id})`")
						else: await ctx.send(f"⚠️ ⠀tag '{arg2}' does not exist!")
				else: 
					if arg1 in tags_list: await ctx.send(tags_list[arg1]['content'])
					else: await ctx.send(f"⚠️ ⠀tag '{arg1}' does not exist!")
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

# 		========================

def setup(bot):
	bot.add_cog(tags(bot))