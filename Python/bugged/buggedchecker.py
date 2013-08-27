import ConfigParser
import os
import sys
import subprocess

Config = ConfigParser.ConfigParser()
Config.read("config.ini")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
		
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

print("|-----------------------------------\n| TrueWoW (WotLK v3.3.5a)\n| BuggedChecker Addon Updater\n|-----------------------------------\n|\n|\n| - This will automatically your BuggedChecker addon for you.\n|\n| - Please make sure your firewall is disabled or an exception is made\n|   to allow this application to access the internet.\n|\n|\n| - Compatible with Windows XP/Vista/7/8 (x32 and x64 bit versions).\n|\n| - If you have any problems, try running this updater as Administrator!\n|\n|\n|\n|\n|\n|\n")
con = raw_input("|Do you want to continue (Y/N)? ")
if con == "y":

	folder = ConfigSectionMap("Folder")['location']
	if os.path.isfile(folder+"\Wow.exe"):
		workingdir=os.getcwd()
		wget=workingdir+"\wget.exe"
		ssr=workingdir+"\ssr.exe"
		quests=workingdir+"\quests.php"
		lists=workingdir+"\list.lua"
		os.chdir(workingdir)
		#subprocess.call([wget, 'http://www.truewow.org/quests.php'])
		#subprocess.Popen([ssr, '-f "quests.php" -o "list.lua" -s "<br>" -r ""'])
		subprocess.Popen([ssr,"-f", r'./quests.php' ,"-o",r'"%s"' %lists,"-s","'<br>'","-r","''"])
	else:
		print("Bad")
else:
	sys.exit(0)
