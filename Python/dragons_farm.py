'''
food
Base Rate: 6100
Research Bonus:2440
Wilds Bonus: 1525
Items Bonus: 0
Troops use: 43574
total prod/hr: -33509
'''

'''
TO-DO list
Fix last counter to correctly predict the number of buildings for that rank
'''
farmProd = [100, 300, 600, 1000, 1500, 2100, 2800, 3600, 4500, 5500]
maxfarm = 10
def foodCalc(array, research, wilds, items, troops):
    calc = array
    calc += (research+wilds+items)
    calc -= troops
    #print("Total: "+str(calc))
    return calc
def stableCalc(total, array):
    array.sort()
    levels = [[0] for x in range(1,maxfarm+1)]
    required = [[0] for y in range(1,maxfarm+1)]
    for level in array:
        if(int(level) <= maxfarm):
            levels[int(level)-1][0] += 1
    newtotal = abs(int(total))
    #print("Total:",newtotal)
    #return total
    counter = 1
    last = 0
    #print(levels)
    while newtotal > 0:
        for ranks in levels:
            #print("-Rank",ranks)
            for number in ranks:
                #print("Ranks",counter,":",number)
                #if total <= 0:
                #    print("Test:",total)
                #    break
                #print("Start Number:",number,"Total:",newtotal)
                if newtotal > 0:
                    if counter > 1:
                        #print("Counter:",counter)
                        if last != 0:
                            #print("Number:",number,"last:",last)
                            number += last
                            #print("Number(edited):",number)
                            if number > 0:
                                temp = 0
                                while temp <= number:
                                    if newtotal > 0:
                                        newtotal -= (farmProd[counter])
                                        temp += 1
                                    else:
                                        break
                                required[counter][0] += int(temp)
                                last = int(number)
                            #endif
                        #endif
                        elif last == 0:
                            if number > 0:
                                temp = 0
                                while temp <= number:
                                    if newtotal > 0:
                                        newtotal -= (farmProd[counter])
                                        temp += 1
                                    else:
                                        break
                                required[counter][0] += int(temp)
                                last = int(temp)
                                if newtotal <= 0:
                                #    print("Test:",newtotal)
                                    break
                            #endif
                        #endif
                    #endif
                    elif counter == 1:
                        #print("Counter:",counter)
                        if number > 0:
                            temp = 0
                            while temp <= number:
                                if newtotal > 0:
                                    newtotal -= (farmProd[counter])
                                    temp += 1
                                else:
                                    break
                            required[counter][0] += int(temp)
                            last = int(temp)
                            if newtotal <= 0:
                            #    print("Test:",newtotal)
                                break
                counter += 1
        return (required)
def calcCheck(total, needed):
    check = 0
    count = 1
    for needs in needed:
        #print("Needs:",needs)
        for x in needs:
            #print("x:",x)
            if x != 0:
                check += (farmProd[count]*x)
                #print(total,"+",(farmProd[count]*x))
        count += 1
    #print(check)
    return (total+check)
baserate = int(input("Enter base rate for food: "))
research = int(input("Enter research bonus for food: "))
wilds = int(input("Enter wilds bonus for food: "))
items = int(input("Enter items bonus for food: "))
troops = int(input("Enter troops used for food: "))
#research = 3360
#wilds = 2100
#items = 0
#troops = 14357
print("We are going to need data on how many farms you have and their levels")
numfarm = int(input("Enter number of farms you own: "))
farmlevels = []
for x in range(1,numfarm+1):
    question = "Enter level for farm "+str(x)+": "
    levelinput = int(input(question))
    if(levelinput <= maxfarm):
        farmlevels.append(str(levelinput))
    else:
        print("ERROR: level for your farm is too high. Please re-enter value.")
        levelinput = int(input(question))
        if(levelinput <= maxfarm):
            farmlevels.append(str(levelinput))
        else:
            print('ERROR: Not saving value for farm\'s level.')
#print(farmlevels)
base = 0
for level in farmlevels:
    base += farmProd[int(level)-1]
total = foodCalc(baserate, research, wilds, items, troops)
#print("Total: "+str(total))
#print(stableCalc(str(foodCalc(farmlevels, research, wilds, items, troops)), farmlevels))
stable = stableCalc(total, farmlevels)
test = calcCheck(total, stable)
#print(stable)
print("Base Rate:",total)
print("Attempt:",test,"per hour")
lastcount = 1
for x in stable:
    for y in x:
        if y != 0:
            print("Build",y,"level",lastcount,"farms")
    lastcount +=1