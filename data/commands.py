class help_list():

	categories = {

		'general': {
			'description'	: "basic commands for basic functions",
			'commands': {
				'help'		 	: "links to this list of commands",
				'about'			: "provides useful bot info", 
			}
		},

		'utilities': {
			'description'	: "helpful commands for information and/or utility",
			'commands': {
				'ping' : "gives trashbots latency",
				'server' : "gives information about a server",
				'user <user>' : "gives information about a user",
				'avatar <user>' : "provides the avatar of a given user",
				'mcserver' : "gives information about the elisttm minecraft server",
				'clear <amount>' : "deletes a specified number of messages",
				'massnick <nickname> OR massnick reset' : "changes the nickname of everyone in the server (server admins only)",
			}
		},

		'fun': {
			'description'	: "fun commands for games or whatever",
			'commands': {
				'say <message>' : "makes trashbot say a specified message", 
				'echo <channel> <message>' : "makes trashbot echo a message to a provided channel (server admin only)",
				'urban <word>' : "gets the urban dictionary definition of the given word",
				'penis <user>' : "gets a users penis size",
				'penisrank <top/bottom>' : "ranks the biggest or smallest penis sizes in the current guild",
			}
		},

		'cats': {
			'description': "commands for random pictures of funny cats (images fetched from my personally hosted cat api)",
			'commands': {
				'cat <cat>' : "sends a random cat picture",
				'tommy' : "sends a random picture of tommy (zeebrongis' cat)",
				'floppa' : "sends a random image of big floppa",
				'gloop' : "sends a random gloop aesthetic cat",
				'nori' : "sends a random picture of nori (squidd's cat)",
				'mish' : "sends a random picture of mish (peter's cat)",
				'lucas' : "sends a random picture of lucas (sharpz's cat)",
				'marley' : "sends a random picture of marley (fluffer's cat)",
				'spock' : "sends a random picture of spock (fluffer's cat)",
			}
		},

		'tags': {
			'description'	: "commands related to trashbots tag database",
			'commands': {
				'tag <subcommand> OR <tag>' : "sends the content of the provided tag",
				'create <tag> <contents>' : "creates a tag with the given name and content",
				'remove <tag>' : "deletes a tag that you own",
				'edit <tag> <contents>' : "updates the contents of a tag you own",
				'transfer <tag> <user>' : "transfers ownership of a tag you own to a specified user",
				'owner <tag>' : "provides the owner of the given tag",
				'list <user>' : "gives a list of tags owned by a user",
				'listall' : "gives a list of every tag in the database",
				'random' : "returns a random tag from the database",
				'forceremove <tag>' : "forcefully deletes the specified tag from the database",
				'forceedit <tag> <content>' : "forcefully edits a tag with the given contents",
				'forcetransfer <tag> <user>' : "forcefully gives ownership of a tag to a specified user"
			}
		},

		'customization': {
			'description' : "per server customization for the bot",
			'commands': {
				'settings <setting> <action> <param>': "management and viewing of trashbots configuration",
			}
		},

		'admin': { 
			'description'	: "various bot functions restricted to bot admins",
			'commands': {
				'admins' : "lists all of trashbot's admins",
				'presence <text>' : "changes trashbot's playing status",
				'blacklist <user>' : "blacklists/unblacklists users from using trashbot's commands",
				'shutdown' : "logs out and shuts down the bot",
				'restart' : "restarts the bot",
			}
		},

		'cogmanager': {
			'description'	: "extension management for debugging or whatever",	
			'commands': {
				'cogs' : 'lists all loadable cogs and their statuses', 
				'load <cog>' : 'loads a specified cog',
				'unload <cog>' : 'unloads a specified cog', 
				'reload <cog>' : 'reloads all cogs or a specified cog',
			}
		}
	}