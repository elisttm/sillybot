import data.constants as tt

y = tt.y
w = tt.w
x = tt.x
i = tt.i

class _a(): # general error messages
	no_permission = x+"you do not have permission to use this command!"
	bot_no_permission = x+"i do not have permission to use that command here!"
	on_cooldown = x+"please wait `{}s` before using this command again!"
	invalid_params = w+"invalid command parameter(s) provided! {}"
	disabled_in_dm = x+"this command is disabled in dms!"
	guild_not_enabled = x+"that command is not enabled in this server!"

class _t(): # tags
	does_not_exist = w+"the tag \"{}\" does not exist!"
	already_exists = x+"the tag \"{}\" already exists!"
	not_owner = x+"you are not the owner of this tag!"
	reserved = x+"that tag is reserved!"
	charlimit = w+"too many characters! {}"

class _c(): # customization
	none_set = x+"no {} set for this guild!"
	removed = y+"removed this guilds {}!"
	_set = y+"set the {} for this guild to '{}'" 
	check = i+"the {} for this guild is '{}'"
	already_set = x+"the {} for this guild is already set to that!"

class _cm(): # cogmanager
	invalid_cog = w+"please specify a valid cog!"

