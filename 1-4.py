import string


def decrypt_single_char_xor(filepath):
    # Convert the hex-encoded string to a byte array
    # Initialize an empty list to store the possible plaintext messages
    max_ascii_chars = 0
    ascii_text_chars = list(range(97, 122)) + [32]
    best_plaintext = None
    with open(filepath, "r") as f:
        for line in f:
            ciphertext = bytearray.fromhex(line.strip())
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

print(decrypt_single_char_xor("4.txt"))

#encrypted message: Now that the party is jumping