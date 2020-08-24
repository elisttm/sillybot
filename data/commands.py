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
			'description'	: "helpful utility/informative commands",
			
			'commands': {
				'ping' : "sends the bot's latency",
				'server' : "provides info about the current server",
				'user <user>' : "provides info about a given user",
				'avatar <user>' : "provides the avatar of a given user",
				'clear <amount>' : "deletes a specified number of messages",
				'massnick <nickname/reset>' : "changes the nickname of everyone in the server (server admins only)",
				'prefix <set/remove> <prefix>' : "allows management of a custom server prefix (server admins only)",
			
			}
		},

		'fun': {
			'description'	: "fun commands for games or whatever",
			
			'commands': {
				'say <message>' : "makes trashbot say a specified message", 
				
			}
		},

		'cats': {
			'description': "commands for random pictures of funny cats",
			
			'commands': {
				'cat' : "sends a random picture of any cat",
				'tommy' : "sends a random picture of tommy (zeebrongis' cat)",
				'floppa' : "sends a random image of big floppa",
				'gloop' : "sends a random gloop aesthetic cat",
				'nori' : "sends a random picture of nori (squidd's cat)",
				'mish' : "sends a random picture of mish (peter's cat)",
				'lucas' : "sends a random picture of lucas (sharpz's cat)",
			
			}
		},
		
		'tags': {
			'description'	: "viewing and management of tags in the database",
			
			'commands': {
				'tag <tag>' : "sends the content of the provided tag",
				'tag create <tag> <contents>' : "creates a tag with the given name and content",
				'tag remove <tag>' : "deletes a tag that you own",
				'tag edit <tag> <contents>' : "updates the contents of a tag you own",
				'tag transfer <tag> <user>' : "transfers ownership of a tag you own to a specified user",
				'tag owner <tag>' : "provides the owner of the given tag",
				'tag list <user>' : "gives a list of tags owned by a user",
				'tag random' : "returns a random tag from the database",
				'*tag forceremove <tag>' : "deletes the specified tag from the database",
				'*tag forcetransfer <tag> <user>' : "forcefully gives ownership of a tag to a specified user"
			}
		},

		'admin': { 
			'description'	: "various bot functions restricted to bot admins",
			
			'commands': {
				'admins' : "lists all of trashbot's admins",
				'*presence <text>' : "changes trashbot's playing status",
				'*echo <channel> <message>' : "makes trashbot echo a message to a provided channel ID",
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
				'*reload <cog>' : 'reloads all cogs or a specified cog; ',
				
			}
		}
	}