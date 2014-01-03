#homework_8
#Programmer James Bishop
#Date Sept 12, 2013
#Assignment: Write a complete python program which allows a user to input an integer and outputs a backslash which is n rows high.

rows=int(input("Enter the number of rows: ")) #get input as a integer
count=0 #start a counter

for x in range (1,rows+1): #for the number of rows
    count = rows+1-x #set count to rows +1 - the row we are on
    while count > 0: #while loop to print " " until at the end
        if count == 1: # if the counter is at 1 (being the last one) print "*"
            print("*")
        else: #else print a " "
            print(" ", end="")
        count -= 1 # subtract 1 from counter
    #end while
#end for