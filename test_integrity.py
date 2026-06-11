from crypto.aes_utils import *
from crypto.hash_utils import *

with open(
    "test_files/video.mp4",
    "rb"
) as f:

    video_data = f.read()

key = generate_session_key()

iv, ciphertext = encrypt_data(
    video_data,
    key
)

hash_value = calculate_hash(
    iv + ciphertext
)

ciphertext = bytearray(ciphertext)

ciphertext[100] ^= 1

ciphertext = bytes(ciphertext)

print(
    verify_hash(
        iv + ciphertext,
        hash_value
    )
)