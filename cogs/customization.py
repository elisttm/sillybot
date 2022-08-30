import discord, emoji
from discord.ext import commands
from a import checks
from a.funcs import f
from a.stuff import conf
import a.constants as tt

class customization(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.group(name='settings', aliases=['s'])
	@commands.guild_only()
	@checks.is_guild_admin()
	@commands.cooldown(1, 1, commands.BucketType.guild)
	async def settings(self, ctx, key=None, action=None, *, value=None):
		await ctx.channel.typing()
		if not key:
			e_settings = discord.Embed(title=f"", description=f"this is a list of sillybots configuration for this specific server\n[command documentation]({tt.settings_doc})\n[customize via dashboard]({tt.site}config/{ctx.guild.id})", color=tt.dcolor)
			e_settings.set_author(name=f"sillybot settings", icon_url=tt.icon.info)
			perm_errors = []
			data = tt.config.find_one({'_id':ctx.guild.id},{'_id':0})
			if not data:
				data = {}
			for group in conf.key_groups:
				text = ''
				for key in conf.key_groups[group]:
					try:
						if key not in data and 'default' in conf.keys[key]:
							data[key] = conf.keys[key]['default']
						if key not in data or (data[key] != False and not data[key]): 
							data[key] = 'n/a'
						elif conf.keys[key]['type'] == 'toggle': 
							data[key] = 'disabled' if data[key] == False else 'enabled'
						elif conf.keys[key]['type'] == 'list': 
							data[key] = f"[{', '.join(data[key])}]"
						elif conf.keys[key]['type'] == 'text': 
							data[key] = f'"{data[key]}"'
						elif conf.keys[key]['type'] == 'emoji':
							if data[key] in emoji.UNICODE_EMOJI['en']:
								data[key] = f'{data[key]}'
							else:
								data[key] = f'{self.bot.get_emoji(int(data[key]))}'
						elif conf.keys[key]['type'] == 'role':
							role = ctx.guild.get_role(data[key])
							data[key] = f'{role.mention}'
						elif conf.keys[key]['type'] == 'channel':
							channel = self.bot.get_channel(data[key])
					except Exception:
 						data[key] = '<unable to get value>'
					text += f'\n**`{key}:`** {data[key]}'
				e_settings.add_field(name=group,value=text,inline=False)
			if len(perm_errors) > 0:
				e_settings.description += f"\n*note: i am missing permissions for the following settings: {', '.join(perm_errors)}*"
			await ctx.send(embed=e_settings)
		else:
			if key not in conf.keys.keys() or action not in conf.actions['all'] or action not in conf.actions['value' if conf.keys[key]['type'] in conf.value_types else conf.keys[key]['type']]:
				raise(commands.UserInputError)
				return
			data = tt.config.find_one({'_id':ctx.guild.id},{'_id':0})
			if not data:
				data = {}
			if action == 'reset': 
				if key in data:
					f._unset(tt.config, ctx.guild.id, key)
					await ctx.send(tt.y+f"reset {'the ' if conf.keys[key]['type'] != 'toggle' else ''}{conf.keys[key]['name']} to the default value!")
				else:
					await ctx.send(tt.x+f"{conf.keys[key]['name']} is already reset!")
			elif conf.keys[key]['type'] == 'toggle':
				if key in data and data[key] == True if action == 'enable' else False:
					await ctx.send(tt.x+f"{conf.keys[key]['name']} is already {action}d!")
					return
				f._set(tt.config, ctx.guild.id, {"$set":{key:True if action == 'enable' else False}})
				await ctx.send(tt.y+f"{action}d {key}!")
			elif conf.keys[key]['type'] in conf.value_types and action == 'set':
				try:
					if conf.keys[key]['type'] == 'role':
						role = await commands.RoleConverter().convert(ctx, value)
						if role >= ctx.guild.me.top_role or not ctx.guild.me.guild_permissions.manage_roles:
							await ctx.send(tt.w+"i do not have permission to manage this role!")
							return
						value = [role.id, role.name]
					elif conf.keys[key]['type'] == 'channel':
						channel = await commands.TextChannelConverter().convert(ctx, value)
						perms = channel.permissions_for(ctx.guild.me)
						if not perms.send_messages or not perms.read_messages:
							await ctx.send(tt.w+"i do not have permission to speak in this channel!")
							return
						value = [channel.id, channel.mention]
					elif conf.keys[key]['type'] == 'emoji':
						if value in emoji.UNICODE_EMOJI['en']:
							value = [value, value]
						else:
							_emoji = await commands.PartialEmojiConverter().convert(ctx, value)
							value = [_emoji.id, str(_emoji)]
					elif conf.keys[key]['type'] == 'number':
						value = [int(value), value]
					else:
						value = [value, value]
				except:
					raise(commands.UserInputError)
					return
				if (key in data and data[key] == value[0]) or (key not in data and 'default' in conf.keys[key] and value[0] == conf.keys[key]['default']):
					await ctx.send(tt.x+f"the {conf.keys[key]['name']} is already set to that!")
					return
				f._set(tt.config, ctx.guild.id, {"$set":{key:value[0]}})
				await ctx.send(tt.y+f"set the {conf.keys[key]['name']} to '{value[1]}'")
			elif conf.keys[key]['type'] == 'list':
				if value is None:
					await ctx.send(tt.w+'no values provided!')
					return
				value_list = [x.strip() for x in value.split(',')]
				if action == 'add':
					if key in data and all(x in data[key] for x in value_list):
						await ctx.send(tt.x+f"all of the provided values are already set!")
						return
					for v in value_list:
						if ('valid' in conf.keys[key] and v not in conf.keys[key]['valid']) or (key in data and v in data[key]):
							value_list.remove(v)
					if len(value_list) == 0:
						await ctx.send(tt.x+f"no valid values provided!")
						return
					f._list(tt.config, ctx.guild.id, key, value_list, 'add')
					await ctx.send(tt.y+f"added {f.split_list(value_list,'and','`')} to the {conf.keys[key]['name']}!")
				elif action == 'remove':
					if not data.get(key):
						await ctx.send(tt.x+f"there are no values set to remove!")
						return
					value_list = [v for v in value_list if v in data[key]]
					if len(value_list) == 0:
						await ctx.send(tt.x+f"the provided values are not set in the first place!")
						return
					if value_list == data[key]:
						f._unset(tt.config, ctx.guild.id, key)
					else:
						f._list(tt.config, ctx.guild.id, key, value_list, 'remove')
					await ctx.send(tt.y+f"removed {f.split_list(value_list,'and','`')} from the {conf.keys[key]['name']}")

async def setup(bot):
	await bot.add_cog(customization(bot))
