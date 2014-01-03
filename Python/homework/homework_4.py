#homework_3
#Programmer James Bishop
#Date August 28, 2013
#Assignment: Write a complete python program that inputs 3 integers and outputs YES if any of the three of the integers is positive otherwise it outputs NO.

#Get the 3 inputs
a=input("Enter the first integer: ")
b=input("Enter the second integer: ")
c=input("Enter the last integer: ")

# If statement to see if a,b, or c is above zero meaning its positive
if int(a)>0 or int(b)>0 or int(c)>0:
    print("YES") #if one of them is above zero print YES
else:
    print("NO") #else print NO