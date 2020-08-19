# this file is used to store the names and descriptions of
# the bot's commands to be used in the 'help' command

class help_list():

	categories = {
		"general"		: "commands that provide basic functionality",
		"utilities"	: "commands that provide utility and display information",
		"fun"				: "commands that do fun stuff like post pictures of cats",
		"tags"			: "viewing and managing tags on the database",
		"admin"			: "various functions only usable by trashbot's admins",
		"cogmanager": "extension management; only usable by trashbot's admins",
	}


	general = {
		"help"		 	: "lists trashbot's commands",
		"about"			: "provides useful bot info", 
	}
	utilities = {
		"ping"			: "sends trashbot's latency",
		"server"		: "gives info about the server",
		"user"			: "gives info about a user",
		"avatar"		: "sends the avatar of a user",
		"clear"			: "deletes a specified number of messages",
		"prefix"		: "allows server admins to set or remove a custom prefix",
	}
	fun = {
		"say"				: "makes trashbot say a specified message", 
		"iphone"		: "iphone winning",
		"android"		: "android losing",
		"randomcat"	: "sends a random picture of a cat; also includes the commands 'tommy', 'floppa', 'gloop', 'nori', 'mish', 'lucas'",
	#	"tommy"			: "sends a random picture of tommy",
	#	"floppa"		: "sends a random big floppa image",
	#	"gloop"			: "sends a random gloop aesthetic cat",
	#	"nori"			: "sends a random picture of nori (squidds cat)",
	#	"mish"			: "sends a random picture of mish (peters cat)",
	#	"lucas"			: "sends a random picture of lucas (sharpz cat)",
	}
	tags = {
		"tag"				: "sends the content of the provided tag or allows management of tags using the below subcommands",
		"create"		: "creates a tag (create [tag name] [tag contents])",
		"delete"		: "deletes a tag that you own (delete [tag name])",
		"owner"			: "returns the owner of the provided tag (owner [tag name])",
		"list"			: "gives a list of tags owned by a user (list [@user])",
		"random"		: "returns a random tag from the database",
	}
	admin = { 
		"admins"		: "lists all of trashbot's admins",
		"presence"	: "changes trashbot's playing status",
		"massnick"	: "changes the nickname of everyone on the server",
		"echo"			: "makes trashbot echo a message to a provided channel ID",
		"restart"		: "restarts the bot",
	}
	cogmanager =  {
		"load"			: "loads a specified cog",
		"unload"		: "unloads a specified cog", 
		"reload"		: "reloads all cogs or a specified cog; ",
		"cogs"			: "lists all loadable cogs and their statuses", 
	}


	commands = {
		"general" 	: general,
		"utilities"	: utilities,
		"fun"				: fun,
		"tags"			: tags,
		"admin"			: admin,
		"cogmanager": cogmanager,
	}
