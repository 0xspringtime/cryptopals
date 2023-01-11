#11
import os
from Crypto.Cipher import AES
from random import randint

def generate_random_aes_key():
    return os.urandom(16)

def encryption_oracle(data):
    key = generate_random_aes_key()
    prepend_bytes = os.urandom(randint(5,10))
    append_bytes = os.urandom(randint(5,10))
    data = prepend_bytes + data + append_bytes
    cipher = AES.new(key, AES.MODE_ECB) if randint(0, 1) == 0 else AES.new(key, AES.MODE_CBC, os.urandom(16))
    return cipher.encrypt(data)

def detect_cipher_mode(ciphertext):
    block_size = 16
    chunks = [ciphertext[i:i+block_size] for i in range(0, len(ciphertext), block_size)]
    if len(set(chunks)) != len(chunks):
        return "ECB"
    else:
        return "CBC"