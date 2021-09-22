import discord
from discord.ext import commands
from a import checks
from a.funcs import f
from a.stuff import conf
import a.constants as tt

toggles = {True:'enabled', False:'disabled', 'enable':True, 'disable':False,}

class customization(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.group(name='settings', aliases=['s'])
	@commands.guild_only()
	@commands.cooldown(1, 1, commands.BucketType.guild)
	async def settings(self, ctx, key=None, action=None, *, value=None):
		await ctx.trigger_typing()
		if key == None:
			data = f.data(tt.config, ctx.guild.id, d={})
			for key in conf.keys:
				if key not in data:
					data[key] = conf.keys[key]['default'] if 'default' in conf.keys[key] else None
			e_settings = discord.Embed(title=f"", description=f"this is a list of trashbots configuration for this specific server\n[command documentation]({tt.settings_doc})\n[customize via dashboard]({tt.guild_config.format(ctx.guild.id)})", color=tt.color.pink)
			e_settings.set_author(name=f"trashbot settings", icon_url=tt.icon.info)
			perm_errors = []
			for group in conf.key_groups:
				text = ''
				for key in conf.key_groups[group]:
					try:
						if data[key] == None:
							value = 'n/a'
						elif conf.keys[key]['type'] == 'toggle':
							value = f'"{toggles[data[key]]}"'
						elif conf.keys[key]['type'] == 'role':
							role = ctx.guild.get_role(data[key])
							value = f'"{role.name}"'
							if role >= ctx.guild.me.top_role:
								value = '*'+value
								perm_errors.append(key)
						elif conf.keys[key]['type'] == 'channel':
							channel = self.bot.get_channel(data[key])
							value = f'"#{channel.name}"'
							perms = channel.permissions_for(ctx.guild.me)
							if not any([perms.send_messages, perms.read_messages]):
								value = '*'+value
								perm_errors.append(key)
						elif conf.keys[key]['type'] == 'list':
							value = f"[{', '.join(data[key])}]"
						elif conf.keys[key]['type'] == 'number':
							value = data[key]
						else:
							value = f'"{data[key]}"'							
					except:
						value = "'unable to get value'"
					text += f'\n{key}: {value}'
				e_settings.add_field(name=group, value=f"```py\n{text}\n```", inline=False)
			if len(perm_errors) > 0:
				e_settings.description += f"\n*note: the following settings require extra permissions to work: {', '.join(perm_errors)}*"
			await ctx.send(embed=e_settings)
		else:
			if not checks.guild_admin_check(ctx):
				return
			if key not in conf.keys.keys() or action not in conf.actions['all'] or action not in conf.actions['value' if conf.keys[key]['type'] in conf.value_types else conf.keys[key]['type']]:
				raise(commands.UserInputError)
				return
			data = f.data(tt.config, ctx.guild.id, d={})
			if conf.keys[key]['type'] == 'toggle':
				if key in data and data[key] == toggles[action]:
					await ctx.send(tt.x+f"{conf.keys[key]['info'][0]} is already {action}d!")
					return
				f.data_update(tt.config, ctx.guild.id, key, toggles[action])
				await ctx.send(tt.y+f"{action}d {key}!")
				return
			elif conf.keys[key]['type'] in conf.value_types:
				if action == 'set':
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
						#elif conf.keys[key]['type'] == 'emoji':
						#	emoji = await commands.PartialEmojiConverter().convert(ctx, value)
						#	value = [emoji.id, emoji.name]
						elif conf.keys[key]['type'] == 'number':
							value = [int(value), value]
						else:
							value = [value, value]
					except:	
						raise(commands.UserInputError)
						return		
					if key in data and data[key] == value[0]:
						await ctx.send(tt.x+f"the {conf.keys[key]['info'][0]} is already set to that!")
						return
					f.data_update(tt.config, ctx.guild.id, key, value[0])
					await ctx.send(tt.y+f"set the {conf.keys[key]['info'][0]} to '{value[1]}'")
					return
				elif action == 'reset' and key in data:
					f.data_update(tt.config, ctx.guild.id, key, None, 'unset')
					await ctx.send(tt.y+f"reset the {conf.keys[key]['info'][0]} to default!")
				else:
					await ctx.send(tt.x+f"the {conf.keys[key]['info'][0]} is already not set!")
					return
			elif conf.keys[key]['type'] == 'list':
				if value is None:
					await ctx.send(tt.w+'no values provided!')
					return
				applied_list=[]
				value_list = [x for x in value.replace(', ',',').split(',')]
				if key not in data:
					data[key] = []
				if action == 'add':
					for value in value_list:
						if ('valid' in conf.keys[key] and value not in conf.keys[key]['valid']) or value in data[key]:
							continue
						applied_list.append(value)
					if all(x in data[key] for x in value_list):
						await ctx.send(tt.x+f"all of the provided values are already set!")
						return
					if len(applied_list) == 0:
						await ctx.send(tt.x+f"no valid values provided!")
						return
					f.data_update(tt.config, ctx.guild.id, key, applied_list, 'append')
					await ctx.send(tt.y+f"added {f.split_list(applied_list,'and','`')} to the {conf.keys[key]['info'][0]}!")
					return
				elif action == 'remove':
					if key not in data or data[key] == [] or data[key] == None:
						await ctx.send(tt.x+f"there are no values set to remove!")
						return
					for value in value_list:
						if value in data[key]:
							applied_list.append(value)
					if applied_list == []:
						await ctx.send(tt.x+f"the provided values are not set in the first place!")
						return
					f.data_update(tt.config, ctx.guild.id, key, applied_list, 'remove')
					await ctx.send(tt.y+f"removed {f.split_list(applied_list,'and','`')} from the {conf.keys[key]['info'][0]}")
					return

def setup(bot):
	bot.add_cog(customization(bot))
