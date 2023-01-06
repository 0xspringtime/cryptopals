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
    ciphertext = f.read()

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


def decrypt_file(ciphertext_b64, key_size):
    # Decode the base64-encoded ciphertext
    ciphertext = base64.b64decode(ciphertext_b64)

    # Decrypt the ciphertext using the repeating-key XOR function
    key = attack(ciphertext, key_size)

    # XOR the ciphertext with the key to decrypt it
    decrypted_message = bytearray()
    for i, b in enumerate(ciphertext):
        decrypted_message.append(b ^ key[i % len(key)])

    # Return the decrypted message as a string
    return decrypted_message.decode()


def score(candidate_key_size, ciphertext):
    # as suggested in the instructions,
    # we take samples bigger than just one time the candidate key size
    slice_size = 2 * candidate_key_size

    # the number of samples we can make
    # given the ciphertext length
    nb_measurements = len(ciphertext) // slice_size - 1

    # the "score" will represent how likely it is
    # that the current candidate key size is the good one
    # (the lower the score the *more* likely)
    score = 0
    for i in range(nb_measurements):
        s = slice_size
        k = candidate_key_size
        # in python, "slices" objects are what you put in square brackets
        # to access elements in lists and other iterable objects.
        # see https://docs.python.org/3/library/functions.html#slice
        # here we build the slices separately
        # just to have a cleaner, easier to read code
        slice_1 = slice(i * s, i * s + k)
        slice_2 = slice(i * s + k, i * s + 2 * k)

        score += hamming_distance(ciphertext[slice_1], ciphertext[slice_2])

    # normalization: do not forget this
    # or there will be a strong biais towards long key sizes
    # and your code will not detect key size properly
    score /= candidate_key_size

    # some more normalization,
    # to make sure each candidate is evaluated in the same way
    score /= nb_measurements

    return score

def decrypt_single_char_xor(hex_string):
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


def findkeylength(ciphertext, min_length=2, max_length=30):
    key = lambda x: score(x, ciphertext)
    return min(range(min_length, max_length), key=key)

def attack(c):
    keysize = findkeylength(c)
    # we break encryption for each character of the key
    key = bytes()
    message_parts = list()
    for i in range(keysize):
        # the "i::keysize" slice accesses elements in an array
        # starting at index 'i' and using a step of 'keysize'
        # this gives us a block of "single-character XOR" (see figure above)
        part = decrypt_single_char_xor(ciphertext[i::keysize])
        message_parts.append(part)

    # then we rebuild the original message
    # by putting bytes back in the proper order
    message = bytes()
    for i in range(max(map(len, message_parts))):
        message += bytes([part[i] for part in message_parts if len(part) >= i + 1])
    return message

print(ciphertext)
print(attack(ciphertext).decode())