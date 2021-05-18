
def encrypt(key,plaintext):
    ciphertext=""
    letters = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
    n = len(plaintext)
    for i in range(n):
        letter = plaintext[i]
        if letter.isalpha():
            x = letters.index(plaintext[i])
            x = (x + key) % 26
            ciphertext += letters[x]
        else:
            ciphertext += letter
    return ciphertext

def decrypt(key,ciphertext):
    plaintext = encrypt(-key, ciphertext)
    return plaintext
