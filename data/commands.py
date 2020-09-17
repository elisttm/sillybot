class cmdl():

	ctgs = {
		'general': {
			'desc': "basic commands for basic functions",
			'cmds': {
				'help': {
					'usage': "help",
					'desc': "links to this list of commands",
				},
				'about': {
					'usage': "about",
					'desc': "provides useful bot info", 
				},
			},
		},
		'utilities': {
			'desc': "helpful commands for information and/or utility",
			'cmds': {
				'ping': {
					'usage': "ping",
					'desc': "gives trashbots latency",
				},
				'server': {
					'usage': "server <server>",
					'desc': "gives information about a server",
				},
				'user': {
					'usage': "user <user>",
					'desc': "gives information about a user",
				},
				'avatar': {
					'usage': "avatar <user>",
					'desc': "sends the avatar of a given user",
				},
				'emote' : {
					'usage': "emote <emote>",
					'desc': "sends the image of the provided custom emoji",
					'aliases': ['e','emoji']
				},
				'mcserver': {
					'usage': "mcserver",
					'desc': "gives information about the elisttm minecraft server",
				},
				'clear': {
					'usage': "clear <amount>",
					'desc': "deletes a specified number of messages",
				},
				'massnick': {
					'usage': "massnick <nickname> OR reset/revert",
					'desc': "changes the nickname of everyone in the server (server admins only)",
				},
			},
		},
		'fun': {
			'desc': "fun commands for games or whatever",
			'cmds': {
				'say': {
					'usage': "say <message>",
					'desc': "makes trashbot repeat a message", 
				},
				'echo': {
					'usage': "echo <channel> <message>",
					'desc': "makes trashbot repeat a message to a channel",
					'perms': "(server/bot admins only)",
				},
				'urban': {
					'usage': "urban <word>",
					'desc': "gets the urban dictionary definition of the given word",
				},
				'penis': {
					'usage': "penis <user>",
					'desc': "gets a users penis size",
				},
				'penisrank': {
					'usage': "penisrank top/bottom",
					'desc': "ranks the biggest or smallest penis sizes in the current guild",
				},
			},
		},
		'cats': {
			'desc': "commands for random pictures of funny cats (images fetched from my personally hosted cat api)",
			'cmds': {
				'cat': {
					'usage': "cat <cat> OR cat list",
					'desc': "sends a random cat picture from the provided directory. the commands 'tommy', 'floppa', 'gloop', 'nori', 'mish', 'lucas', 'marley', and 'spock' are aliases of this one using different parameters",
				},
			},
		},
		'tags': {
			'desc': "commands and subcommands related to trashbots tag database",
			'cmds': {
				'tag': {
					'usage': "tag <subcommand> OR tag <tag>",
					'desc': "main command of all other tag commands, alias for 'tag view'",
					'aliases': ['t'],
				},
				'view': {
					'usage': "tag view <tag>",
					'desc': "sends the content of the provided tag",
				},
				'create': {
					'usage': "tag create <tag> <contents>",
					'desc': "creates a tag with the given name and content",
					'aliases': ['c'],
				},
				'remove': {
					'usage': "tag remove <tag>",
					'desc': "deletes a tag that you own",
					'aliases': ['r'],
				},
				'edit': {
					'usage': "tag edit <tag> <contents>",
					'desc': "updates the contents of a tag you own",
				},
				'transfer': {
					'usage': "tag transfer <tag> <user>",
					'desc': "transfers ownership of a tag you own to a specified user",
				},
				'owner': {
					'usage': "tag owner <tag>",
					'desc': "provides the owner of the given tag",
				},
				'list': {
					'usage': "tag list <user>",
					'desc': "gives a list of tags owned by a user",
				},
				'listall': {
					'usage': "tag listall",
					'desc': "gives a list of every tag in the database",
				},
				'random': {
					'usage': "tag random",
					'desc': "returns a random tag from the database",
				},
				'forceremove': {
					'usage': "tag forceremove <tag>",
					'desc': "forcefully deletes the specified tag from the database",
					'perms': "(bot admins only)",
					'aliases': ['fr'],
				},
				'forceedit': {
					'usage': "tag forceedit <tag> <content>",
					'desc': "forcefully edits a tag with the given contents",
					'perms': "(bot admins only)",
					'aliases': ['fe'],
				},
				'forcetransfer': {
					'usage': "tag forcetransfer <tag> <user>",
					'desc': "forcefully gives ownership of a tag to a specified user",
					'perms': "(bot admins only)",
					'aliases': ['ft'],
				},
			},
		},
		'customization': {
			'desc': "per server customization for the bot ",
			'cmds': {
				'settings': {
					'usage': "settings <setting> <action> <param>",
					'desc': "main command used for per server configuration management",
					'perms': "(server/bot admins only)",
					'aliases': ['s'],
				},
			},
		},
		'admin': { 
			'desc': "various bot functions restricted to bot admins",
			'cmds': {
				'admins': {
					'usage': "admins",
					'desc': "lists all of trashbot's admins",
				},
				'presence': {
					'usage': "presence <text>",
					'desc': "changes trashbot's playing status",
					'perms': "(bot admins only)",
				},
				'blacklist': {
					'usage': "blacklist <user>",
					'desc': "blacklists/unblacklists users from using trashbot's commands",
					'perms': "(bot admins only)",
				},
				'shutdown': {
					'usage': "shutdown",
					'desc': "logs out and shuts down the bot",
					'perms': "(bot admins only)",
				},
				'restart': {
					'usage': "restart",
					'desc': "restarts the bot",
					'perms': "(bot admins only)",
				},
			},
		},
		'cogmanager': {
			'desc': "extension management for debugging or whatever",	
			'cmds': {
				'cogs': {
					'usage': "cogs",
					'desc': "lists all loadable cogs and their statuses",
				},
				'load': {
					'usage': "load <cog>",
					'desc': "loads a specified cog",
					'perms': "(bot admins only)",
				},
				'unload': {
					'usage': "unload <cog>",
					'desc': "unloads a specified cog", 
					'perms': "(bot admins only)",
				},
				'reload': {
					'usage': "reload <cog>",
					'desc': "reloads all cogs or a specified cog",
					'perms': "(bot admins only)",
				},
			},
		}
	}