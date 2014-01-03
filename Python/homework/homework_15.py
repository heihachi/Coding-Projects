'''
homework 14
Programmer James Bishop
Date October 4, 2013
Purpose: Write a compete python program that allows a user to input a single integer n.  The program then returns a list of the first n prime numbers.
'''

def isprime(number):
    times = 0 # keep count of how many times its dividable 
    for check in range (1, number+1): # go through a for loop up to number
        run = number/check # check and see if they are dividable
        remainder = int(number%check) # check for a remainder
        if run >= 1 and remainder == 0: # check if its dividable without a remainder (divided perfectly)
            times += 1 # add 1 to how many times it was divided evenly
    if times == 2: # check if times is 2 (1 and itself)
        return True # Return True if its prime
    else:
        return False # Else its false
        
#End Function Start Main Code        
numbers = int(input("Enter the number of primes you wish to find: ")) # get input of number of primes to print
primes = [] # empty list to hold prime numbers
counter = 1 # counter to allow infinite number of primes
while len(primes) != numbers: #while the lentgh of primes is not equal to the number of primes you want
    for x in range (counter, counter+11): # for loop to go through a list of 1-11, 12-22, and so on 
        check = isprime(x) # call the function isprime()
        if check == True: # if the function said that its is True its a prime number
            primes.append(x) # we than append into prime
        if len(primes) == numbers: # during this loop if the length of primes ever becomes equal to numbers it will break the loop
            break #break loop
    counter += 11 # this is to keep the for loop dynamic by multiples of 11 
print(primes) # last thing is to prime the table of primes.