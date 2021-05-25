import hashlib
import os
import random
import string

def hash_collision(k):
    if not isinstance(k,int):
        return( b'\x00',b'\x00' )
    if k < 0:
        return( b'\x00',b'\x00' )

    #Collision finding code goes here
    trial = 0
    notMatched = True

    while (notMatched):
        print(trial, "th trial")
        trial += 1
        letters = string.ascii_letters
        x = ''.join(random.choice(letters) for i in range(4))
        x = x.encode('utf-8')

        y = ''.join(random.choice(letters) for i in range(4))
        y = y.encode('utf-8')

        x_hashed = hashlib.sha256(x).hexdigest()
        x_hashed = bin(int(x_hashed, 16))

        y_hashed = hashlib.sha256(y).hexdigest()
        y_hashed = bin(int(y_hashed, 16))

        for i in range(k):
            if x_hashed[-1-i]!=y_hashed[-1-i]:
                break
            if i>=(k-1):
                notMatched = False

    return( x, y )


# k = 5
# x, y = hash_collision(k)
# x_hashed = hashlib.sha256(x).hexdigest()
# x_hashed = bin(int(x_hashed, 16))
# y_hashed = hashlib.sha256(y).hexdigest()
# y_hashed = bin(int(y_hashed, 16))
# print(x_hashed[-k-3:])
# print(y_hashed[-k-3:])
