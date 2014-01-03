a = int(input("Number: "))
if a > 2:
    for x in range(1, a+1):
        if x == a:
            print("* " * (a))
        elif x == 1:
            print((" " * (a-1)) + "*")
        else:
            print((" " * (a-x)) + "*" + (" " * (2*x-3)) + "*")