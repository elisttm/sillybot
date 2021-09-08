import discord
from discord.ext import commands
from a import checks
from a.funcs import f
import a.configs as conf
import a.constants as tt

def parse_toggle(value):
	if value == True: return "enabled"
	if value == False: return "disabled"
	if value == "enable": return True
	if value == "disable": return False

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
			e_settings = discord.Embed(title=f"\u200b", description="this is a list of trashbots configuration for this specific server", color=tt.clr['pink'])
			e_settings.set_author(name=f"trashbot settings", icon_url=tt.ico['cog'])
			e_settings.add_field(name="\u200b", value=f"[command documentation]({tt.settings_doc})\n[customize via dashboard]({tt.guild_config.format(ctx.guild.id)})")
			for group in conf.key_groups:
				text = ''
				for key in conf.key_groups[group]:
					if guild_config[key] == None:
						value = "not set"
					elif conf.keys[key]['type'] == 'toggle':
						value = parse_toggle(guild_config[key])
					elif conf.keys[key]['type'] == 'role':
						value = f"@{ctx.guild.get_role(guild_config[key]).name}"
					elif conf.keys[key]['type'] == 'channel':
						value = f"#{self.bot.get_channel(guild_config[key]).name}"
					else:
						value = f"{guild_config[key]}"
					text += f'\n{key} : \"{value}\"'
				e_settings.add_field(name=group, value=f"```py\n{text}\n```", inline=False)
			await ctx.send(embed=e_settings)

	def action_check(key, action):
		if conf.keys[key]['type'] in conf.value_types: 
			_type = 'value'
		else: 
			_type = conf.keys[key]['type']
		if action not in conf.actions[_type]:
			return False
		return True

	@commands.command()
	@commands.guild_only()
	@checks.is_guild_admin()
	async def cfg_cmd(self, ctx, key, action, value=None):
		if action not in conf.all_actions or self.action_check(key, action) == False:
			raise(commands.UserInputError)
			return
		data = f.data(tt.config, ctx.guild.id, {})
		if conf.keys[key]['type'] == 'toggle':
			f.data_update(tt.config, ctx.guild.id, key, parse_toggle(action))
			await ctx.send(tt.y+f"{action}d {key}!")
			return
		if conf.keys[key]['type'] == 'list':
			if value is None:
				await ctx.send(tt.w+'no list of values provided!')
				return
			value_list = value.replace(' ','').split(',')
			add_values=remove_values=invalid_values=data_list=[];note=''
			if key in data:
				data_list = data[key]
			if action == 'add':
				for value in value_list:
					if 'valid' in conf.keys[key] and value not in conf.keys[key]['valid']:
						invalid_values.append(value)
						continue
					if value in data_list:
						if len(value_list) == 1:
							return await ctx.send('')
						continue
					add_values.append(value)
				if len(invalid_values) > 0:
					note = f"(note: {f.split_list(invalid_values)} were ignored as they are invalid)"
				if len(add_values) == 0:
					await ctx.send(tt.x+f"no valid values provided! {note}")
					return
				f.data_update(tt.config, ctx.guild.id, key, data_list.extend(add_values), 'append')
				await ctx.send(tt.y+f"added {f.split_list(add_values,'and','`')} to the {conf.keys[key]['c']['name']} {note}")
				return
			elif action == 'remove':
				if key not in data:
					await ctx.send(tt.x+f"the {conf.keys[key]['c']['name']} have no values to remove!")
					return
				for value in value_list:
					if value not in data_list:
						remove_values.append(value)
				f.data_update(tt.config, ctx.guild.id, key, [x for x in data_list if x not in remove_values], 'remove')
				await ctx.send(tt.y+f"removed {f.split_list(add_values,'and','`')} from the {conf.keys[key]['c']['name']}")
				return
		elif conf.keys[key]['type'] in conf.value_types:
			if action == 'set':
				set_value = None; name = ''
				if conf.keys[key]['type'] == 'role':
					set_value = value.id
					value.name
				elif conf.keys[key]['type'] == 'channel':
					set_value = value.id
					name = value.mention
				elif conf.keys[key]['type'] == 'number':
					try: 
						set_value = int(value)
					except:	
						raise(commands.UserInputError)
						return		
				if not set_value: 
					set_value = value
				if not name: 
					name = value
				if key in data and data[key] == set_value:
					await ctx.send(tt.x+f"the {conf.keys[key]['c']['name']} is already set to that!")
					return
				f.data_update(tt.config, ctx.guild.id, key, set_value)
				await ctx.send(tt.y+f"set the {conf.keys[key]['c']['name']} to '{name}'")
				return
			elif action == 'reset' and key in data:
				f.data_remove(tt.config, ctx.guild.id, key)
				await ctx.send(tt.y+f"reset the {conf.keys[key]['c']['name']} to default!")
			else:
				await ctx.send(tt.x+f"the {conf.keys[key]['c']['name']} is already set to the default value!")
				return

	# text / toggles / numbers / lists
	@settings.command(aliases=[
		'prefix','joinmsg','leavemsg',
		'starboardcount',
		'stickyroles','globaltags',
		'disable',
	])
	@checks.is_guild_admin()
	async def settings_text(self, ctx, action, *, text=None):
		await ctx.invoke(self.bot.get_command('cfg_cmd'), action=action, key=ctx.invoked_with, value=text)

	# channels
	@settings.command(aliases=[
		'msgchannel','starboard',
	])
	@checks.is_guild_admin()
	async def settings_channels(self, ctx, action, *, channel:discord.TextChannel=None):
		await ctx.invoke(self.bot.get_command('cfg_cmd'), action=action, key=ctx.invoked_with, value=ctx.channel if not channel else channel)

	# roles
	@settings.command(aliases=[
		'defaultrole',
	])
	@checks.is_guild_admin()
	async def settings_roles(self, ctx, action, *, role:discord.Role=None):
		await ctx.invoke(self.bot.get_command('cfg_cmd'), action=action, key=ctx.invoked_with, value=role)

# 		========================

	# rolemenu stuff goes here

# 		========================

def setup(bot):
	bot.add_cog(customization(bot))