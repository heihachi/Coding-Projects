#homework_10
#Programmer James Bishop
#Date Sept 12, 2013
#Assignment: Write a complete python that reads 30 numbers from a file numb.dat and outputs the average of the numbers.

numberlist=[] #create the empty list we are going to put the numbers from the file into
#file="D:\\Coding\\Coding-Projects\\python\\homework\\numb.dat" # folder and file name that we are using change this
file='numb.dat' #incase file is in the current directory 
fopen = open(file, 'r') #open file
line = fopen.readlines() #enter all (30) lines into the list line
fopen.close() # close file

# For loop to make the number a integer and append it to numberlist
for number in line: 
    number = int(number)
    numberlist.append(number)

#sum the list and divide by 30 to get the average and print it
total = sum(numberlist)/30
print(total)