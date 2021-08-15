#+= imports =+#
try:
	import time, json, requests, webbrowser, os, sys, ctypes
	from pypresence import Presence
	from colorama import Fore, init
	init(autoreset=True) # auto reset color every print
except Exception as error:
	print(f'Couldn\'t import everything (did you install requirements?) | {error}')

#+= important functions =+#
class log:
	def error(text: str):
		changeWindowTitle('Error')
		clear()
		print(f'{Fore.LIGHTRED_EX}[Error]{Fore.RESET} {text}\nPlease report this error on the Switchence GitHub issue page if this error happens consistently')
		time.sleep(5)
		webbrowser.open('https://github.com/Aethese/Switchence/issues/', new=2, autoraise=True)
		time.sleep(600)
		sys.exit()

	def info(text: str):
		changeWindowTitle('Info')
		clear()
		print(f'{Fore.LIGHTGREEN_EX}[Info]{Fore.RESET} {text}')
		time.sleep(600)
		sys.exit()

	def warning(text: str):
		print(f'\n{Fore.LIGHTYELLOW_EX}[WARNING]{Fore.RESET} {text}\n')

	def loading(text: str):
		print(f'{Fore.LIGHTCYAN_EX}[Loading]{Fore.RESET} {text}')
log.loading('Loading initial functions...')

def clear():
	os.system('cls' if os.name =='nt' else 'clear') # *supposedly* multi platform supported clear
clear()

def changeWindowTitle(title):
	if os.name == 'nt':
		ctypes.windll.kernel32.SetConsoleTitleW(f'Switchence | {title}')
changeWindowTitle('Loading')

def updateProgram(setting, onlineVer): # 5132-1460-8735
	if setting:
		changeWindowTitle('Updating')
		try:
			currentOnlineVersion = requests.get('https://raw.githubusercontent.com/Aethese/Switchence/main/main.py')
			if currentOnlineVersion.status_code != 200:
				print(f'{Fore.LIGHTRED_EX}[ERROR]{Fore.RESET} Status code is not 200, it is {currentOnlineVersion.status_code}, so the program will not update')
			else:
				onlineVersionBinary = currentOnlineVersion.content # if status code = success update to latest version
				with open('main.py', 'wb') as file: # thanks to https://stackoverflow.com/users/13155625/dawid-januszkiewicz for getting this to work!
					file.write(onlineVersionBinary)
				with open('config.json', 'r') as jsonfile:
					jsonFile = json.load(jsonfile)
					for details in jsonFile['config']:
						details['version'] = onlineVer
				with open('config.json', 'w') as jsonfile:
					json.dump(jsonFile, jsonfile, indent=4)
				log.info('Updated to the latest version!')
		except Exception as error:
			log.error(f'Couldn\'t change version setting when updating | {error}')
		log.info('Successfully updated to the latest version of Switchence!')
	elif setting == False:
		log.warning('Attempted to update program without the Auto Updater on')

#+= variables =+#
id = '803309090696724554' # just pre defining variables
version = None
oVersion = None # online version
sw = None
updatenotifier = None
configfname = None
showbutton = None
legacy = None
autoupdate = None
gamenames = []
gamefnames = []
chosenOne = ''
img = ''
fname = ''
updateAvailable = False
announcement = None

#+= loading config file =+#
def createFiles():
	try: # fucking global vars
		global sw, version, updatenotifier, configfname, showbutton, legacy, autoupdate
		configjson = {}
		configjson['config'] = [{
			'sw-code': sw,
			'version': '1.5.0',
			'update-notifier': True,
			'fname': False,
			'show-button': True,
			'legacy': True,
			'auto-update': False
		}]
		with open('config.json', 'w') as jsonfile:
			json.dump(configjson, jsonfile, indent=4)
		with open('config.json', 'r') as jsonfile: # actually get the info lol
			log.loading('Setting config settings...')
			jsonFile = json.load(jsonfile)
			for details in jsonFile['config']:
				sw = details['sw-code']
				version = details['version']
				updatenotifier = details['update-notifier']
				configfname = details['fname']
				showbutton = details['show-button']
				legacy = details['legacy']
				autoupdate = details['auto-update']
			log.loading('Config file settings set!')
	except Exception as error:
		log.error(f'Couldn\'t create config settings | {error}')

