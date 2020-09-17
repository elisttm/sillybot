import data.constants as tt

s = tt.s
y = tt.y
w = tt.w
x = tt.x
i = tt.i
h = tt.h

charlimit = w+"too many characters! {}"

class _a(): # general error messages
	no_permission = x+"you do not have permission to use this command!"
	no_permission_perms = x+"{} need the permissions {} to use this command!"
	on_cooldown = x+"please wait `{}s` before using this command again!"
	invalid_params = w+"invalid command parameter(s) provided! {}"
	disabled_in_dm = x+"this command is disabled in dms!"
	guild_not_enabled = x+"that command is not enabled for this server!"

class _t(): # tags
	does_not_exist = w+"the tag \"{}\" does not exist!"
	already_exists = x+"the tag \"{}\" already exists!"
	not_owner = x+"you are not the owner of this tag!"
	reserved = x+"that tag is reserved!"
	cannot_be_blank = x+"tag cannot be blank!"
	charlimit = charlimit

class _u(): # utilities
	charlimit = charlimit
	mn_no_nicknames = x+"this guild does not have a nickname backup!"
	mn_no_revert = x+"cannot revert nicknames! (last massnick was a reset or revert)"
	mn_attempting = h+"attempting to {} `{}` nicknames, please wait..."
	mn_finished = y+"`{}/{}` nicknames successfully {}!"
	clr_invalid_amount = w+"invalid amount of messages! (must be between 1 - 100)"
	log_mn_attempting = "{} '{}' nicknames {}in '{}'..."
	log_mn_finished = "'{}/{}' nicknames {} {}in '{}'!"

class _c(): # customization
	none_set = x+"no {} set for this guild!"
	removed = y+"removed this guilds {}!"
	_set = y+"set the {} for this guild to '{}'" 
	check = i+"the {} for this guild is '{}'"
	already_set = x+"the {} for this guild is already set to that!"

class _cm(): # cogmanager
	invalid_cog = w+"please specify a valid cog!"

