'''
This is teh Bugged addon updater
coded by Heihachi of The TrueWoW Developer Team
'''

import os
import sys
import imp
import time
import urllib2
import ConfigParser
import msvcrt as m
import subprocess 

# functions for handling config file
def configFile(filename):
    global config
    config = ConfigParser.ConfigParser()
    config.read(filename)
#get the sections and names
def ConfigSectionMap(section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
#main functions 
#wait for key press for errors
def wait():
    print "Press any key to continue..."
    m.getch()
#function to write to List.lua
def writeQuests(location, data):
    try:
        list = location+"/List.lua"
        fopen = open(list, 'w')
        fopen.write(data)
        fopen.close()
    except: #catch all errors
        e = sys.exc_info()[0]
        print ""
        print "##################################################"
        print "Error:",e
        print "Please Post Config.ini and error on the BuggedChecker Thread on the forums."
        wait()
#function to get the list from truewow and change <br> to \n (convert html newline to text newline)
def update(location):
    print "Updating Addon located at "+location
    response = urllib2.urlopen('http://www.truewow.org/quests.php')
    html = response.read()
    #print html.replace('<br>', '\n')
    writeQuests(location, html.replace('<br>', '\n'))

#function to launch wow client after a update.
'''
Only use this function when used with standalone
'''
def launchwow(location):
    if standalone == '1':
        print("Launching World of Warcraft Client")
        wowexe = "..\..\..\Wow.exe"
        try:
            os.startfile(wowexe)
        except subprocess.CalledProcessError:
            print(CalledProcessError)
        except OSError:
            print(OSError)
    else:
        print("Standalone is needed for this function to propertly work!")
#banner to display 
banner = ''':-----------------------------------
: TrueWoW (WotLK v3.3.5a)    
: BuggedChecker Addon Updater
:-----------------------------------
:
:
: - This will automatically update your BuggedChecker addon for you.
: 
: - Please Make sure your firewall is disabled or an exception is made
:   to allow this application to access the internet.
:
: - Compatible with All Version of Windows (Coded on windows 8 and 
:   tested on windows 7)
:
: - If you have any problems, try running this updater as Administrator!
:
:
: Original Updater Coded by: Titanstorm of TrueWoW
:
: Python Updater Coded by: Heihachi of The TrueWoW Developer Team
:
: Update will include setting up a service.
:'''
#setup config variables
configFile('config.ini')
standalone = ConfigSectionMap("config")['standalone']
service = ConfigSectionMap("config")['service']
launch = ConfigSectionMap("config")['launch']
#try and update if errors will print errors and pause execution
try:
    if standalone == '1':
        folder = os.getcwd()
    elif standalone == '0':
        folder = ConfigSectionMap("config")['location']
    # end that if statement
    if service == '1':
        print banner
        update(folder)
        if launch == '1':
            launchwow(folder)
    else:
        raise
except:
    print(service)
    #print banner
    #print ""
    #print "##################################################"
    #print "Service is not set to 1!"
    #print "Please set service = 1 in config.ini"
    #wait()
    
