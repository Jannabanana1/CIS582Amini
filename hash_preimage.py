import hashlib
import os
import string
import random

def hash_preimage(target_string):
    if not all( [x in '01' for x in target_string ] ):
        print( "Input should be a string of bits" )
        return
    n = len(target_string)
    while True:
        keys = string.ascii_letters + string.digits + string.punctuation
        x = ''.join(random.choice(keys) for i in range(50)).encode('utf-8')
        nonce = hashlib.sha256(x).hexdigest()
        nonce = bin(int(nonce, 16))
        if nonce[-n:] == target_string:
            return x


# x = hash_preimage('1111111111111')
# print(x)
# nonce = hashlib.sha256(x).hexdigest()
# nonce = bin(int(nonce, 16))
# print(nonce)
