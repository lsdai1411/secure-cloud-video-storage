from crypto.aes_utils import *

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

with open(
    "encrypted_video.bin",
    "wb"
) as f:

    f.write(ciphertext)

decrypted_data = decrypt_data(
    ciphertext,
    key,
    iv
)

with open(
    "video_restored.mp4",
    "wb"
) as f:

    f.write(decrypted_data)

print("DONE")