import math

def num_BTC(b):
    ntokens = 50
    reward = 50
    blocks = 1
    while (blocks < b):
        if (blocks % 210_000==0):
            reward = reward / 2
        ntokens = ntokens + reward
        blocks = blocks + 1

    return float(ntokens)

b = 648559; tb = 18490993.75
# b = 890884
b = 813574; tb = 19522337.5
# b = 392344; tb = 15058600.00
# b = 462283; tb = 16278537.5
r = num_BTC(b)
print("num_BTC(",b,") = ",r, ": ", r-tb)

# 25.0
# 12.5
# 6.25
# 3.15
