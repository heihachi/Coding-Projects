#cipher
#Programmer James Bishop
#Date October 1, 2013
#Purpose: Uses Vigenere Cipher to encrypt raw text.

#debug = []

def vigenere(text, key): # requires a string and a key
    text = text.replace(" ", "").upper() # replace the spaces with a NULL character and convert all to uppercase
    value = int(len(text)/len(key)+1) #see how many copies of the key we will need to fill up the string without error
    key = key * value #added one to value to ensure that there are enough key characters.
    #print(len(text), "/", len(key)) #debug the value variable
    output = [] # setup a output list to hold the encrypted letters/string
    counter = 0 #simple counter for the key
    for letter in text: # for each letter in the string it will do this
        #print(counter) #debug the counter
        encode = encrypt(letter, key[counter]) #run the encrypt function to replace each character one at a time
        output.append(encode) #append it to output
        counter += 1 #add one to our counter so that the next letter is used.
    #print(', '.join(debug)) #print the debug info of integers to compare with online vigenere tool
    return ''.join(output) # return the list joined by a ''
#Function that will encrypt each letter
def encrypt(character, keycharacter):
#    debug.append(str(((ord(keycharacter) + ord(character)) % 26) + ord('A'))) #added the integer to a debug list to print later
    return chr(((ord(keycharacter) + ord(character)) % 26) + ord('A')) #add the key index to the character and wraps around at 26 than adds A(26)

# Get Input and set the key we will use for the cipher
txt = input("Enter a string: ")
key = input("Enter a Key: ")
print(vigenere(txt, key))# this will run the vigenere function 