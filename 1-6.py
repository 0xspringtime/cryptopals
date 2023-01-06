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

ascii_text_chars = list(range(97, 122)) + [32]
with open(filepath) as f:
    ciphertext = base64.b64decode(f.read())


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


def findkeylength(ciphertext, min_length=2, max_length=30):
    key = lambda x: score(x, ciphertext)
    return min(range(min_length, max_length), key=key)

def bxor(a, b):
    "bitwise XOR of bytestrings"
    return bytes([ x^y for (x,y) in zip(a, b)])

def attack_single_byte_xor(ciphertext):
    # a variable to keep track of the best candidate so far
    best = None
    for i in range(2**8): # for every possible key
        # converting the key from a number to a byte
        candidate_key = i.to_bytes(1, byteorder='big')
        keystream = candidate_key*len(ciphertext)
        candidate_message = bxor(ciphertext, keystream)
        nb_letters = sum([ x in ascii_text_chars for x in candidate_message])
        # if the obtained message has more letters than any other candidate before
        if best == None or nb_letters > best['nb_letters']:
            # store the current key and message as our best candidate so far
            best = {"message": candidate_message, 'nb_letters': nb_letters, 'key': candidate_key}
    return best

result = attack_single_byte_xor(ciphertext)

print('key:', result['key'])
print('message:', result['message'])
print('nb of letters:', result['nb_letters'])


def attack_repeating_key_xor(c):
    keysize = findkeylength(c)
    # we break encryption for each character of the key
    key = bytes()
    message_parts = list()
    for i in range(keysize):
        # the "i::keysize" slice accesses elements in an array
        # starting at index 'i' and using a step of 'keysize'
        # this gives us a block of "single-character XOR" (see figure above)
        part = attack_single_byte_xor(bytes(ciphertext[i::keysize]))
        key += part["key"]
        message_parts.append(part["message"])

    # then we rebuild the original message
    # by putting bytes back in the proper order
    message = bytes()
    for i in range(max(map(len, message_parts))):
        message += bytes([part[i] for part in message_parts if len(part) >= i + 1])

    return {'message': message, 'key': key}

result = attack_repeating_key_xor(ciphertext)
print("key:",result["key"],'\n')
print('message:\n')
print(result["message"].decode())