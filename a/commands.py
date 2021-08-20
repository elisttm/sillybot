# variables used for the help command and error handler

perm_server_admin = "server admins only"
perm_bot_admin = "bot admins only"

_c_ = {
	'general': [
		"basic commands for basic functions",
		{
			'help': [
				'help', "provides the list of commands"
			],
			'about': [
				'about', "provides information about trashbot"
			],
		},
	],
	
	'utilities': [
		"helpful utility commands",
		{
			'ping': [
				'ping', "tests trashbot's latency"
			],
			'server': [
				'server', "provides information about the current server"
			],
			'user': [
				'user <user>', "provides information about a given user"
			],
			'avatar': [
				'avatar <user>', "provides the avatar of the given user"
			],
			'emote': [
				'emote <emoji>', "sends the full image of the given emote", ['e', 'emoji']
			],
			'clear': [
				'clear <number>', "purges the specified number of messages"
			],
			'massnick': [
				'massnick <nickname> OR [reset/undo/cancel]', "changes the nickname of everyone in the current server; the 'reset' subcommand removes everyones nicknames, 'undo' attempts to undo the last massnick", None, perm_server_admin
			],
		},
	],

	'fun': [
		"miscellaneous silly commands",
		{
			'say': [
				'say <message>', "has trashbot repeat the provided message"
			],
			'echo': [
				'echo <channel> <message>', "has trashbot remotely repeat the given message to the given channel"
			],
			'urban': [
				'urban <word>', "sends the urban dictionary definition of the given word"
			],
			'cat': [
				'cat <cat> OR [list]', "sends a random cat picture; you can use a folder as a subcommand to pick from it and use the 'list' subcommand to list folders"
			]
		},
	],

	'tags': [
		"commands related to trashbot's public tag system",
		{
			'tag': [
				'tag <subcommand> OR <tag>', "parent command to all the subcommands; putting a tag in place of a subcommand acts indentically to using the view subcommand", ['t']
			],
			'tag view': [
				'tag view <tag>', "provides the contents of the given tag"
			],
			'tag create': [
				'tag create <tag> <content>', "creates a tag with the given content if it doesn't already exist", ['c']
			],
			'tag delete': [
				'tag delete <tag>', "deletes a tag that you own", ['d']
			],
			'tag edit': [
				'tag edit <tag> <content>', "applies the provided content to a tag you own", ['e']
			],
			'tag transfer': [
				'tag transfer <tag> <user>', "transfers ownership of a tag you own to the given user", ['tr']
			],
			'tag owner': [
				'tag owner <tag>', "tells who owns the provided tag"
			],
			'tag list': [
				'tag list <user>', "sends a list of tags owned by a given user", ['ls']
			],
			'tag listall': [
				'tag listall', "sends a list of every public tag"
			],
			'tag random': [
				'tag random', "randomly chooses a tag from the database and sends its contents"
			],
			'tag forceedit': [
				'tag forceedit <tag> <content>', "applies the provided content to the given tag regardless of ownership", ['fe'], perm_bot_admin
			],
			'tag forceremove': [
				'tag forceremove <tag>', "deletes the given tag regardless of ownership", ['fr'], perm_bot_admin
			],
			'tag forcetransfer': [
				'tag forcetransfer <tag> <user>', "transfers the given tag to the given user regardless of ownership", ['ft'], perm_bot_admin
			],
		},
	],

	'customization': [
		"per server customization for trashbot",
		{
			'settings': [
				'settings <setting> <action> <params>', "command for managing the current server's config; documentation can be found [a:/docs/settings:here]", ['s'], perm_server_admin
			],
		},
	],

	'admin': [
		"various bot functions exclusive to bot admins",
		{
			'presence': [
				'presence <text>', "changes trashbot's playing status to the provided text", None, perm_bot_admin
			],
			'blacklist': [
				'blacklist <user>', "toggles the given user's ability to use trashbot", None, perm_bot_admin
			],
			'shutdown': [
				'shutdown', "shuts trashbot down and closes the connection", None, perm_bot_admin
			],
			'restart': [
				'about', "restarts trashbot", None, perm_bot_admin
			],
			'cogs': [
				'cogs', "provides a list of cogs", None, perm_bot_admin
			],
			'load': [
				'load <cog>', "loads the specified cog", None, perm_bot_admin
			],
			'unload': [
				'unload <cog>', "unloads the specified cog", None, perm_bot_admin
			],
			'reload': [
				'reload <cog>', "reloads the specified cog; leave empty to reload all cogs", None, perm_bot_admin
			],
		},
	],
}