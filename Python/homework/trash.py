from itertools import starmap, cycle                                                           
debug = [] 
def encrypt(message, key):                                                                     
 
    # convert to uppercase.                                                                    
    # strip out non-alpha characters.                                                          
    message = filter(lambda _: _.isalpha(), message.upper())                                   
 
    # single letter encrpytion.                                                                
    def enc(c,k):
        debug.append(str(((ord(k) + ord(c)) % 26) + ord('A')))
        return chr(((ord(k) + ord(c)) % 26) + ord('A'))                              
    return "".join(starmap(enc, zip(message, cycle(key))))                                     
 
def decrypt(message, key):                                                                     
 
    # single letter decryption.                                                                
    def dec(c,k):
        return chr(((ord(c) - ord(k)) % 26) + ord('A'))                              
        
    return "".join(starmap(dec, zip(message, cycle(key))))                                     
 
 
text = "thisisacipher"              
key = "VIGENERECIPHER"                                                                         
 
encr = encrypt(text, key)                                                                      
decr = decrypt(encr, key)                                                                      
 
print(text)  
print(key)                                                                                 
print(encr)                                                                                    
print(decr)
print(', '.join(debug))