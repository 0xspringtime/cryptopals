def repeating_key_xor(message, key):
    # Convert the message and key to bytes
    message_bytes = message.encode()
    key_bytes = key.encode()

    # Initialize an empty list to store the encrypted message
    encrypted_message = []

    # Encrypt the message using the key
    for i in range(len(message_bytes)):
        encrypted_message.append(message_bytes[i] ^ key_bytes[i % len(key_bytes)])

    # Convert the encrypted message to a hex-encoded string
    return bytes(encrypted_message).hex()

message = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
key = "ICE"
encrypted_message = repeating_key_xor(message, key)

print(encrypted_message)

#output: 0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f