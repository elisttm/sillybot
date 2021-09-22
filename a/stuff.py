class cmds:
	legend = {
		"<param>": "variable parameter",
		"subcmd": "subcommand parameter",
		"[params]": "group of parameters",
		"^param(s)": "optional parameter(s) that can be empty",
	}
	_c_ = {
		'general': ["basic commands for general functions", {
			'help': ['help', "sends the link to this page"],
			'about': ['about', "gives internal info about trashbot"],
		}],
		'utilities': ["helpful utility commands", {
			'ping': ['ping', "tests and sends trashbots latency"],
			'server': ['server', "gives information about the current server"],
			'user': ['user <user>', "gives information about a user"],
			'avatar': ['avatar <user>', "sends the avatar of a user"],
			'emote': ['emote <emoji>', "sends the full image of an emoji", ['e', 'emoji']],
			'clear': ['clear <number>', "purges a specified number of messages in the current channel"],
			'massnick': ['massnick <nickname>/clear/undo/cancel', "modifies the nicknames of everyone in the server. 'clear' removes all nicknames, 'undo' and 'cancel' are self explanatory", None, "server admins only"],
			'report': ['report <text>', "sends a report to me (eli); please only use for errors and bugs!"],
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
			'tag owner': ['tag owner <tag>', "sends the name of the owner of a tag"],
			'tag list': ['tag list <user>', "sends the list of tags owned by a user"],
			'tag random': ['tag random', "sends the contents of a randomly selected tag"],
		}],
		'customization': ["per server customization for trashbot", {
			'settings': ['settings <setting> <action> <params>', "used to manage the server config, leaving params blank returns the current servers config; [a:/docs/settings:link to documentation]", ['s'], "server admins only"],
		}],
	}

class conf:
	keys = {
		"prefix": {
			"group": "basic", 
			"type": "text",
			"default": "t!",
			"info": ["prefix", "the command prefix"],
			"c": {"max":"5", "size":"1"},
		},
		"msgchannel": {
			"group": "messages", 
			"type": "channel",
			"info": ["message channel", "channel that welcome/farewell messages are put in"],
		},	
		"joinmsg": {
			"group": "messages", 
			"type": "text",
			"info": ["greeting message", "message sent when a member joins"],
			"c": {"max":"1000", "size":"25"},
		},
		"leavemsg": {
			"group": "messages", 
			"type": "text",
			"info": ["farewell message", "message sent when a member leaves"],
			"c": {"max":"1000", "size":"25"},
		},
		"autorole": {
			"group": "roles", 
			"type": "role",
			"info": ["default role", "role assigned to members when they join"]
		},
		"stickyroles": {
			"group": "roles",
			"type": "toggle",
			"default": False,
			"info": ["stickyroles", "toggles saving and reassigning roles when members leave and rejoin"],
		},
		"starboard": {
			"group": "starboard",
			"type": "channel",
			"info": ["starboard channel", "the channel used for the starboard"],
		},
		"starboardcount": {
			"group": "starboard",
			"type": "number", 
			"default": 5, 
			"info": ["starboard threshold", "number of reactions needed to add a message to the starboard"],
			"c": {"min":1, "max":10}
		},
		#"starboardemoji": {
		#	"group": "starboard",
		#	"type": "emoji", 
		#	"default": emoji.emojize(':star:'),
		# "info": ["starboard reaction emoji", "the emoji used for starboard reactions"] 
		#},
		"disabled": {
			"group": "commands",
			"type": "list",
			"valid": ['tag'],
			"info": ["disabled commands", "list of commands that are disabled for members"],
		},
	}

	key_groups = {"basic":[], "commands":[], "roles":[], "messages":[], "starboard":[],}
	for key in keys:
		key_groups[keys[key]['group']].append(key)

	value_types = ['text','number','channel','role']
	actions = {
		'all': [],
		'value': ['set', 'reset'],
		'toggle': ['enable', 'disable'],
		'list': ['add', 'remove'],
	}
	for x in actions: 
		actions['all'].extend(actions[x])

	for category in ['utilities','fun']:
		for command in list(cmds._c_[category][1]):
			keys['disabled']['valid'].append(command)
