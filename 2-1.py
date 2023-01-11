def add_pkcs7_padding(data, block_size):
    padding_len = block_size - (len(data) % block_size)
    padding = bytes([padding_len] * padding_len)
    return data + padding

data = b'YELLOW SUBMARINE'
block_size = 20
padded_data = add_pkcs7_padding(data, block_size)
print(padded_data)