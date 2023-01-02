def xor_hex_strings(s1, s2):
    # Convert the hex-encoded strings to bytes
    b1 = bytes.fromhex(s1)
    b2 = bytes.fromhex(s2)

    # Check that the buffers are of equal length
    if len(b1) != len(b2):
        raise ValueError("Buffers must be of equal length")

    # Initialize an empty list to store the XOR combination
    xor_combination = []

    # Iterate through the buffers and compute the XOR combination
    for i in range(len(b1)):
        xor_combination.append(b1[i] ^ b2[i])

    # Convert the XOR combination back to a hex-encoded string
    return bytes(xor_combination).hex()

print(xor_hex_strings('1c0111001f010100061a024b53535009181c', '686974207468652062756c6c277320657965'))

#produces desired 746865206b696420646f6e277420706c6179