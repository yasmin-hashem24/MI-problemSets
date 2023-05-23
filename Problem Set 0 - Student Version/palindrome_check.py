import utils

def palindrome_check(string: str) -> bool:
    '''
    This function takes string and returns where a string is a palindrome or not
    A palindrome is a string that does not change if read from left to right or from right to left
    Assume that empty strings are palindromes
    '''
    if(len(string)==0):
        return True  #TODO: ADD YOUR CODE HERE
    rev= ''.join(reversed(string))
    if string == rev:
        return True

    return False
