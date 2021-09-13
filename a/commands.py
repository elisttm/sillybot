
legend = {
	"<param>": "variable parameter",
	"[params]": "multiple types of parameters",
	"sub1/sub2/sub3": "subcommand parameters",
	"*param(s)": "optional parameter(s) that can be left blank",
}

_c_ = {
	'general': [
		"basic commands for basic functions", {
			'help':
				['help', "provides the list of commands"],
			'about':
				['about', "provides information about trashbot"],
	}],
	'utilities': [
		"helpful utility commands", {
			'ping': 
				['ping', "tests trashbots latency"],
			'server':
				['server', "provides information about the current server"],
			'user':
				['user <*user>', "provides information about a given user"],
			'avatar':
				['avatar <*user>', "provides the avatar of the given user"],
			'emote':
				['emote <emoji>', "sends the full image of the given emote", ['e', 'emote']],
			'clear':
				['clear <number>', "purges the specified number of messages"],
			'massnick':
				['massnick [<nickname>/reset/undo/cancel]', "modifies the nicknames of everyone in the server; 'reset' removes all nicknames, 'undo' attempts to undo the last massnick, 'cancel' cancels any massnicks in progress", None, "server admins only"],
	}],
	'fun': [
		"miscellaneous silly commands", {
			'say':
				['say <message>', "has trashbot repeat the provided message"],
			'echo':
				['echo <channel> <message>', "has trashbot remotely repeat the given message to the given channel"],
			'urban':
				['urban <word>', "sends the urban dictionary definition of the given word"],
			'cat':
				['cat [*<cat>/list]', "sends a random cat picture from the given directory"]
		},
	],
	'tags': [
		"commands related to trashbots tag system", {
			'tag':
				['tag [<subcommand>/<tag>]', "main command for all tag subcommands; inputting a tag mimics 'tag view'", ['t']],
			'tag view':
				['tag view <tag>', "provides the contents of a given tag"],
			'tag create':
				['tag create <tag> <content>', "creates a tag with the provided content", ['c']],
			'tag delete':
				['tag delete <tag>', "deletes a tag that you own", ['d']],
			'tag edit':
				['tag edit <tag> <content>', "applies the provided content to a tag you own", ['e']],
			'tag transfer':
				['tag transfer <tag> <user>', "transfers ownership of a tag you own to the given user", ['tr']],
			'tag owner':
				['tag owner <tag>', "provides the owner of the provided tag"],
			'tag list':
				['tag list <*user>', "sends a list of tags owned by a given user", ['ls']],
			'tag random':
				['tag random', "sends the contents of a randomly selected tag"],
		},
	],
	'customization': [
		"per server customization for trashbot", {
			'settings': 
				['settings <setting> <action> <params>', "command for managing the current servers config; [a:/docs/settings:link to documentation]", ['s'], "server admins only"],
	}],
}