# trashbot 

trashbot is a simple but useful discord bot written in python using the discord.py api wrapper

more info and important links are on [my website](https://elisttm.space/trashbot)

---  

### essential packages

* **discord.py** (api wrapper used for all interactions with discord)
* **pymongo** (mongodb driver for database stuff)

### file structure

since my file organization is always really convoluted, heres a rundown of where and what everything is
|||
|--|--|
| /a/ | files that store globally accessed data;  *constants.py* stores important variables, *funcs.py* stores functions, *checks.py* has command checks, *commands.py* stores the command list, and *configs.py* stores stuff for customization |
| /cogs/ | organized discord command modules that can be easily loaded and unloaded; i use this system to make my life way way easier |
| /stuff/ | for any files that arent explicitly code, like images or temporary .txt files  |