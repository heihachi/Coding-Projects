#homework 14
#Programmer James Bishop
#Date October 4, 2013
#Purpose: Uses Vigenere Cipher to encrypt/decrypt raw text.
 
#debug = []
 
def vigenere(function, text, key): # requires a string and a key
    text = text.replace(" ", "").upper() # replace the spaces with a NULL character and convert all to uppercase
    key = key.replace(" ", "").upper() #replace spaces with NULL and convert to all uppercase
    value = int(len(text)/len(key)+1) #see how many copies of the key we will need to fill up the string without error
    key = key * value #added one to value to ensure that there are enough key characters.
    #print(len(text), "/", len(key)) #debug the value variable
    if function == 'encrypt':
        encoded = [] #empty list for encoded characters
        counter = 0 #simple counter
        for letter in text: # for each letter in the string it will do this
            #print(counter) #debug the counter
            encode = encrypt(letter, key[counter]) #run the encrypt function to replace each character one at a time
            encoded.append(encode) #append it to output
            counter += 1 #add one to our counter so that the next letter is used.
        return ''.join(encoded)
    elif function == 'decrypt':
        decoded = [] #empty list for decrypted characters
        counter = 0 #simple counter for the key
        for letter in text: # for each letter in the string it will do this
            #print(counter) #debug the counter
            decode = decrypt(letter, key[counter]) #run the decrypt function to replace each character one at a time
            decoded.append(decode) #append it to output
            counter += 1 #add one to our counter so that the next letter is used.
        return ''.join(decoded)

    
#Function that will encrypt each letter
def encrypt(character, keycharacter):
#    debug.append(str(((ord(keycharacter) + ord(character)) % 26) + ord('A'))) #added the integer to a debug list to print later
    return chr(((ord(keycharacter) + ord(character)) % 26) + ord('A')) #add the key index to the character and wraps around at 26 than adds A(26)
#function that will decrypt each letter
def decrypt(character, keycharacter):
#    debug.append(str(((ord(keycharacter) + ord(character)) % 26) + ord('A'))) #added the integer to a debug list to print later
    return chr(((ord(character) - ord(keycharacter)) % 26) + ord('A')) #subtract the key index from the character and wraps around at 26 than adds A(26) 
 
# Get Input and set the key we will use for the cipher
txt = input("Enter a encrypted string: ")
key = input("Enter the key used: ")
decrypted = vigenere('decrypt', txt, key)# this will run the vigenere encrypt function 
print("DECRYPTED: ", decrypted)