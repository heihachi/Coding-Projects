import os, subprocess


print("SSD Symlink")
print("1: Just User Data")
print("2: Just Program Files")
print("3: Just Program Files (x86)")
print("4: Just Start Menu")
print("5: Just Steam")
print("9: All")
selection = int(input("Please select one: "))

if selection > 0 and selection < 10:
    user="C:\\Users\\heihachi\\"
    program1="C:\\Program Files\\"
    program2="C:\\Program Files (x86)\\"
    start="C:\\ProgramData\\Microsoft\\Windows\\"
    ssduser="D:\\SSD_Symlinks\\Users\\Heihachi\\"
    ssdprogram1="D:\\SSD_Symlinks\\Program Files\\"
    ssdprogram2="D:\\SSD_Symlinks\\Program Files (x86)\\"
    file1=user+'mklink.bat'
    file2=program1+'mklink.bat'

    file3=program2+'mklink.bat'
    file4=start+'mklink.bat'
    if os.path.exists(file1):
        os.remove(file1)
    if os.path.exists(file2):
        os.remove(file2)
    if os.path.exists(file3):
        os.remove(file3)
    if os.path.exists(file4):
        os.remove(file4)	
        
    if selection == 1 or selection == 9:
        """
        This is the section to handle User Symlinks
        """
        os.chdir(ssduser)
        #fopen = open(file, 'a')
        list = next(os.walk('.'))[1]
        fopen = open(file1, 'a')
        print("cd",user, file=fopen)
        for folder in list:
            os.chdir(user)
            fullname = user+folder
            ssdname=ssduser+folder
            cmd_fixed = 'mklink /j "{0}" "{1}"'.format(folder, ssdname)
            print(cmd_fixed, file=fopen)
        fopen.close()
        subprocess.Popen(r'explorer /select,"{0}"'.format(file1))
        print("User Link Done!")

    if selection == 2 or selection == 9:
        """
        This is the section to handle Program Files Symlinks
        """
        os.chdir(ssdprogram1)
        #fopen = open(file, 'a')
        list2 = next(os.walk('.'))[1]
        fopen2 = open(file2, 'a')
        print("cd",program1, file=fopen2)
        for folder in list2:
            os.chdir(program1)
            fullname = program1+folder
            ssdname=ssdprogram1+folder
            cmd_fixed = 'mklink /j "{0}" "{1}"'.format(folder, ssdname)
            print(cmd_fixed, file=fopen2)
        fopen2.close()
        subprocess.Popen(r'explorer /select,"{0}"'.format(file2))
        print("Program Files Link Done!")

    if selection == 3 or selection == 9:
        """
        This is the section to handle Program Files (x86) Symlinks
        """
        os.chdir(ssdprogram2)
        list3 = next(os.walk('.'))[1]
        fopen3 = open(file3, 'a')
        print("cd",program2, file=fopen3)
        for folder in list3:
            os.chdir(program2)
            fullname = program2+folder
            ssdname=ssdprogram2+folder
            cmd_fixed = 'mklink /j "{0}" "{1}"'.format(folder, ssdname)
            print(cmd_fixed, file=fopen3)
        fopen3.close()
        subprocess.Popen(r'explorer /select,"{0}"'.format(file3))
        print("Program File (x86) Link Done!")
        
    if selection == 4 or selection == 9:
        """
        This is the secion to handle Start Menu Symlinks
        """
        fop = open(file4, 'a')
        start_menu = 'mklink /j "Start Menu" "D:\SSD_Symlinks\ProgramData\Microsoft\Windows\Start Menu\"'
        print(start_menu, file=fop)
        fop.close()
        subprocess.Popen(r'explorer /select,"{0}"'.format(file4))
        print("Start Menu Link Done!")
        
    if selection == 5 or selection == 9:
        file5 = program2+'steam.bat'
        fop = open(file5, 'a')
        print("cd",program2, file=fop)
        start_menu = 'mklink /j "Steam\SteamApps" "D:\Games\PC\Steam\SteamApps"'
        print(start_menu, file=fop)
        fop.close()
        subprocess.Popen(r'explorer /select,"{0}"'.format(file5))
        print("Steam Link Done!")