log.loading('Checking for config file...')
if os.path.isfile('config.json'):
	log.loading('Found config file, attempting to read contents...')
	try:
		with open('config.json', 'r') as jsonfile:
			log.loading('Reading config file\'s content...')
			jsonFile = json.load(jsonfile)
			for details in jsonFile['config']:
				sw = details['sw-code']
				version = details['version']
				updatenotifier = details['update-notifier']
				configfname = details['fname']
				showbutton = details['show-button']
				legacy = details['legacy']
				autoupdate = details['auto-update']
			log.loading('Loaded config settings!')
	except:
		try:
			if sw == None: # in case an empty config folder is found
				sw = ''
			if version == None:
				version = '1.5.0' # this will not be changed
			log.loading('Missing config settings found, creating them...')
			createFiles()
		except Exception as error:
			log.error(f'Couldn\'t load config file (1) | {error}')
elif os.path.isfile('config.json') == False:
	log.loading('Config file not found, attempting to create one...')
	try:
		sw = ''
		createFiles()
	except Exception as error:
		log.error(f'Couldn\'t load config file (2) | {error}')
else:
	log.error('Couldn\'t load config settings')

#+= game list =+#
log.loading('Attempting to load game list...')
try:
	gamejson = requests.get('https://raw.githubusercontent.com/Aethese/Switchence/main/games.json') # auto update game list :)
	if gamejson.status_code != 200:
		log.error(f'Could not get game list with status code {gamejson.status_code}')
	gamejsontext = gamejson.text
	games = json.loads(gamejsontext)
	oVersion = games['version']
	announcement = games['announcement']
	log.loading('Game list loaded!')
except Exception as error:
	log.error(f'Couldn\'t load game list | {error}')

log.loading('Attempting to read game list info...')
try:
	for details in games['games']:
		gamenames.append(details['name'])
		gamefnames.append(details['fname'])
	log.loading('Successfully read game list info!')
except Exception as error:
	log.error(f'Couldn\'t load game names from list | {error}')

#+= checking version =+#
log.loading('Checking file version...')
if version == '' or version == None: # checks your version
	log.loading('File version not found, attempting to create...')
	try:
		with open('config.json', 'r') as jsonfile:
			jsonFile = json.load(jsonfile)
			for details in jsonFile['config']:
				details['version'] = oVersion
		with open('config.json', 'w') as jsonfile:
			json.dump(jsonFile, jsonfile, indent=4)
		log.loading('Successfully created file version!')
	except Exception as error:
		log.error(f'Couldn\'t write to the version file | {error}')
elif version != oVersion:
	updateAvailable = True

#+= rpc =+#
log.loading('Attempting to start Rich Presence...')
try:
	RPC = Presence(id)
	RPC.connect()
	log.loading('Successfully started Rich Presence!')
except Exception as error:
	log.error(f'RPC couldn\'t connect | {error}')

