# Left-4-Dead-2-assistant
A quality of life tool for Left 4 Dead 2. Find potential hackers early, find available servers in desired locations and record and view chat logs to name a few functions.

-condebug must be enabled in the launch options (click properties on the Left 4 Dead 2 file on steam)
![image](https://github.com/JackLacey18/Left-4-Dead-2-hacker-finder/assets/94805552/16b090f0-cd6d-4b49-85f2-452df00336f4)

This will create the console.log file that can be parsed. The log will be located in a path similar to below.
"C:\Program Files (x86)\Steam\steamapps\common\Left 4 Dead 2\left4dead2\console.log"

Ensure the correct file path of the console.log file is stored in the console_file_path.txt file.

The script is to be run in command line. Navigate to the location you have stored the files and run the script.

The script is fully controllable from the developer console in Left 4 Dead 2. Type 'help' in the developer console for more information.
Here is the breakdown for what you can do with this script.

Type any of the following commands in the developer console.
* 'status'  -  Performs a background check on all players in the game.
* 'mm_dedicated_force_servers'  -  Checks for available servers and copies the first server available in order of EU North, EU West and US East servers.
* 'chat'  -  Prints part of the most recent chat logs.
* 'players'  -  Prints how long each player has been connected to the server.
* 'region'  -  Displays the preferred server region for the mm_dedicated_force_servers command.
* 'net_channels'  -  Manual server IP address finder in the event the script is executed after joining a game.
* 'address'  -  Prints the IP address of the server and copies it to the clipboard.
* 'server'  -  Prints server name and copies it to the clipboard.
* 'log_filepath'  -  Print the filepath defined in the console file path.txt file.

* (Automatic) #Cstrike_TitlesTXT_Game_connected  -  Alerts the user of a new player on CMD.
* (Automatic) Connected to  -  Stores the IP address of the server.
* (Automatic) Records chat in-game.
