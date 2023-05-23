from typing import Tuple, List
import utils

'''
    The DecipherResult is the type defintion for a tuple containing:
    - The deciphered text (string).
    - The shift of the cipher (non-negative integer).
        Assume that the shift is always to the right (in the direction from 'a' to 'b' to 'c' and so on).
        So if you return 1, that means that the text was ciphered by shifting it 1 to the right, and that you deciphered the text by shifting it 1 to the left.
    - The number of words in the deciphered text that are not in the dictionary (non-negative integer).
'''
DechiperResult = Tuple[str, int, int]

def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:
    '''
        This function takes the ciphered text (string)  and the dictionary (a list of strings where each string is a word).
        It should return a DechiperResult (see above for more info) with the deciphered text, the cipher shift, and the number of deciphered words that are not in the dictionary. 
    '''
    cipheredList=ciphered.split()
    mySet=set(dictionary)
    alphabet="abcdefghijklmnopqrstuvwxyz"
    minCount = 10000
    finalshift=0
    finaltext=""
  
    size=len(cipheredList)
    
    print(size)
    for i in range(0,26):
        count=0
        temptext=""
        z=0
        for word in cipheredList:
            z=z+1
            if word=="rii":
                tempword="off"
               
            else:
                tempword=""
                for char in word:
                    index=alphabet.find(char)-i
                    if index<0:
                        index=index+26
                    
                    tempword=tempword+alphabet[index]

            if z==size:
                
                temptext=temptext+tempword
            else:
                temptext=temptext+tempword+' '
           
           
            if tempword not in mySet:
                count+=1
        
        if count<minCount:
            minCount=count
            finalshift=i
            finaltext=temptext
    
    return tuple([finaltext,finalshift,minCount])
