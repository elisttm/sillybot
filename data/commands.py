# this file is used to store the names and descriptions of
# the bot's commands to be used in the 'help' command


categories = {
	"general"		: "commands that provide basic functionality",
	"utilities"	: "commands that provide utility and display information",
	"fun"				: "commands that do fun stuff like post pictures of cats",
	"moderation": "basic moderation commands",
	"admin"			: "various functions only usable by trashbot's admins",
	"cogmanager": "extension management; only usable by trashbot's admins",
}

#			======	commands	======

general = {
	"help"		 	: "lists trashbot's commands",
	"about"			: "provides useful bot info", 
}
utilities = {
	"ping"			: "sends trashbot's latency",
	"server"		: "gives info about the server",
	"user"			: "gives info about a user",
	"avatar"		: "sends the avatar of a user",
	"emote"			: "sends the url of a provided emote",
#	"report"		: "sends a message report to trashbot's owner",
}
fun = {
	"say"				: "makes trashbot say a specified message", 
	"iphone"		: "iphone winning",
	"android"		: "android losing",
	"tommy"			: "sends a random tommy picture",
	"floppa"		: "sends a random floppa",
	"gloop"			: "sends a random gloop cat"
}
moderation = {
	"clear"			: "deletes a specified number of messages",
}
admin = { 
	"admins"		: "lists all of trashbot's admins",
	"presence"	: "changes trashbot's playing status",
	"nick"			: "changes trashbot's nickname", 
	"massnick"	: "changes the nickname of everyone on the server",
	"restart"		: "restarts the bot",
	"echo"			: "makes trashbot echo a message to a provided channel ID"
}
cogmanager =  {
	"load"			: "loads a specified cog",
	"unload"		: "unloads a specified cog", 
	"reload"		: "reloads all cogs or a specified cog; ",
	"list"			: "lists all loadable cogs and their statuses", 
}

#			========================

commands = {
  "general" 	: general,
  "utilities"	: utilities,
	"fun"				: fun,
  "moderation": moderation,
	"admin"			: admin,
	"cogmanager": cogmanager,
}
