import discord, os, json
from discord.ext import commands
from a import checks
from a.funcs import funcs
import a.configs as conf
import a.constants as tt

def parse_toggle(ya):
	if ya == True: return "enabled"
	if ya == False: return "disabled"
	if ya == "enable": return True
	if ya == "disable": return False

class customization(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.load_db = funcs.load_db
		self.dump_db = funcs.dump_db
		self.check_for_db = funcs.check_for_db
		self.send_log = funcs.send_log
		
# 		========================

	@commands.group(name='settings', aliases=['s'])
	@commands.guild_only()
	async def settings(self, ctx):
		await ctx.trigger_typing()
		if ctx.invoked_subcommand is None:
			if ctx.subcommand_passed is not None:
				raise(commands.UserInputError)
				return 
			try:
				e_settings = discord.Embed(title=f"click here to go to the configuration dashboard", url=tt.guild_config.format(str(ctx.guild.id)), description=f"these settings only affect this server\n", color=tt.clr['pink'])
				e_settings.set_author(name=f"trashbot settings", icon_url=tt.ico['cog'])
				guild_data_path = tt.guild_data_path.format(str(ctx.guild.id))
				guild_data = {}
				for key in conf.default_settings:
					guild_data[key] = conf.default_settings[key]
				if os.path.exists(guild_data_path):
					guild_data_ = self.load_db(guild_data_path)
					for key in guild_data_:
						guild_data[key] = guild_data_[key]
				for group in conf.key_groups:
					text = ''
					for key in conf.key_groups[group]:
						if guild_data[key] == None:
							value = "not set"
						elif conf.keys[key]['type'] == 'toggle':
							value = parse_toggle(guild_data[key])
						elif conf.keys[key]['type'] == 'role':
							value = f"@{ctx.guild.get_role(guild_data[key]).name}"
						elif conf.keys[key]['type'] == 'channel':
							value = f"#{self.bot.get_channel(guild_data[key]).name}"
						else:
							value = f"{guild_data[key]}"
						text += f'\n{key} : \"{value}\"'
					e_settings.add_field(name=group, value=f"```py\n{text}\n```", inline=False)
				await ctx.send(embed=e_settings)
			except Exception as error:
				await ctx.send(tt.msg_e.format(error))

	@commands.command()
	@commands.guild_only()
	@checks.is_guild_admin()
	async def cfg_cmd(self, ctx, key, action, value=None):
		if action not in conf.actions:
			raise(commands.UserInputError)
			return
		guild_data_path = tt.guild_data_path.format(str(ctx.guild.id))
		try:
			if (conf.keys[key]['type'] == 'toggle' and (action not in conf.toggle_actions)) or (conf.keys[key]['type'] != 'toggle' and (action in conf.toggle_actions)):
				raise(commands.UserInputError)
				return
			self.check_for_db(guild_data_path)
			guild_data = self.load_db(guild_data_path)
			if conf.keys[key]['type'] == 'toggle':
				guild_data[key] = parse_toggle(action)
				await ctx.send(tt.y+f"{action}d {key}!")
				self.dump_db(guild_data_path, guild_data)
				return
			if action == 'set':
				set_value = ''; name = ''
				if conf.keys[key]['type'] == 'role':
					set_value = value.id; name = value.name
				elif conf.keys[key]['type'] == 'channel':
					set_value = value.id; name = value.mention
				else:
					if conf.keys[key]['type'] == 'number':
						try: set_value = int(value)
						except:	
							raise(commands.UserInputError)
							return		
					else:
						set_value = value
				if not set_value: set_value = value
				if key in guild_data and guild_data[key] == set_value:
					await ctx.send(tt.x+f"the {conf.keys[key]['c']['name']} is already set to that!")
					return
				guild_data[key] = set_value
				if not name: name = value
				await ctx.send(tt.y+f"set the {conf.keys[key]['c']['name']} to '{name}'")
			elif action == 'reset' and key in guild_data:
				del guild_data[key]
				await ctx.send(tt.y+f"reset the {conf.keys[key]['c']['name']} to default!")
			else:
				await ctx.send(tt.x+f"the {conf.keys[key]['c']['name']} is already the default value!")
				return
			self.dump_db(guild_data_path, guild_data)
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	# text/toggles/numbers
	@settings.command(aliases=['prefix','stickyroles','starboardcount','joinmsg','leavemsg','globaltags'])
	@checks.is_guild_admin()
	async def settings_text(self, ctx, action, *, text:str=None):
		await ctx.invoke(self.bot.get_command('cfg_cmd'), action=action, key=ctx.invoked_with, value=text)

	# channels
	@settings.command(aliases=['msgchannel','starboard'])
	@checks.is_guild_admin()
	async def settings_channels(self, ctx, action, *, channel:discord.TextChannel=None):
		channel = ctx.channel if not channel else channel
		await ctx.invoke(self.bot.get_command('cfg_cmd'), action=action, key=ctx.invoked_with, value=channel)

	# roles
	@settings.command(aliases=['defaultrole'])
	@checks.is_guild_admin()
	async def settings_roles(self, ctx, action, *, role:discord.Role=None):
		await ctx.invoke(self.bot.get_command('cfg_cmd'), action=action, key=ctx.invoked_with, value=role)

# 		========================

	# rolemenu stuff goes here

# 		========================

def setup(bot):
	bot.add_cog(customization(bot))