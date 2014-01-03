#homework_9
#Programmer James Bishop
#Date Sept 12, 2013
#Assignment: Write a compete python program that allows a user to input as many positive numbers as the user wants to input.  When the user inputs a positive or negative number the program outputs the numbers in sorted order and outputs the average of the numbers.  

counter = 1 #start counter
#average2 = 0 #a usable average using basic commands instead of sum()
numbers=int(input("Enter a positive number or enter a negative number to stop: ")) #get input for first number
numberlist=[] #start a list for the ending sum()

while numbers > 0: #while the input is greater than zero
    numberlist.append(numbers) #append the list with the entered numbers including the first one
    numbers=int(input("Enter a positive number or enter a negative number to stop: ")) #run the input again in the loop
    counter += 1 #add one to the counter
#    average2 += numbers # add the input into average2 overwriting the existing number with a updated version
    #print(list(numberlist))
average = float(sum(numberlist)/counter) #using sum although we never covered it so going to have a usable one as well.
#average2 = average2/counter #at the end of the loop average average2 with counter
print("The average of all",counter,"numbers you entered is:",average) #print data
#print("The average of all",counter,"numbers you entered is:",average)