#+= some more important functions =+#
def changePresence(swStatus, pName, pImg, pFname):
	start_time = time.time()
	local = time.localtime()
	string = time.strftime('%H:%M', local)
	if swStatus == False:
		try:
			if showbutton:
				RPC.update(large_image=pImg, large_text=pFname, small_image='switch_png', small_text=f'Switchence v{version}', details=pFname, 
						   buttons=[{'label': 'Get this program here', 'url': 'https://github.com/Aethese/Switchence/releases'}], start=start_time)
				print(f'Set game to {pFname} at {string}')
				changeWindowTitle(f'Playing {pFname}')
			elif showbutton == False:
				RPC.update(large_image=pImg, large_text=pFname, small_image='switch_png', small_text=f'Switchence v{version}', details=pFname, start=start_time)
				print(f'Set game to {pFname} at {string}')
				changeWindowTitle(f'Playing {pFname}')
			else:
				log.error('Couldn\'t get button info (1)')
		except Exception as error:
			log.error(f'Couldn\'t set RPC(1) to {pName} | {error}')
	elif swStatus:
		try:
			if showbutton == True:
				RPC.update(large_image=pImg, large_text=pFname, small_image='switch_png', small_text=f'Switchence v{version}', details=pFname, 
						   state=f'SW-{sw}', buttons=[{'label': 'Get this program here', 'url': 'https://github.com/Aethese/Switchence/releases'}], start=start_time)
				print(f'Set game to {pFname} at {string} with friend code \'SW-{sw}\' showing')
				changeWindowTitle(f'Playing {pFname}')
			elif showbutton == False:
				RPC.update(large_image=pImg, large_text=pFname, small_image='switch_png', small_text=f'Switchence v{version}', details=pFname, state=f'SW-{sw}', start=start_time)
				print(f'Set game to {pFname} at {string} with friend code \'SW-{sw}\' showing')
				changeWindowTitle(f'Playing {pFname}')
			else:
				log.error('Couldn\'t get button info (2)')
		except Exception as error:
			log.error(f'Couldn\'t set RPC(2) to {pName} | {error}')
	else:
		log.error('Couldn\'t get friend code status')

def changeUpdateNotifier():
	picked = input('What setting do you want the Update Notifier to be on (on or off)? ')
	picked = picked.lower()
	if picked == 'on' or picked == 'true' or picked == 't': # why do you want this on tbh
		try:
			with open('config.json', 'r') as jsonfile: # very weird/hacky way to do this lol, but it does work tho
				jsonFile = json.load(jsonfile)
				for details in jsonFile['config']:
					details['update-notifier'] = True
			with open('config.json', 'w') as jsonfile:
				json.dump(jsonFile, jsonfile, indent=4)
		except Exception as error:
			log.error(f'Couldn\'t change update-notifier setting | {error}')
		log.info('Update notifier set to {Fore.GREEN}TRUE{Fore.RESET}. Rerun the program to use it with the new settings')
	elif picked == 'off' or picked == 'false' or picked == 'f':
		try:
			with open('config.json', 'r') as jsonfile: # very weird/hacky way to do this lol
				jsonFile = json.load(jsonfile)
				for details in jsonFile['config']:
					details['update-notifier'] = False
			with open('config.json', 'w') as jsonfile:
				json.dump(jsonFile, jsonfile, indent=4)
		except Exception as error:
			log.error(f'Couldn\'t change update-notifier setting | {error}')
		log.info('Update notifier set to {Fore.YELLOW}FALSE{Fore.RESET}. Rerun the program to use it with the new settings')

def changeFNameSetting():
	if configfname == False:
		l = 'short'
	elif configfname == True:
		l = 'full'
	else:
		log.error('Couldn\'t get config name setting')
	k = input(f'Your current setting is set to: {Fore.LIGHTGREEN_EX}{l}{Fore.RESET}. What do you want to change it to (\'full\' for full game names, \'short\' for shortened game names)? ')
	k = k.lower()
	if k == 'full' or k == 'f':
		try:
			with open('config.json', 'r') as jsonfile: # man i can use this anywhere lol
				jsonFile = json.load(jsonfile)
				for details in jsonFile['config']:
					details['fname'] = True
			with open('config.json', 'w') as jsonfile:
				json.dump(jsonFile, jsonfile, indent=4)
			log.info(f'Set game name to {Fore.LIGHTYELLOW_EX}Full{Fore.RESET}')
		except Exception as error:
			log.error(f'Couldn\'t change fname setting | {error}')
	elif k == 'short' or k == 's':
		try:
			with open('config.json', 'r') as jsonfile:
				jsonFile = json.load(jsonfile)
				for details in jsonFile['config']:
					details['fname'] = False
			with open('config.json', 'w') as jsonfile:
				json.dump(jsonFile, jsonfile, indent=4)
			log.info(f'Set game name to {Fore.LIGHTYELLOW_EX}Short{Fore.RESET}')
		except Exception as error:
			log.error(f'Couldn\'t change fname setting | {error}')

