import base64

# The hexadecimal string to be converted
hex_string = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'

# Convert the hexadecimal string to a bytes object
bytes_object = bytes.fromhex(hex_string)

# Encode the bytes object to a base64 string
base64_string = base64.b64encode(bytes_object)

# Print the base64 string
print(base64_string)

#obtains desired SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t
