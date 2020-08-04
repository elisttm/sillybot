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


general = {
	"help"		 	: "lists trashbot's commands",
	"about"			: "provides useful bot info", 
}
utilities = {
	"ping"			: "sends trashbot's latency",
	"server"		: "gives info about the server",
	"user"			: "gives info about a user",
	"avatar"		: "sends the avatar of a user",
}
fun = {
	"say"				: "makes trashbot say a specified message", 
	"iphone"		: "iphone winning",
	"android"		: "android losing",
	"randomcat"	: "sends a random picture of a cat",
	"tommy"			: "sends a random picture of tommy",
	"floppa"		: "sends a random big floppa image",
	"gloop"			: "sends a random gloop aesthetic cat",
	"nori"			: "sends a random picture of nori (squidds cat)",
	"mish"			: "sends a random picture of mish (peters cat)",
	"lucas"			: "sends a random picture of lucas (sharpz cat)",
}
moderation = {
	"clear"			: "deletes a specified number of messages",
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
  "moderation": moderation,
	"admin"			: admin,
	"cogmanager": cogmanager,
}