def changeAutoUpdate():
	print(f'Your current Auto Update setting is set to {Fore.LIGHTGREEN_EX}{autoupdate}{Fore.RESET}')
	ask = input('What would you like to change it to? On or off? ')
	ask = ask.lower()
	if ask == 'on':
		try:
			with open('config.json', 'r') as jsonfile:
				jsonFile = json.load(jsonfile)
				for details in jsonFile['config']:
					details['auto-update'] = True
			with open('config.json', 'w') as jsonfile:
				json.dump(jsonFile, jsonfile, indent=4)
			log.info(f'Set Auto Update setting to {Fore.LIGHTGREEN_EX}True{Fore.RESET}')
		except Exception as error:
			log.error(f'Couldn\'t change fname setting | {error}')
	elif ask == 'off':
		try:
			with open('config.json', 'r') as jsonfile:
				jsonFile = json.load(jsonfile)
				for details in jsonFile['config']:
					details['auto-update'] = False
			with open('config.json', 'w') as jsonfile:
				json.dump(jsonFile, jsonfile, indent=4)
			log.info(f'Set Auto Update setting to {Fore.LIGHTRED_EX}False{Fore.RESET}')
		except Exception as error:
			log.error(f'Couldn\'t change fname setting | {error}')
	else:
		log.info(f'Your sellection, {ask}, is not a good answer, please answer with \'on\' or \'off\' next time')

#+= looking for game status before picking a game =+#
log.loading('Attempting to set looking for game status...')
try:
	start_time = time.time()
	if showbutton:
		RPC.update(large_image='switch_png', large_text='Searching for a game', details='Searching for a game', 
				   buttons=[{'label': 'Get this program here', 'url': 'https://github.com/Aethese/Switchence/releases'}], start=start_time)
		log.loading('Successfully set looking for game status!')
	elif showbutton == False:
		RPC.update(large_image='switch_png', large_text='Searching for a game', details='Searching for a game', start=start_time)
		log.loading('Successfully set looking for game status!')
except Exception as error:
	log.error(f'Couldn\'t set looking for game status')
time.sleep(0.75)
changeWindowTitle('Picking a game')
clear()
print('''
 .d8888b.                d8b 888             888                                          
d88P  Y88b               Y8P 888             888                                          
Y88b.                        888             888                                          
 "Y888b.   888  888  888 888 888888  .d8888b 88888b.   .d88b.  88888b.   .d8888b  .d88b.  
    "Y88b. 888  888  888 888 888    d88P"    888 "88b d8P  Y8b 888 "88b d88P"    d8P  Y8b 
      "888 888  888  888 888 888    888      888  888 88888888 888  888 888      88888888 
Y88b  d88P Y88b 888 d88P 888 Y88b.  Y88b.    888  888 Y8b.     888  888 Y88b.    Y8b.     
 "Y8888P"   "Y8888888P"  888  "Y888  "Y8888P 888  888  "Y8888  888  888  "Y8888P  "Y8888    
Made by: Aethese#1337
''')

#+= handle new update =+#
if updateAvailable:
	if autoupdate:
		print(f'{Fore.LIGHTGREEN_EX}[INFO]{Fore.RESET} New update found, updating to latest version...')
		time.sleep(1)
		updateProgram(autoupdate, oVersion)
	if updatenotifier: # this will show if auto updates aren't on
		print(f'{Fore.LIGHTGREEN_EX}[INFO]{Fore.RESET} Your current version of Switchence {Fore.LIGHTRED_EX}v{version}{Fore.RESET} is not up to date')
		print(f'{Fore.LIGHTGREEN_EX}[INFO]{Fore.RESET} You can update Switchence to the current version {Fore.LIGHTRED_EX}v{oVersion}{Fore.RESET} by turning on Auto Updates or by visiting the official GitHub page')
		print(f'{Fore.LIGHTGREEN_EX}[INFO]{Fore.RESET} If you wish to turn on auto updates type \'auto update\' in the game selection input')
		print(f'{Fore.LIGHTGREEN_EX}[INFO]{Fore.RESET} If you wish to turn off update notifications, type \'update notifier\' in the game selection input')
		print(f'{Fore.LIGHTYELLOW_EX}The program will return to normal shortly')
		time.sleep(2)
		webbrowser.open('https://github.com/Aethese/Switchence/releases', new=2, autoraise=True)
		time.sleep(7)

