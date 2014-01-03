'''
homework 13
Programmer James Bishop
Date October 2, 2013
Purpose: Write a complete python program which allows a user to input a number between 1 and 99 inclusive.  The program then outputs the number of quaters, dimes, nickels, and pennies needed to make this amount of change.

Have two ways to do it. The modulus one was for more practice on it and too see how well it works.
'''

def countChange(amount):
    # get number of quarters with amount/25
    quarters = int(amount/25)
    # set new amount minus the number of quarters
    amount = int(amount-(quarters*25))
    # get number of dimes using amount/10
    dimes = int(amount/10)
    # set new amount minus the dimes
    amount = int(amount - (dimes*10))
    # get number of nickels using amount/5
    nickels = int(amount/5)
    #set new amount minus the nickels
    amount = int(amount-(nickels*5))
    # get number of pennies using amount/1
    pennies = int(amount/1)
    #print output
    print("Quarters: ",quarters)
    print("Dimes   : ",dimes)
    print("Nickels : ",nickels)
    print("Pennies : ",pennies)
    
def changeModulus(change):
    list = [25, 10, 5, 1] #Create a list of what coins we are looking for
    amount = [] #setup empty list to dump amount of coins
    for type in list:
        x = int(change/type) #see how many times change is broken into a coin
        change = int(change % type) # update change with the new amount
        amount.append(x) #append the amount of coins it took into amount
    #print output
    print("Quarters: ",amount[0]) #output the first subset of amount (quarters)
    print("Dimes   : ",amount[1]) #output the second subset of amount (dimes)
    print("Nickels : ",amount[2]) #output the third subset of amount (nickels)
    print("Pennies : ",amount[3]) #output the last subset of amount (pennies)
    #print(amount) #used to debug amount list
    
change = int(input("How much change do you have? >"))
print("Using division", end="\n\n")
countChange(change)
print()
print("Using Modulus", end="\n\n")
changeModulus(change)