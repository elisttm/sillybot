import a.commands as cmds
import a.constants as tt

keys = {
	"prefix": {
		"group": "basic",
		"type": "text",
		"default": "t!", 
		"c": {
			"name": "prefix",
			"desc": "changes the command prefix",	
			"max": "5", "size": "1",
		},
	},
	"disabled": {
		"group": "commands",
		"type": "list",
		"default": None,
		"valid": ['tags'],
		"c": {
			"name": "disabled commands",
			"desc": "disables commands added to the list",
			"separator": " "
		},
	},
	"msgchannel": {
		"group": "messages",
		"type": "channel",
		"default": None, 
		"c": {
			"name": "message channel",
			"desc": "channel where welcome/farewell messages are sent to",
		},
	},	
	"joinmsg": {
		"group": "messages",
		"type": "text",
		"default": None, 
		"c": {
			"name": "greeting message",
			"desc": "the message that gets sent when a user joins the server",
			"maxlength": "50", "size": "25",
		},
	},
	"leavemsg": {
		"group": "messages",
		"type": "text",
		"default": None, 
		"c": {
			"name": "farewell message",
			"desc": "the message that gets sent when a user joins the server",
			"maxlength": "50", "size": "25",
		},
	},
	"autorole": {
		"group": "roles",
		"type": "role",
		"default": None, 
		"c": {
			"name": "default role",
			"desc": "the role to assign to users when they join",
		},
	},
	"stickyroles": {
		"group": "roles",
		"type": "toggle",
		"default": False,
		"c": {
			"name": "stickyroles",
			"desc": "toggles saving and assigning roles when users leave/join",
		},
	},
	"starboard": {
		"group": "starboard",
		"type": "channel",
		"default": None, 
		"c": {
			"name": "starboard channel",
			"desc": "the channel used for the starboard",
		},
	},
	"starboardcount": {
		"group": "starboard",
		"type": "number", 
		"default": 5, 
		"c": {
			"name": "starboard reaction number",
			"desc": "the number of reactions for the starboard",
			"max": 10,
		},
	},
	#"starboardemoji": {
	#	"group": "starboard",
	#	"type": "emoji", 
	#	"default": tt.e.star, 
	#	"c": {
	#		"name": "starboard reaction emoji",
	#		"desc": "the emoji the starboard uses",
	#	},
	#},
}

value_types = ['text','number','channel','role']

actions = {
	'all': [],
	'value': ['set', 'reset'],
	'toggle': ['enable', 'disable'],
	'list': ['add', 'remove'],
}
for x in actions:
	actions['all'].extend(actions[x])

key_groups = {
	"basic": [],
	"commands": [],
	"roles": [],
	"messages": [],
	"starboard": [],
}

default_settings = {}
for key in keys:
	default_settings[key] = keys[key]['default']
	key_groups[keys[key]['group']].append(key)

for category in ['utilities','fun']: 
	keys['disabled']['valid'].extend(cmds._c_[category][1])
