#empty triangle
#Programmer James Bishop
#Date Sept. 12, 2013
 
rows = int(input("Enter a number higher than 5: "))
 
if rows > 5: # make sure its higher than 5
    for x in range (1,rows+1): #create a loop to make n number of rows equal to rows
        for y in range (1,x+1): #will have n number of columns
            if x == 1: # if x (the row) equals 1 or first row it will print a single *
                print("*")
            elif x == rows: #else if its rows (the last row) it will print a whole line of them to close the triangle
                print("*", end ="")
            else: # if its anything else it will check if its the first or last spot
                if y == 1: # if first column it will print a * without a newline
                    print("*", end="")
                elif y == x: #else if its the last column it will also print a * but with a newline
                    print("*")
                else: #anything else is a space to create the hollowness
                    print(" ", end="")