#homework_11
#Programmer James Bishop
#Date Sept 12, 2013
#Assignment: Write a complete python program that reads 20 real numbers from a file inner.txt and outputs them in sorted order to a file outter.txt.  Note there is not any screen output for this program.

output = [] #create a empty list for the output
#two different styles to use to get the file. One is for a full path and other is for a file in the same directory as the script
#file = "D:\\Coding\\Coding-Projects\\python\\homework\\inner.txt"
file = 'inner.txt'

#open file, read the lines, and then close the file
fopen = open(file, 'r')
list = fopen.readlines()
fopen.close()

#for loop to change the strings in the file to integers since they are a number set
for line in list:
    line = int(line)
    output.append(line)
#sort the list
output.sort()

#same file style as the first file.
#file2 = "D:\\Coding\\Coding-Projects\\python\\homework\\outter.txt"
file2 = 'outter.txt'

#open with write only
fopen = open(file2, 'w')

#for loop to change the integers to strings so it writes correctly
for line in output:
    line = str(line)
    fopen.write(line) #writes to file without a newline
    fopen.write("\n") #force a new line to be added
#close the file when done with the for loop
fopen.close()