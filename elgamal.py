import random
import math
from params import p
from params import g

def keygen():
    q = int( (p - 1)/2 )
    a = random.SystemRandom().randint(1, q)
    sk = a
    # h = g**a % p
    h = pow(g, a, p)
    pk =  h
    return pk,sk

def encrypt(pk,m):
    h = pk
    q = int( (p - 1)/2 )
    r = random.SystemRandom().randint(1, q)
    # c1 = g**r % p
    c1 = pow(g, r, p)
    # c2 = (h**r * m) % p
    c2 = m * pow(h,r,p) % p
    return [c1,c2]

def decrypt(sk,c):
    a = sk
    # m = c[0]**(p-1-a)*c[1] % p
    m = c[1] * pow(c[0], p-1-a,p) % p
    return m

# pk, sk = keygen()
# m = random.SystemRandom().randint(1, p)
# print("m:", m)
# c = encrypt(pk, m)
# m = decrypt(sk, c)
# print(m, '==', decrypt(sk, c))

