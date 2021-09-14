import discord
from discord.ext import commands
from a import checks
from a.funcs import f
import a.configs as conf
import a.constants as tt

toggles = {True:'enabled', False:'disabled', 'enable':True, 'disable':False,}

class customization(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
# 		========================

	@commands.group(name='settings', aliases=['s'])
	@commands.guild_only()
	async def settings(self, ctx):
		await ctx.trigger_typing()
		if ctx.invoked_subcommand is None:
			if ctx.subcommand_passed is not None:
				raise(commands.UserInputError)
				return 
			guild_config = conf.default_settings
			data = f.data(tt.config, ctx.guild.id)
			if data is not None:
				for key in data:
					guild_config[key] = data[key]
			e_settings = discord.Embed(title=f"", description=f"this is a list of trashbots configuration for this specific server\n[command documentation]({tt.settings_doc})\n[customize via dashboard]({tt.guild_config.format(ctx.guild.id)})", color=tt.color.pink)
			e_settings.set_author(name=f"trashbot settings", icon_url=tt.icon.cog)
			for group in conf.key_groups:
				text = ''
				for key in conf.key_groups[group]:
					if f.empty(guild_config[key]):
						value = 'n/a'
					elif conf.keys[key]['type'] == 'toggle':
						value = f'"{toggles[guild_config[key]]}"'
					elif conf.keys[key]['type'] == 'role':
						value = f'"@{ctx.guild.get_role(guild_config[key]).name}"'
					elif conf.keys[key]['type'] == 'channel':
						value = f'"#{self.bot.get_channel(guild_config[key]).name}"'
					elif conf.keys[key]['type'] == 'list':
						value = f"[{', '.join(guild_config[key])}]"
					elif conf.keys[key]['type'] == 'number':
						value = guild_config[key]
					else:
						value = f'"{guild_config[key]}"'
					text += f'\n{key} : {value}'
				e_settings.add_field(name=group, value=f"```py\n{text}\n```", inline=False)
			await ctx.send(embed=e_settings)

	@settings.command(aliases=[
		'prefix','joinmsg','leavemsg','starboardcount',
		'stickyroles','globaltags',
		'msgchannel','starboard',
		'autorole',
		'disabled',
	])
	@commands.guild_only()
	@checks.is_guild_admin()
	@commands.cooldown(1, 1, commands.BucketType.guild)
	async def settings_config(self, ctx, action, *, value=None):
		key = ctx.invoked_with
		if key == 'settings_config':
			return
		if action not in conf.actions['all'] or action not in conf.actions['value' if conf.keys[key]['type'] in conf.value_types else conf.keys[key]['type']]:
			raise(commands.UserInputError)
			return
		data = f.data(tt.config, ctx.guild.id, d={})

		if conf.keys[key]['type'] == 'toggle':
			if key in data and data[key] == toggles[action]:
				await ctx.send(tt.x+f"{conf.keys[key]['c']['name']} is already {action}d!")
				return
			f.data_update(tt.config, ctx.guild.id, key, toggles[action])
			await ctx.send(tt.y+f"{action}d {key}!")
			return

		elif conf.keys[key]['type'] in conf.value_types:
			if action == 'set':
				_value = [value, value]
				if conf.keys[key]['type'] == 'role':
					value = await commands.RoleConverter().convert(ctx, value)
					_value = [value.id, value.name]
				elif conf.keys[key]['type'] == 'channel':
					value = await commands.TextChannelConverter().convert(ctx, value)
					_value = [value.id, value.mention]
				elif conf.keys[key]['type'] == 'number':
					try: 
						_value[0] = int(value)
					except:	
						raise(commands.UserInputError)
						return		
				if key in data and data[key] == _value[0]:
					await ctx.send(tt.x+f"the {conf.keys[key]['c']['name']} is already set to that!")
					return
				f.data_update(tt.config, ctx.guild.id, key, _value[0])
				await ctx.send(tt.y+f"set the {conf.keys[key]['c']['name']} to '{_value[1]}'")
				return
			elif action == 'reset' and key in data:
				f.data_update(tt.config, ctx.guild.id, key, None, 'unset')
				await ctx.send(tt.y+f"reset the {conf.keys[key]['c']['name']} to default!")
			else:
				await ctx.send(tt.x+f"the {conf.keys[key]['c']['name']} is already set to the default value!")
				return

		elif conf.keys[key]['type'] == 'list':
			if value is None:
				await ctx.send(tt.w+'no values provided!')
				return
			add_values=remove_values=invalid_values=data_list=[]
			value_list = [x.replace(' ','') for x in value.split(conf.keys[key]['c']['separator'])]
			print(value_list)
			if key in data and data[key] != None:
				data_list = data[key]
			else:
				f.data_update(tt.config, ctx.guild.id, key, [])
			if action == 'add':
				for value in value_list:
					if ('valid' in conf.keys[key] and value not in conf.keys[key]['valid']) or value in data_list:
						invalid_values.append(value)
						continue
					add_values.append(value)
				if all(x in data_list for x in value_list):
					await ctx.send(tt.x+f"all of the provided values are already set!")
					return
				if len(add_values) == 0:
					await ctx.send(tt.x+f"no valid values provided!")
					return
				f.data_update(tt.config, ctx.guild.id, key, add_values, 'append')
				await ctx.send(tt.y+f"added {f.split_list(add_values,'and','`')} to the {conf.keys[key]['c']['name']}! {'(ignoring '+f.split_list(invalid_values,'and','`')+')' if len(invalid_values) > 0 else ''}")
				return
			elif action == 'remove':
				if key not in data or f.empty(data[key]):
					await ctx.send(tt.x+f"there are no values set that can be removed!")
					return
				for value in value_list:
					if value in data_list:
						remove_values.append(value)
				print(remove_values)
				if remove_values == []:
					await ctx.send(tt.x+f"the provided values are not set in the first place!")
					return
				f.data_update(tt.config, ctx.guild.id, key, remove_values, 'remove')
				await ctx.send(tt.y+f"removed {f.split_list(remove_values,'and','`')} from the {conf.keys[key]['c']['name']}")
				return

# 		========================

def setup(bot):
	bot.add_cog(customization(bot))