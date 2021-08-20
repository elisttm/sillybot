# variables used for configuration settings

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
			"desc": "sets whether or not global tags can be used",
		},
	},
	
	"msgchannel": {
		"group": "messages",
		"type": "channel",
		"default": None, 
		"c": {
			"name": "message channel",
			"desc": "sets the channel that welcome/farewell messages get sent to",
		},
	},
			
	"joinmsg": {
		"group": "messages",
		"type": "text",
		"default": None, 
		"c": {
			"name": "greeting message",
			"desc": "sets the message that gets sent when a user joins the server",
			"maxlength": "50", "size": "25",
		},
	},
	
	"leavemsg": {
		"group": "messages",
		"type": "text",
		"default": None, 
		"c": {
			"name": "farewell message",
			"desc": "sets the message that gets sent when a user joins the server",
			"maxlength": "50", "size": "25",
		},
	},
	
	"autorole": {
		"group": "roles",
		"type": "role",
		"default": None, 
		"c": {
			"name": "default role",
			"desc": "sets the role that is assigned to people on join",
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
	
	"starboardchannel": {
		"group": "starboard",
		"type": "channel",
		"default": None, 
		"c": {
			"name": "starboard channel",
			"desc": "sets the channel used for starboard",
		},
	},
	
	"starboardcount": {
		"group": "starboard",
		"default": 5, 
		"type": "number", 
		"c": {
			"name": "starboard reaction number",
			"desc": "sets the number of reactions for the starboard",
			"max": 10,
		},
	},
}

default_settings = {}
for key in keys:
	default_settings[key] = keys[key]['default']

key_groups = {
	"basic": [],
	"commands": [],
	"roles": [],
	"messages": [],
	"starboard": [],
}

for key in keys:
	keyg = keys[key]['group']
	key_groups[keyg].append(key)

actions = []
value_actions = ['set', 'reset']
toggle_actions = ['enable', 'disable']
actions.extend(value_actions);actions.extend(toggle_actions)