#+= handle announcement =+#
if announcement != None or announcement != '':
	print(f'\n{Fore.LIGHTCYAN_EX}[ANNOUNCEMENT]{Fore.RESET} {announcement}\n')

#+= pick game =+#
print('Here are the current games: ')
if configfname == False:
	print(', '.join(gamenames))
elif configfname:
	print(', '.join(gamefnames))
else:
	log.error('Couldn\'t print game names')
x = input('\nWhat game do you wanna play? ')
x = x.lower()

#+= input options =+#
if x == 'github' or x == 'gh':
	print('i mean i guess')
	time.sleep(0.5)
	webbrowser.open('https://github.com/Aethese/Switchence/', new=2, autoraise=True)
	time.sleep(2.5)
	sys.exit()
elif x == 'update notifier' or x == 'update-notifier' or x == 'un' or x == 'u-n':
	changeUpdateNotifier()
elif x == 'change-name' or x =='change name' or x == 'c-n' or x == 'cn':
	changeFNameSetting()
elif x == 'auto-update' or x == 'auto update' or x == 'a-u' or x == 'a u':
	changeAutoUpdate()
elif x == 'options' or x == 'o':
	log.info('''The current options are:
\'github\' this will bring up the public GitHub repo
\'update notifier\' which toggles the built-in update notifier
\'change name\' this will toggle how game names are shown on the game select screen
\'auto update\' which toggles the built-in auto updater
\'options\' this will bring up this page
''')

#+= sw handling =+#
y = input(f'Do you want to show your friend code \'SW-{sw}\' (you can change this by typing \'change\')? ')
y = y.lower()
if y == 'yes' or y == 'y':
	if sw == '' or sw == None:
		log.info('Friend code not set. Rerun the program and change your friend code to your friend code')
elif y == 'change' or y == 'c':
	c = input('What is your new friend code (just type the numbers)? ')
	b = input(f'Is \'SW-{c}\' correct? ')
	b = b.lower()
	if b == 'yes' or b == 'y':
		try:
			with open('config.json', 'r') as jsonfile: # i use this because it works, don't judge me
				jsonFile = json.load(jsonfile)
				for details in jsonFile['config']:
					details['sw-code'] = c
			with open('config.json', 'w') as jsonfile:
				json.dump(jsonFile, jsonfile, indent=4)
			sw = c
			print(f'Friend code changed to SW-{c}')
			y = 'yes'
		except Exception as error:
			log.error(f'Couldn\'t change sw-code | {error}')
	else:
		print('Friend code not changed')

#+= search for game =+#
try:
	for n in games['games']:
		z = n['name']
		o = n['fname']
		if z.lower() == x:
			chosenOne = z
			break
		elif o.lower() == x:
			chosenOne = o
			break
	else:
		log.info('The game you specified is not in the current game list')
except Exception as error:
	log.error(f'Can\'t find the game ({x}) the user specified (1) | {error}')

#+= send info to changePresence function about game picked =+#
try:
	for i in games['games']:
		if i['name'] == chosenOne or i['fname'] == chosenOne:
			name = i['name']
			img = i['img']
			fname = i['fname']
			if y == 'yes' or y == 'y':
				changePresence(True, name, img, fname)
				break
			else:
				changePresence(False, name, img, fname)
				break
except Exception as error:
	log.error(f'Can\'t find the game ({chosenOne}) specified (2) | {error}')

#+= just needed, trust me =+#
while True:
	time.sleep(15)
