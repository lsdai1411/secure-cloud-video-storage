from crypto.aes_utils import *

key = generate_session_key()

message = b"HELLO AES CBC"

iv, ciphertext = encrypt_data(
    message,
    key
)

plaintext = decrypt_data(
    ciphertext,
    key,
    iv
)

print("ORIGINAL :", message)
print("DECRYPT  :", plaintext)

print(
    "MATCH =",
    message == plaintext
)