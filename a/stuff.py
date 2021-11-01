class cmds:
	legend = {
		"command <param>": "variable parameter",
		"command param": "subcommand parameter",
		"command <param1>/<param2>": "multiple subcommands/parameters",
		"#param(s)": "optional parameter(s) that can be empty",
	}
	_c_ = {
		'general': ["basic commands for general functions", {
			'help': ['help', "sends the link to this page"],
			'about': ['about', "gives internal info about trashbot"],
		}],
		'utilities': ["helpful utility commands", {
			'ping': ['ping', "tests and sends trashbots latency"],
			'server': ['server', "gives information about the current server"],
			'user': ['user <#user>', "gives information about a user"],
			'avatar': ['avatar <#user>', "sends the avatar of a user"],
			'emote': ['emote <emoji>', "sends the full image of an emoji", ['e', 'emoji']],
			'clear': ['clear <number> <#user>', "purges a specified number of messages in the current channel"],
			'massnick': ['massnick <nickname>/clear/undo/cancel', "modifies the nicknames of everyone in the server. 'clear' removes all nicknames, 'undo' and 'cancel' are self explanatory", None, "server admins only"],
			'report': ['report <content>', "sends a report to me (eli), please only use for errors and bugs! (note: attachments (i.e. images and files) can be sent with reports)"],
		}],
		'fun': ["miscellaneous silly commands", {
			'say': ['say <message>', "has trashbot repeat a message"],
			'echo': ['echo <channel> <message>', "has trashbot echo a message to another channel", None, "server admins only"],
			'urban': ['urban <word>', "provides the urban dictionary entry of a word"],
			'cat': ['cat <cat>/list', "sends a random cat picture from my collection"]
		}],
		'tags': ["commands related to trashbots tag system", {
			'tag': ['tag <subcommand>/<tag>', "main command for all tag functions; a tag name in place of a subcommand mimics 'tag view'", ['t']],
			'tag view': ['tag view <tag>', "sends the contents of a tag"],
			'tag create': ['tag create <tag> <content>', "creates a tag with the provided contents", ['c']],
			'tag delete': ['tag delete <tag>', "deletes a tag that you own", ['d']],
			'tag edit': ['tag edit <tag> <content>', "applies the provided contents to a tag you own", ['e']],
			'tag transfer': ['tag transfer <tag> <user>', "transfers ownership of a tag you own to someone else"],
			'tag info': ['tag info <tag>', "provides the owner and creation timestamp of the provided tag"],
			'tag list': ['tag list <#user>', "sends the list of tags owned by a user"],
			'tag random': ['tag random', "sends the contents of a randomly selected tag"],
		}],
		'customization': ["per server customization for trashbot", {
			'settings': ['settings <setting> <action> <value(s)>', "command for server config managing, leaving params blank displays the current servers config; documentation can be found [a:/docs/settings:here]", ['s'], "server admins only"],
		}],
	}

class conf:
	keys = {
		"prefix": {
			"group": "basic", 
			"type": "text",
			"name": "prefix",
			"description": "the command prefix",
			"default": "t!",
			"c": {"max":5, "size":1},
		},
		"disabledcmds": {
			"group": "basic",
			"type": "list",
			"name": "disabled commands",
			"description": "a list of commands that are disabled for members",
			"valid": ['tag','say','echo','urban','massnick','clear'],
		},
		"msgchannel": {
			"group": "messages", 
			"type": "channel",
			"name": "message channel", 
			"namealt": "channel",
			"description": "channel where welcome and farewell messages get sent to",
		},	
		"joinmsg": {
			"group": "messages", 
			"type": "text",
			"name": "greeting message", 
			"namealt": "greeting",
			"description": "message that is sent when a member joins",
			"c": {"type":"large", "max":1000},
		},
		"leavemsg": {
			"group": "messages", 
			"type": "text",
			"name": "farewell message", 
			"namealt": "farewell",
			"description": "message that is sent when a member leaves",
			"c": {"type":"large", "max":1000},
		},
		"autorole": {
			"group": "roles", 
			"type": "role",
			"name": "default role", 
			"namealt": "default",
			"description": "role assigned to members when they join",
		},
		"stickyroles": {
			"group": "roles",
			"type": "toggle",
			"name": "stickyroles",
			"description": "toggles saving and reassigning roles when members leave and rejoin",
			"default": False,
			"perms": ['manage_roles'],
		},
		"starboard": {
			"group": "starboard",
			"type": "channel",
			"name": "starboard channel",
			"namealt": "channel",
			"description": "the channel where starboard messages are sent to",
		},
		"starboardcount": {
			"group": "starboard",
			"type": "number", 
			"name": "starboard threshold",
			"namealt": "threshold",
			"description": "number of reactions needed to add a message to the starboard",
			"default": 5, 
			"c": {"min":1, "max":10}
		},
		"starboardemoji": {
			"group": "starboard",
			"type": "emoji", 
			"name": "starboard emoji",
			"namealt": "emoji",
			"description": "the emoji used on starboard messages",
			"default": '⭐',
			"c": {"max":18, "size":12},
		},
	}

	key_groups = {"basic":[],"messages":[],"roles":[],"starboard":[],}
	for key in keys: 
		key_groups[keys[key]['group']].append(key)
	value_types = ['text','number','channel','role','emoji']
	actions = {
		'all': [],
		'value': ['set', 'reset'],
		'toggle': ['enable', 'disable'],
		'list': ['add', 'remove'],
	}
	for x in actions: 
		actions['all'].extend(actions[x])