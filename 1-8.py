# Load the hex-encoded ciphertexts from the file
with open("8.txt", "r") as f:
    ciphertexts = f.readlines()

# Iterate over the ciphertexts
for ciphertext in ciphertexts:
    # Convert the ciphertext from hex to bytes
    ciphertext = bytearray.fromhex(ciphertext.strip())

    # Split the ciphertext into blocks of 16 bytes
    blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    
    blocks = [tuple(block) for block in blocks]


    # Check if there are any repeating blocks
    if len(blocks) != len(set(blocks)):
        print("ECB mode detected in ciphertext:", ciphertext.hex())