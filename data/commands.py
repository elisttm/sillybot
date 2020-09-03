class help_list():
	
	#	command <param1> <param2>
	#	command <param1a> <param1b> OR <param2>

	#	*command : command usable by trashbot admins/owners only

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
				'ping' : "gives trashbots command latency",
				'server' : "gives information about a server",
				'user <user>' : "gives information about a user",
				'avatar <user>' : "provides the avatar of a given user",
				'mcserver' : "gives information about the elisttm minecraft server",
				'clear <amount>' : "deletes a specified number of messages",
				'massnick <nickname> OR "reset"' : "changes the nickname of everyone in the server (server admins only)",
				'prefix set <prefix> OR "reset"' : "allows management of a custom server prefix (server admins only)",
			}
		},

		'fun': {
			'description'	: "fun commands for games or whatever",
			'commands': {
				'say <message>' : "makes trashbot say a specified message", 
				'urban <word>' : "gets the urban dictionary definition of the given word",
				'urbanshit <word>' : "gets the urban dictionary definition of the given word using a really bad parser",
			}
		},

		'cats': {
			'description': "commands for random pictures of funny cats (images fetched from my personally hosted cat api)",
			'commands': {
				'cat <cat>' : "sends a random cat picture (all other cat commands are aliases of this one)",
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
				'tag <tag>' : "sends the content of the provided tag",
				'tag create <tag> <contents>' : "creates a tag with the given name and content",
				'tag remove <tag>' : "deletes a tag that you own",
				'tag edit <tag> <contents>' : "updates the contents of a tag you own",
				'tag transfer <tag> <user>' : "transfers ownership of a tag you own to a specified user",
				'tag owner <tag>' : "provides the owner of the given tag",
				'tag list <user>' : "gives a list of tags owned by a user",
				'tag listall' : "gives a list of every tag in the database",
				'tag random' : "returns a random tag from the database",
				'*tag forceremove <tag>' : "forcefully deletes the specified tag from the database",
				'*tag forceedit <tag> <content>' : "forcefully edits a tag with the given contents",
				'*tag forcetransfer <tag> <user>' : "forcefully gives ownership of a tag to a specified user"
			}
		},

		'admin': { 
			'description'	: "various bot functions restricted to bot admins",
			'commands': {
				'admins' : "lists all of trashbot's admins",
				'*presence <text>' : "changes trashbot's playing status",
				'*echo <channel ID> <message>' : "makes trashbot echo a message to a provided channel ID",
				'*shutdown' : "logs out and shuts down the bot",
				'*restart' : "restarts the bot",
			}
		},

		'cogmanager': {
			'description'	: "extension management for debugging or whatever",	
			'commands': {
				'cogs' : 'lists all loadable cogs and their statuses', 
				'*load <cog>' : 'loads a specified cog',
				'*unload <cog>' : 'unloads a specified cog', 
				'*reload <cog>' : 'reloads all cogs or a specified cog',
			}
		}
	}