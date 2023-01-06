from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Load the encrypted data from the file
with open("7.txt", "rb") as f:
    encrypted_data = f.read()

# Decode the encrypted data from Base64
encrypted_data = base64.b64decode(encrypted_data)

# Create a Cipher object using the AES algorithm and the ECB mode
cipher = Cipher(algorithms.AES(b"YELLOW SUBMARINE"), modes.ECB(), backend=default_backend())

# Create a decryption context
decryptor = cipher.decryptor()

# Decrypt the encrypted data
padded_plaintext = decryptor.update(encrypted_data) + decryptor.finalize()

# Remove the padding from the plaintext
unpadder = padding.PKCS7(128).unpadder()
plaintext = unpadder.update(padded_plaintext)
plaintext += unpadder.finalize()

# Print the plaintext
print(plaintext)
