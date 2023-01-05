import base64
filepath = "6.txt"
def hamming_distance(s1, s2):
    # Convert the strings to bytes
    b1 = base64.b64encode(s1)
    b2 = base64.b64encode(s2)

    # Compute the Hamming distance
    distance = 0
    for b1, b2 in zip(b1, b2):
        distance += bin(b1 ^ b2).count("1")

    return distance


with open(filepath) as f:
    ciphertext = base64.b64decode(f.read())

def decrypt_repeating_key_xor(ciphertext, key_size):
    # Break the ciphertext into blocks of key_size length
    blocks = [ciphertext[i:i + key_size] for i in range(0, len(ciphertext), key_size)]

    # Transpose the blocks
    transposed_blocks = [bytearray() for _ in range(key_size)]
    for block in blocks:
        for i, b in enumerate(block):
            transposed_blocks[i].append(b)

    # Decrypt each transposed block using single-character XOR
    key = bytearray()
    for block in transposed_blocks:
        key.append(decrypt_single_char_xor(block))

    return key


def decrypt_single_char_xor(hex_string):
    # Convert the hex-encoded string to a byte array
    ciphertext = bytearray.fromhex(hex_string)
    # Initialize an empty list to store the possible plaintext messages
    max_ascii_chars = 0
    ascii_text_chars = list(range(97, 122)) + [32]
    best_plaintext = None

    # Iterate through all possible single characters (0-255)
    for i in range(256):
        # Initialize an empty list to store the current plaintext message
        plaintext = bytearray()
        # XOR the ciphertext with the current single character
        for j in range(len(ciphertext)):
            plaintext.append(ciphertext[j] ^ i)


           # Convert the plaintext message to a bytes object
            plaintext_bytes = bytes(plaintext)
            num_ascii_chars = sum(1 for c in plaintext_bytes if c in ascii_text_chars)
            if num_ascii_chars > max_ascii_chars:
                max_ascii_chars = num_ascii_chars
                best_plaintext = plaintext_bytes

    return best_plaintext

def decrypt_file(ciphertext_b64, key_size):
    # Decode the base64-encoded ciphertext
    ciphertext = base64.b64decode(ciphertext_b64)

    # Decrypt the ciphertext using the repeating-key XOR function
    key = decrypt_repeating_key_xor(ciphertext, key_size)

    # XOR the ciphertext with the key to decrypt it
    decrypted_message = bytearray()
    for i, b in enumerate(ciphertext):
        decrypted_message.append(b ^ key[i % len(key)])

    # Return the decrypted message as a string
    return decrypted_message.decode()


def findkeylength(ciphertext, min_length=2, max_length=40):
    key = lambda x: decrypt_repeating_key_xor(x, ciphertext)
    return min(range(min_length, max_length), key=key)

#print(ciphertext)
print(attack(ciphertext))