import a.commands as cmds

# variables for server configuration settings

disable_commands = ['tags',]
for category in ['utilities','fun']: 
	disable_commands.extend(cmds._c_[category])

actions = {
	'value': ['set', 'reset'],
	'toggle': ['enable', 'disable'],
	'list': ['add', 'remove'],
}

all_actions = []
all_actions.extend(actions['value'])
all_actions.extend(actions['toggle'])
all_actions.extend(actions['list'])

value_types = ['text','number','channel','role']

key_groups = {
	"basic": [],
	"commands": [],
	"roles": [],
	"messages": [],
	"starboard": [],
}

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
	
	"globaltags": {
		"group": "commands",
		"type": "toggle",
		"default": True, 
		"c": {
			"name": "global tags",
			"desc": "toggles if the tag command can be used",
		},
	},

	"disable": {
		"group": "commands",
		"type": "list",
		"default": None,
		"valid": disable_commands,
		"c": {
			"name": "disabled commands",
			"desc": "disables commands added to the list",
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
			"desc": "toggles saving and assigning roles after leaving/joining",
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
}

default_settings = {}
for key in keys:
	default_settings[key] = keys[key]['default']

for key in keys:
	keyg = keys[key]['group']
	key_groups[keyg].append(key)