import random
from math import pow
from params import p
from params import g

def keygen():
    q = int( (p - 1)/2 )
    print("p:", p)
    print("q:", q)
    a = random.sample(range(1, q + 1), 1)[0]
    sk = a
    h = pow(g, a, p)
    pk =  h
    return pk,sk

def encrypt(pk,m):
    h = pk
    q = int( (p - 1)/2 )
    r = random.sample(range(1, q + 1), 1)[0]
    c1 = pow(g, r, p)
    c2 = (h**r * m) % p
    return [c1,c2]

def decrypt(sk,c):
    a = sk
    m = (c[1]/(c[0]**a)) % p
    return m


pk, sk = keygen()
c = encrypt(pk, 100)
m = decrypt(sk, c)
print(m)


