import discord
import os
import json
from discord.ext import commands
from utils import checks
from utils.funcs import funcs
from data.messages import _c
import data.constants as tt

# 		========================

settings_groups_list = {
#	'group': {'label':'keyword',},
	'general': {
		'prefix':'prefix',
	}, 
	'roles': {
		'default':'defaultrole',
	}, 
	'channels': {
		'msgchannel':'msgchannel',
		'starboard':'starboard',
	},
	'messages': {
		'join':'joinmsg', 
		'leave':'leavemsg', 
		'ban':'banmsg'
	,}
}

cosmetic_config = {'msgchannel':'message channel', 'defaultrole':'default role','prefix':'custom prefix'}

config_subcommands = ['set', 'reset']

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

# typing.Union[discord.TextChannel, discord.Member]

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
				for group in settings_groups_list:
					embvalue = ''
					for x, y in settings_groups_list[group].items():
						embvalue += f'{y} : '
						if (group not in guild_data) or (x not in guild_data[group]):
							embvalue += f'"{undefined_value(x)}"\n'
							continue
						if group == 'roles':
							role = ctx.guild.get_role(guild_data[group][x])
							embvalue += f'"{role.name}" ({role.id})\n'
							continue
						if group == 'channels':
							channel = self.bot.get_channel(guild_data[group][x])
							embvalue += f'"#{channel.name}" ({channel.id})\n'
							continue
						else:
							embvalue += f'"{guild_data[group][x]}"\n'
					e_settings.add_field(name=group, value=f"```py\n{embvalue}\n```", inline=False)
				await ctx.send(embed=e_settings)
			except Exception as error:
				await ctx.send(tt.msg_e.format(error))

	#			-----  BASE CONFIG THING  -----

	@commands.command()
	@commands.guild_only()
	async def cfg_cmd(self, ctx, group, config, action, param=None):
		c_config = config; c_group = group; note = ''
		if group[-1] == 's':
			c_group = group[:len(group)-1]
		if config in cosmetic_config : 
			c_config = cosmetic_config[config]
			c_group = ''
		st = f"{c_config} {c_group}"
		guild_data_path = tt.guild_data_path.format(str(ctx.guild.id))
		try:
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
				await ctx.send(_c._set.format(st, param)+' '+note)
			if action == 'reset':
				if not os.path.exists(guild_data_path):
					await ctx.send(_c.none_set.format(st))
					return
				guild_data = self.load_db(guild_data_path)
				if (group not in guild_data) or (config not in guild_data[group]):
					await ctx.send(_c.none_set.format(st))
					return
				del guild_data[group][config]
				await ctx.send(_c.removed.format(st))
			self.dump_db(guild_data_path, guild_data)
		except Exception as error:
			await ctx.send(tt.msg_e.format(error))

	#			-----  GENERAL  -----

	@settings.command(name = 'prefix')
	@checks.is_guild_admin()
	async def settings_prefix(self, ctx, action, *, prefix:str=None):
		group = 'general'; config = 'prefix'
		if action not in config_subcommands:
			raise(commands.UserInputError)
			return
		await ctx.invoke(self.bot.get_command('cfg_cmd'), action=action, group=group, config=config, param=prefix)

	#			-----  CHANNELS  -----

	@settings.command(name = 'msgchannel')
	@checks.is_guild_admin()
	async def settings_msgchannel(self, ctx, action, *, channel:discord.TextChannel=None):
		channel = ctx.channel if not channel else channel
		group = 'channels'; config = 'msgchannel'
		if action not in config_subcommands:
			raise(commands.UserInputError)
			return
		await ctx.invoke(self.bot.get_command('cfg_cmd'), action=action, group=group, config=config, param=channel)

	@settings.command(name = 'starboard')
	@checks.is_guild_admin()
	async def settings_starboard(self, ctx, action, *, channel:discord.TextChannel=None):
		group = 'channels'; config = 'starboard'
		if action not in config_subcommands:
			raise(commands.UserInputError)
			return
		await ctx.invoke(self.bot.get_command('cfg_cmd'), action=action, group=group, config=config, param=channel)

	#			-----  ROLES  -----

	@settings.command(name = 'defaultrole')
	@checks.is_guild_admin()
	async def settings_defaultrole(self, ctx, action, *, role:discord.Role=None):
		group = 'roles'; config = 'default'
		if action not in config_subcommands:
			raise(commands.UserInputError)
			return
		await ctx.invoke(self.bot.get_command('cfg_cmd'), action=action, group=group, config=config, param=role)

	#			-----  MESSAGES  -----

	@settings.command(name = 'joinmsg')
	@checks.is_guild_admin()
	async def settings_joinmsg(self, ctx, action, *, message:str=None):
		group = 'messages'; config = 'join'
		if action not in config_subcommands:
			raise(commands.UserInputError)
			return
		await ctx.invoke(self.bot.get_command('cfg_cmd'), action=action, group=group, config=config, param=message)

	@settings.command(name = 'leavemsg')
	@checks.is_guild_admin()
	async def settings_leavemsg(self, ctx, action, *, message:str=None):
		group = 'messages'; config = 'leave'
		if action not in config_subcommands:
			raise(commands.UserInputError)
			return
		await ctx.invoke(self.bot.get_command('cfg_cmd'), action=action, group=group, config=config, param=message)

	@settings.command(name = 'banmsg')
	@checks.is_guild_admin()
	async def settings_banmsg(self, ctx, action, *, message:str=None):
		group = 'messages'; config = 'ban'
		if action not in config_subcommands:
			raise(commands.UserInputError)
			return
		await ctx.invoke(self.bot.get_command('cfg_cmd'), action=action, group=group, config=config, param=message)			

# 		========================

def setup(bot):
	bot.add_cog(customization(bot))