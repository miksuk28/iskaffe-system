from random import choice

def generate_salt(length=16):
    '''
    Return a random string
    '''
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    salt = []
    
    for i in range(length):
        salt.append(choice(ALPHABET))

    return "".join(salt)