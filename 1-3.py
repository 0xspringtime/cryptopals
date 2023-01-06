import string


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
        plaintext = []
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

print(decrypt_single_char_xor('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'))

#encrypted message: Cooking MC's like a pound of bacon