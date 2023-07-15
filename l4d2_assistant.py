'''
This is a CMD tool which can be completely controlled from the Left 4 Dead 2 console.

-condebug must be enabled in the launch options (click properties on the Left 4 Dead 2 file on steam).

For full functionality, type help in the l4d2 console to find more information.
'''
if __name__ == '__main__':
    # Imports
    import requests
    import bs4
    from steamid_converter import Converter
    import time
    import os
    from sourceserver.sourceserver import SourceServer
    import pyperclip
    from tqdm import tqdm
    import humanize
    import datetime
    
    with open('console file path.txt','r') as file:
        path = file.readlines()[0]

    ip_address = 'None'
    in_game = False
    with open(path,'w') as file:
        file.write('')

    # User defined servers
    servers = {
                # EU North (Sweden)
                'EU North': ['155.133.252.109:27178',
                '155.133.252.121:27161',
                '155.133.252.109:27181',
                '155.133.252.109:27102',
                '155.133.252.122:27117',
                '155.133.252.122:27160'],
                # EU West (Various)
                'EU West': ['155.133.226.125:27279',
                '155.133.226.125:27219',
                '155.133.226.125:27293',
                '155.133.226.125:27084',
                '155.133.226.125:27308',
                '155.133.226.125:27226',
                '155.133.226.125:27235',
                '89.163.187.138:27015',
                '108.61.122.198:27015',
                '155.133.226.125:27028'],
                # US East
                'US East': ['162.254.192.132:27193',
                '68.232.179.197:27015']
                }


    # Start of program.
    while True:
        # Check for status command input into L4D2 console
        file = open(path,'r',encoding='utf-8', errors='ignore')
        logfile = [i for i in file.readlines()]
        for log in logfile:

            ##########################################################################################################################################
            # Help function
            if 'Usage:  help <cvarname>' in log:
                with open(path,'w') as file:
                    file.write('')
                print('Available functions on l4d2 console:')
                print('')
                print('status  -  Performs a background check on all players in the game.')
                print('')
                print('mm_dedicated_force_servers  -  Checks for available servers and copies the first server available in order of EU North, EU West and US East servers.')
                print('')
                print('chat  -  Prints part of the most recent chat logs.')
                print('')
                print('players  -  Prints how long each player has been connected to the server.')
                print('')
                print('(Automatic) #Cstrike_TitlesTXT_Game_connected  -  Alerts the user of a new player on CMD.')
                print('')
                print('(Automatic) Connected to  -  Stores the IP address of the server.')
                print('')
                print('region  -  Displays the preferred server region for the mm_dedicated_force_servers command.')
                print('')
                print('net_channels  -  Manual server IP address finder.')
                print('')
                print('address  -  Prints the IP address of the server and copies it to the clipboard.')
                print('')
                print('server  -  Prints server name and copies it to the clipboard.')
                print('')
                print('log_filepath  -  Print the filepath defined in the console file path.txt file.')
                print('')
                print('settings  -  change various settings.')
                print('')
                print('Sleeping for 20 seconds...')
                print('')
                for second in tqdm(range(20)):
                    time.sleep(1)

            ##########################################################################################################################################
            # Print the location of the console.log file defined in the text file 'console file path.txt'.
            elif 'Unknown command "log_filepath"' in log or 'Unknown command: log_filepath' in log:
                print(path)
                with open(path,'w') as file:
                    file.write('')
                time.sleep(10)

            ##########################################################################################################################################
            # Manual IP address finder using net_channels command in l4d2 console.
            elif '- remote IP' in log:
                ip_address = log.split(' ')[-1]
                print('Connected to:',ip_address)
                time.sleep(3)
                in_game = True
                srv = SourceServer(ip_address)
                srv.close()
                with open(path,'w') as file:
                    file.write('')
            ##########################################################################################################################################
            # Find IP address when joining a game.
            elif 'Connected to' in log:
                ip_address = log.split(' ')[-1]
                print('Connected to:',ip_address)
                time.sleep(3)
                in_game = True
                srv = SourceServer(ip_address)
                srv.close()
                with open(path,'w') as file:
                    file.write('')

            ##########################################################################################################################################
            # Print and copy IP address of server.
            elif 'Unknown command: address' in log and in_game == True:
                print('IP address:',ip_address)
                print('Copied to clipboard.')
                pyperclip.copy(ip_address)
                time.sleep(5)
                with open(path,'w') as file:
                    file.write('')

            ##########################################################################################################################################
            # New player alert.
            elif '#Cstrike_TitlesTXT_Game_connected' in log:
                try:
                    srv = SourceServer(ip_address)
                    players = [i[1] for i in srv.getPlayers()[1]]
                    connection_times = [i[3] for i in srv.getPlayers()[1]]
                    srv.close()
                    new_player = players[connection_times.index(min(connection_times))]
                    for i in range(50):
                            print('Incoming player',new_player)
                except:
                    print('No defined IP address for the server, type net_channels in the console and retry.')
                    time.sleep(5)
                with open(path,'w') as file:
                    file.write('')
                time.sleep(3)

            ##########################################################################################################################################
            # Print and copy server name.
            elif 'Unknown command: server' in log:
                try:
                    srv.retry()
                    print(srv.info['name'])
                    pyperclip.copy(srv.info['name'])
                    print('Server name copied to clipboard.')
                    time.sleep(5)
                except:
                    try:
                        print('Retry failed, starting a new connection...')
                        time.sleep(2)
                        srv = SourceServer(ip_address)
                        print(srv.info['name'])
                        pyperclip.copy(srv.info['name'])
                        print('Server name copied to clipboard.')
                        time.sleep(5)
                    except:
                        print('No defined IP address for the server, type net_channels in the console and retry.')
                        time.sleep(5)
                with open(path,'w') as file:
                    file.write('')

            ##########################################################################################################################################
            # Print players and their connection time to the server.
            elif 'Unknown command: players' in log:
                try:
                    srv = SourceServer(ip_address)
                    players = zip([i[1] for i in srv.getPlayers()[1]],[i[3] for i in srv.getPlayers()[1]])
                    srv.close()
                    for player in players:
                        print('')
                        print(' ',player[0],':',humanize.naturaldelta(datetime.timedelta(seconds=float(player[1]))))
                    with open(path,'w') as file:
                        file.write('')
                    time.sleep(10)
                    
                except:
                    print('No defined IP address for the server, type net_channels in the console and retry.')
                    time.sleep(5)

            ##########################################################################################################################################
            # Chat log.
            elif ' : ' in log:
                if 'players :' not in log:
                    if 'version :' not in log:
                        if 'udp/ip  :' not in log:
                            if 'os      :' not in log:
                                if 'map     :' not in log:
                                    if 'Opened Steam Socket' not in log:
                                        if 'ms :' not in log:
                                            with open("chat.txt",'r') as file:
                                                chat = file.readlines()
                                            with open('chat.txt','a') as file:
                                                file.write(log + '\n')
                                            with open(path,'w') as file:
                                                    file.write('')

            ##########################################################################################################################################
            # Print the chat.
            elif 'Unknown command: chat' in log or 'Unknown command: "chat"' in log:
                with open("chat.txt",'r') as file:
                    chat = [i.strip() for i in file.readlines()]
                chat = [i for i in chat if i != '']
                if len(chat) > 65:
                    for message in chat[-60:]:
                        print(message)
                else:
                    for message in chat:
                        print(message)
                with open(path,'w') as file:
                        file.write('')
                time.sleep(15)

            ##########################################################################################################################################
            # Player background checker.
            elif 'hostname:' in log:
                index = logfile.index(log)
                logfile = logfile[index:]
                with open(path,'w') as file:
                    file.write('')

                # Parse the log to find SteamIDs and convert them into useable profile URLs.
                playerURLs = []
                no_dupes = []
                for log in logfile:
                    split_list = log.split(' ')
                    for i in split_list:
                        if 'STEAM_' in i:
                            if i not in no_dupes:
                                no_dupes.append(i)
                                playerURLs.append('https://steamcommunity.com/profiles/' + str(Converter.to_steamID64(i)))

                # Enter the URL of the player's profile page.
                for url in playerURLs:
                    if url[-1] !='/':
                        url = str(url) + '/'

                    # Appending the url to a permenant file.
                    with open('steam_player_urls.txt','r') as file:
                        existing_data = list(file.readlines())
                    if url + '\n' not in existing_data:
                        with open('steam_player_urls.txt','a') as file:
                            file.write(url + '\n')
                        file.close()
                    try:
                        # Making the request and creating the soup.
                        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"} 
                        request = requests.get(str(url) + 'allcomments',headers=headers)
                        soup = bs4.BeautifulSoup(request.content,'lxml')

                        # Parsing for the name of the player.
                        name = [i.text.strip() for i in soup.find_all('a',class_='whiteLink persona_name_text_content')][0]

                        # Parsing the soup for authors and their comments.
                        authors = [''.join(''.join(''.join(i.text.strip().split('\t')).split('\n')).split('\r')) for i in soup.find_all('div',class_='commentthread_comment_author')]
                        text = [''.join(''.join(''.join(i.text.strip().split('\t')).split('\n')).split('\r')) for i in soup.find_all('div',class_='commentthread_comment_text')]
                        comments = list(zip(authors,text))

                        # Sentiment analysis.
                        text = ''
                        number_of_comments = 0
                        for i in comments:
                            number_of_comments += 1
                            text = text + str(i[1] + ' ')
                        text = text.lower()

                        sentiment_dictionary = {

                        'Cheater mentions' : ['cheat','cheating','cheats','cheatz','cheater',
                                   'hack','hacking','hacks','hackz','hax','hacker',
                                   'script','scripting','scripts','scriptz','scripter',
                                   'aimbot','wallhacks','wallhackz'],

                        'Ragequit mentions' : ['rq','ragequit','rage','rage quit','rusher'],

                        '-Rep mentions' : ['-rep'],

                        'Troll mentions':  ['troll','trolls','trolling',
                                            'suicide','suicides',
                                            'grief','griefer','griefing','griefs'],

                        'Racism mentions' : ['racist','racism']
                        }

                        sentiment_list = []
                        for key in sentiment_dictionary:
                            words = sentiment_dictionary.get(key)
                            count = 0
                            for word in words:
                                count += text.count(word)
                            if count > 1:
                                sentiment_list.append(str(key) + ': '+ str(count))

                        # VAC ban check.
                        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"} 
                        request = requests.get(url,headers=headers)
                        soup = bs4.BeautifulSoup(request.content,'lxml')
                        VAC_ban = [''.join(''.join(i.text.strip().split('\t')).split('\n\r\n')) for i in soup.find_all('div',class_='profile_ban_status')]

                        # Private check.
                        private_check = [i.text.strip() for i in soup.find_all('div', class_='profile_private_info')]

                        # Begin joining the results starting with the player's name.
                        print(' ' + name )

                        # Private check.
                        if len(private_check) > 0:
                            print(' ' + str(private_check[0]))

                        # VAC ban.
                        if len(VAC_ban) > 0:
                            ban = str(VAC_ban[0])
                        else:
                            ban = 'No VAC ban on record. '

                        print(' ' + ban)

                        # Non private details printing.
                        if len(private_check) == 0:

                            url = url + 'stats/L4D2?tab=stats&subtab=versus'
                            request = requests.get(url,headers=headers)
                            soup = bs4.BeautifulSoup(request.content,'lxml')

                            try:
                                # Hours finder
                                hours = [i for i in soup.find_all('div',id='tsblVal')]
                                first_split = str(hours[0]).split('<br/>')[0]
                                hours = first_split.split('>')[1]
                                print(' Playtime: ' + str(hours) + ' ')
                            except:
                                pass

                            try:
                                # Versus win rate
                                win_rate = [i.text for i in soup.find_all('div',id='winlosstxtleft')]
                                print(' Win rate: ' + win_rate[0].split(' ')[0])
                            except:
                                pass

                            # Comments classifier.
                            for description in sentiment_list:
                                print(' ' + description)

                        print('--------------------------------------------------------------------------------------------')
                        
                    except Exception as e:
                        print(e)

                print('Sleeping for 30 seconds...')
                for second in tqdm(range(30)):
                    time.sleep(1)

            ##########################################################################################################################################
            # Free Server Checker
            elif 'mm_dedicated_force_servers' in log:

                with open(path,'w') as file:
                    file.write('')

                available_servers = {}
                for location in servers:
                    free_servers = []
                    for server in servers.get(location):
                        srv = SourceServer(server)
                        try:
                            if srv.info['players'] == 0:
                                free_servers.append('mm_dedicated_force_servers '+str(server))
                        except Exception as e:
                            print(e)
                    available_servers.update({location:free_servers})

                number_of_available_servers = {}

                for location in available_servers:
                    print('')
                    if len(available_servers.get(location)) == 0:
                        print('No available servers in ' + str(location) + '.')
                        number_of_available_servers.update({location:0})
                    else:
                        print('Available servers in ' + str(location) + ':')
                        for server in available_servers.get(location):
                            print(server)
                        number_of_available_servers.update({location:len(available_servers.get(location))})

                print('')

                for location in number_of_available_servers:
                    if int(number_of_available_servers.get(location)) > 0:
                        pyperclip.copy(available_servers.get(location)[0])
                        print('Best server copied to clipboard.')
                        break
                print('')
                print('Sleeping for 20 seconds...')
                for second in tqdm(range(20)):
                    time.sleep(1)

            ##########################################################################################################################################
            # Displays current preferred region for the mm_dedicated_force_servers command.
            elif 'Unknown command: region' in log or 'Unknown command: "region"' in log:
                print('Preferred region:',list(servers.keys())[0])
                time.sleep(5)
                with open(path,'w') as file:
                    file.write('')

            ##########################################################################################################################################
            # Settings function.
            elif 'Unknown command: settings' in log or 'Unknown command: "settings"' in log:
                print('Available server regions: ',list(servers.keys()))
                print('Choose from the available settings')
                var_1 = True
                available_choices = ['server_region_preference']
                # Enter main settings menu.
                while var_1:
                    os.system('cls')
                    print('AVAILABLE SETTINGS')
                    print('')
                    for i in available_choices:
                        print(i)
                    print('')
                    print('Type an available setting into the l4d2 console to make a change or type q to return.') 
                    var_2 = True
                    # Await input from the l4d2 console
                    while var_2:
                        file = open("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Left 4 Dead 2\\left4dead2\\console.log",'r',encoding='utf-8', errors='ignore')
                        logfile = [i for i in file.readlines()]
                        for log in logfile:
                            # If server_region_preference is entered we will change the preferred server for the mm_dedicated_force_servers command.
                            if 'Unknown command: server_region_preference' in log:
                                var_3 = True
                                # Display available regions.
                                while var_3:
                                    print('Choose your preferred server region:')
                                    for i in servers.keys():
                                        print('Type','_'.join(i.split(' ')),'in the l4d2 console.')
                                    var_4 = True
                                    # Await user choice from the l4d2 console and set the region to the choice.
                                    while var_4:
                                        file = open("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Left 4 Dead 2\\left4dead2\\console.log",'r',encoding='utf-8', errors='ignore')
                                        logfile = [i for i in file.readlines()]
                                        for log in logfile:
                                            for key in servers.keys():
                                                if 'Unknown command: {}'.format('_'.join(key.split(' '))) in log:
                                                    new_favourite = {key:servers.get(key)}
                                                    for key in servers:
                                                        if key not in list(new_favourite.keys()):
                                                            new_favourite.update({key:servers.get(key)})
                                                    servers = new_favourite
                                                    with open(path,'w') as file:
                                                        file.write('')
                                                    var_1 = False
                                                    var_2 = False
                                                    var_3 = False
                                                    var_4 = False
                                                    break

                            # If q is typed return back to the main menu.
                            if 'Unknown command: q' in log:
                                var_2 = False
                                break
                    break

                with open(path,'w') as file:
                    file.write('')

            else:
                pass
            ##########################################################################################################################################
        print('Type help in the L4D2 console.')
        print('Awaiting command.')
        time.sleep(0.5)
        os.system('cls')
        print('Type help in the L4D2 console.')
        print('Awaiting command..')
        time.sleep(0.5)
        os.system('cls')
        print('Type help in the L4D2 console.')
        print('Awaiting command...')
        time.sleep(0.5)
        os.system('cls')    