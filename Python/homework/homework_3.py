#homework_3
#Programmer James Bishop
#Date August 28, 2013
#Assignment: Write a complete python program that inputs 3 integers and outputs YES if all three of the integers are positive otherwise it outputs NO.

#Get the 3 inputs
one   = input("What is the first integer? > ")
two   = input("What is the second integer? > ")
three = input("What is the last integer? > ")

#Check if variables one, two, or three are less then zero
if int(one)<0 or int(two)<0 or int(three)<0:
    print("NO") #if one of them are less then zero print NO
else: #else if they are all above zero print YES
    print("YES")