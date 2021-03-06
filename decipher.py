'''
Created on Feb 5, 2019

Ciphers used in the book 'Ghost in the Wires' by Kevin Mitnick

@author: rmoss
'''

import sys, string
from click._compat import raw_input

# Caesar Cipher: Cipher word is entered with a key amount
# Each letter in the cipher word is shifted by that key
# Example: Cipher="Test" Key=5 Output="Yjxy"
def caesarCipher(cipher, key):
    for char in cipher:
        if char.isalpha():
            if char.islower():
                char = chr( (ord(char) + key - ord('a') ) % 26 + ord('a') )
            elif char.isupper():
                char = chr((ord(char) + key - ord('A')) % 26 + ord('A'))
        print(char, end='')
    print('')
    
# Vigenere Cipher: Cipher word is entered with a keyword
# Each letter in the cipher word is shifted by a letter in the keyword
# Example: Cipher = "Hello, world!"; Keyword="test"
def vigenereCipher(cipher, keyword):
    print('Ciphertext: ', end='')
    # Counter for keyword
    keyLoc = 0
    
    for char in cipher:
        key = shift(keyword[keyLoc])
        if char.isalpha():
            if char.islower():
                char = chr( (ord(char) + key - ord('a') ) % 26 + ord('a') )
            elif char.isupper():
                char = chr((ord(char) + key - ord('A')) % 26 + ord('A'))
            
            if keyLoc < len(keyword) -1:
                keyLoc += 1
            else:
                keyLoc = 0
        print(char, end='')
    print('')
    
def shift(char):
    keyShift = 0
    if char.islower():
        keyShift = (ord(char) - ord('a')) % 26
    elif char.isupper():
        keyShift = (ord(char) - ord('A')) % 26
    return keyShift


# Base64 Cipher: 
# Example input: bmFtZXRoZWNvbXBhbnl3aGVyZWJvbm5pZXdhc2VtcGxveWVkd2hlbndlc3RhcnRlZGRhdGluZw==
# Decrypted Output: namethecompanywherebonniewasemployedwhenwestarteddating
def base64(cipher):   
    
    indexTableString = string.ascii_uppercase + string.ascii_lowercase
    indexTable = {indexTableString[i]:'{0:06b}'.format(i) for i in range(52)}
    for i in range(10):
        indexTable[str(i)] = '{0:06b}'.format(i + 52)
    indexTable['+'] = '{0:06b}'.format(62)
    indexTable['/'] = '{0:06b}'.format(63)
    indexTable['='] = ''
    
    cipherBinaryString = ''
    
    for char in cipher:
        cipherBinaryString += indexTable[char]
    
    cipherBinaryList = []
    
    for i in range(0, len(cipherBinaryString), 8):
        cipherBinaryList.append(cipherBinaryString[i:i+8])
        
    for charBinary in cipherBinaryList:
        charStr = chr(int(charBinary, base=2))
        if charStr != '':
            print(charStr, end='')
    print('')

#
def frequencyAnalysis(cipher):
    mostUsed = 'etaoinsrhld'
    
    # To keep track of lowercase substitutions later on
    cipher = cipher.upper()
    
    
    charDict = {}
    for char in cipher:
        if char not in charDict.keys():
            charDict[char] = 1
        else:
            charDict[char] += 1
    
    for key in sorted(charDict.keys()):
        print ("%s: %s" % (key, charDict[key]))
        
    listOfTuples = sorted(charDict.items(), key=lambda x: x[1], reverse=True)
    
    cipherReplaced = cipher    
    
    for i in range(len(listOfTuples)):
        elem = listOfTuples[i][0]
        cipherReplaced = cipherReplaced.replace(elem, mostUsed[i])
 
#Not Done
# Rail Fence Cipher: Cipher word is entered and number of levels
# Each letter is then printed
#
# Example below: Original = TNDGHUIEKNDMETIO
# T    .    .    .    N    .    .    .    D    .    .    .    G    .    .    .
# .    H    .    U    .    I    .    E    .    K    .    N    .    D    .    M
# .    .    E    .    .    .    T    .    .    .    I    .    .    .    O    .
# Decrypted Output = THEUNITEDKINGDOM
def railFence(cipher, levelTotal):
    locInString = 0
    levelString = []
    direction = True #Down = True; Up = False
    
    for level in range(levelTotal):
        
        dotsDown = 2 * (levelTotal - level) - 3
        dotsUp = 2 * (level) - 1
        levelString.append('.' * level)
        
        while(len(levelString[level]) < len(cipher)):
            #print(len(levelString[level]), direction, dotsDown, dotsUp)
            levelString[level] += cipher[locInString]
            locInString += 1
            if dotsDown < 0:
                direction = False
            elif dotsUp < 0:
                direction = True
            if direction and dotsDown > 0:
                levelString[level] += '.' * dotsDown
            elif not direction and dotsUp > 0:
                levelString[level] += '.' * dotsUp

        levelString[level] = levelString[level][:len(cipher)]
        
        print(levelString[level])

                 
argLength = len(sys.argv)
if(argLength > 1):
    cipherType = sys.argv[1]
    key = sys.argv[2]
    plainInput = sys.argv[3]
else:
    cipherType = raw_input("Enter type of cipher: ").lower()
    if cipherType == 'caeasar':
        key = raw_input("Enter key (Enter ? if there isn't one): ").lower()
    else:
        key = raw_input("Enter key: ").lower()
    plainInput = raw_input("Plaintext: ")
    
if cipherType == 'caesar':
    if key == '?':
        # Prints all 26 shifts if no key is entered
        print('Possible ciphertexts:')
        for i in range(26):
            caesarCipher(plainInput, i)
    else:
        print('Ciphertext: ', end='')
        caesarCipher(plainInput, int(key))
elif cipherType == 'vigenere':
    vigenereCipher(plainInput, key)
elif cipherType == 'base64':
    base64(plainInput)
elif cipherType == 'frequency':
    frequencyAnalysis(plainInput)
elif cipherType == 'rail_fence':
    railFence(plainInput,int(key))
    

# multbqncannqenabrhfgacnqogehchetbkkebmsqgkncchebr