import discord
import os
import json
from discord.ext import commands
from utils import checks
from utils.funcs import funcs
from data.messages import _c
import data.constants as tt

# 		========================

settings_groups = {
	'general': ['prefix', 'stickyroles'],
	'roles': ['defaultrole'],
	'channels': ['msgchannel', 'starboard'],
	'messages': ['joinmsg', 'leavemsg', 'banmsg'],
}
cosmetic_config = {
	'prefix': 'custom prefix',
	'stickyroles': 'sticky roles',
	'msgchannel': 'message channel',
	'starboard': 'starboard channel', 
	'defaultrole': 'default role',
	'joinmsg': 'join message',
	'leavemsg': 'leave message',
	'banmsg': 'ban message',
}
toggleable_configs = [
	'stickyroles',
]

config_subcommands = ['set', 'reset', 'enable', 'disable']

def undefined_value(setting):
	undefined = {'prefix':'default','msgchannel':'default'}
	if setting not in undefined:
		return f'not set'
	return undefined[setting]

class customization(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.load_db = funcs.load_db
		self.dump_db = funcs.dump_db
		self.check_for_db = funcs.check_for_db
		self.send_log = funcs.send_log
		self.log_prefix = "[CUSTOMIZATION]"
		
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
				guild_data_path = tt.guild_data_path.format(str(ctx.guild.id))
				e_settings = discord.Embed(title=f"click here for documentation on using this command", url=tt.settings_page, description=f"these are the settings for trashbot in this specific guild\n", color=tt.clr['pink'])
				e_settings.set_author(name=f"trashbot settings", icon_url=tt.ico['cog'])
				if os.path.exists(guild_data_path):
					guild_data = self.load_db(guild_data_path)
				else:
					guild_data = {}
				for group in settings_groups:
					embvalue = ''
					for config in settings_groups[group]:
						embvalue += f'{config} : '
						if (group not in guild_data) or (config not in guild_data[group]):
							embvalue += f'"{undefined_value(config)}"\n'
							continue
						if group == 'roles':
							role = ctx.guild.get_role(guild_data[group][config])
							embvalue += f'"{role.name}" ({role.id})\n'
							continue
						if group == 'channels':
							channel = self.bot.get_channel(guild_data[group][config])
							embvalue += f'"#{channel.name}" ({channel.id})\n'
							continue
						else:
							embvalue += f'"{guild_data[group][config]}"\n'
					e_settings.add_field(name=group, value=f"```py\n{embvalue}\n```", inline=False)
				await ctx.send(embed=e_settings)
			except Exception as error:
				await ctx.send(tt.msg_e.format(error))

	#			-----  BASE CONFIG THING  -----

	@commands.command()
	@commands.guild_only()
	async def cfg_cmd(self, ctx, group, config, action, param=None):
		guild_data_path = tt.guild_data_path.format(str(ctx.guild.id))
		try:
			if (config not in toggleable_configs) and ((action == 'enable') or (action == 'disable')):
				raise(commands.UserInputError)
				return
			if config in toggleable_configs:
				if (action == 'set') or (action == 'reset'):
					raise(commands.UserInputError)
					return
				self.check_for_db(guild_data_path)
				guild_data = self.load_db(guild_data_path)
				if group not in guild_data:
					guild_data[group] = {}
				if action == 'enable':
					guild_data[group][config] = True
					await ctx.send(tt.y+f"enabled {config}!")
				if action == 'disable':
					guild_data[group][config] = False
					await ctx.send(tt.y+f"disabled {config}!")
				self.dump_db(guild_data_path, guild_data)
				return
			if action == 'set':
				self.check_for_db(guild_data_path)
				guild_data = self.load_db(guild_data_path)
				if group not in guild_data:
					guild_data[group] = {}
				if group == 'roles':
					guild_data[group][config] = param.id
					param = param.id
				if group == 'channels':
					guild_data[group][config] = param.id
					param = param.mention
				else:
					guild_data[group][config] = param
				await ctx.send(_c._set.format(cosmetic_config[config], param))
			if action == 'reset':
				if not os.path.exists(guild_data_path):
					await ctx.send(_c.none_set.format(cosmetic_config[config]))
					return
				guild_data = self.load_db(guild_data_path)
				if (group not in guild_data) or (config not in guild_data[group]):
					await ctx.send(_c.none_set.format(cosmetic_config[config]))
					return
				del guild_data[group][config]
				await ctx.send(_c.removed.format(cosmetic_config[config]))
			self.dump_db(guild_data_path, guild_data)
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	#			-----  CONFIGURATION  -----

	@settings.command(aliases=['prefix','stickyroles'])
	@checks.is_guild_admin()
	async def settings_prefix(self, ctx, action, *, prefix:str=None):
		if action not in config_subcommands:
			raise(commands.UserInputError)
			return
		await ctx.invoke(self.bot.get_command('cfg_cmd'), action=action, group='general', config=ctx.invoked_with, param=prefix)

	@settings.command(aliases=['msgchannel','starboard'])
	@checks.is_guild_admin()
	async def settings_channels(self, ctx, action, *, channel:discord.TextChannel=None):
		channel = ctx.channel if not channel else channel
		if action not in config_subcommands:
			raise(commands.UserInputError)
			return
		await ctx.invoke(self.bot.get_command('cfg_cmd'), action=action, group='channels', config=ctx.invoked_with, param=channel)

	@settings.command(aliases=['defaultrole'])
	@checks.is_guild_admin()
	async def settings_roles(self, ctx, action, *, role:discord.Role=None):
		if action not in config_subcommands:
			raise(commands.UserInputError)
			return
		await ctx.invoke(self.bot.get_command('cfg_cmd'), action=action, group='roles', config=ctx.invoked_with, param=role)

	@settings.command(aliases=['joinmsg','leavemsg','banmsg'])
	@checks.is_guild_admin()
	async def settings_messages(self, ctx, action, *, message:str=None):
		if action not in config_subcommands:
			raise(commands.UserInputError)
			return
		await ctx.invoke(self.bot.get_command('cfg_cmd'), action=action, group='messages', config=ctx.invoked_with, param=message)

# 		========================

def setup(bot):
	bot.add_cog(customization(bot))