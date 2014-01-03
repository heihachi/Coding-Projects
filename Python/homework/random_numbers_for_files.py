import random
import os


many = int(input("How many numbers: "))
file = str(input("What file name: "))
folder="D:\\Coding\\Coding-Projects\\python\\homework\\"
os.chdir(folder)
fopen = open(file, 'a')
where=os.getcwd()
print(where)
for x in range (1,many+1):
    randomnumber=random.randint(0,999)
    result=str(randomnumber)
    print(result, file=fopen)
    
    
fopen.close()