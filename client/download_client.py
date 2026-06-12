import sys
import os
import socket
import base64
import json
import time

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from crypto.aes_utils import *
from crypto.rsa_utils import *
from crypto.hash_utils import *

HOST = "127.0.0.1"
PORT = 9999

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client.connect(
    (HOST, PORT)
)

# DOWNLOAD MODE
client.send(
    b"DOWNLOAD"
)

response = client.recv(
    1024
).decode()

print(
    "SERVER RESPONSE:",
    response
)

# NHẬN PUBLIC KEY

public_key_bytes = client.recv(
    4096
)

cloud_public = serialization.load_pem_public_key(
    public_key_bytes
)

print(
    "PUBLIC KEY RECEIVED"
)

# TẠO SESSION KEY

session_key = generate_session_key()

print(
    "SESSION KEY GENERATED"
)

# RSA ENCRYPT

encrypted_session_key = rsa_encrypt(
    session_key,
    cloud_public
)

client.sendall(
    encrypted_session_key
)

print(
    "SESSION KEY SENT"
)

# =====================
# DOWNLOAD REQUEST
# =====================

request = {
    "filename": "video.mp4",
    "timestamp": str(time.time())
}

request_bytes = json.dumps(
    request
).encode()

sender_private = load_private_key(
    "keys/sender_private.pem"
)

signature = sign_data(
    request_bytes,
    sender_private
)

client.sendall(
    len(request_bytes).to_bytes(
        4,
        "big"
    )
)

client.sendall(
    request_bytes
)

client.sendall(
    len(signature).to_bytes(
        4,
        "big"
    )
)

client.sendall(
    signature
)

print(
    "DOWNLOAD REQUEST SENT"
)

response = client.recv(
    1024
).decode()

print(
    "SERVER:",
    response
)

# =====================
# RECEIVE IV
# =====================

iv_length = int.from_bytes(
    client.recv(4),
    "big"
)

iv = client.recv(
    iv_length
)

print(
    "IV RECEIVED"
)

# =====================
# RECEIVE CIPHERTEXT
# =====================

cipher_length = int.from_bytes(
    client.recv(8),
    "big"
)

ciphertext = b""

while len(ciphertext) < cipher_length:

    chunk = client.recv(
        min(
            4096,
            cipher_length - len(ciphertext)
        )
    )

    ciphertext += chunk

print(
    "CIPHERTEXT RECEIVED"
)

print(
    "SIZE:",
    len(ciphertext)
)

# =====================
# RECEIVE HASH
# =====================

hash_length = int.from_bytes(
    client.recv(4),
    "big"
)

received_hash = client.recv(
    hash_length
).decode()

print(
    "HASH RECEIVED"
)

print(
    received_hash[:20],
    "..."
)

# =====================
# VERIFY HASH
# =====================

hash_ok = verify_hash(
    iv + ciphertext,
    received_hash
)

print(
    "HASH VALID:",
    hash_ok
)

# =====================
# AES DECRYPT
# =====================

video_data = decrypt_data(
    ciphertext,
    session_key,
    iv
)

print(
    "VIDEO DECRYPTED"
)

# =====================
# SAVE VIDEO
# =====================


os.makedirs(
    "downloads",
    exist_ok=True
)

with open(
    "downloads/video.mp4",
    "wb"
) as f:

    f.write(video_data)

print(
    "VIDEO SAVED"
)

from logs.logger import write_log

write_log(
    "DOWNLOAD SUCCESS - video.mp4"
)

# =====================
# SEND ACK/NACK
# =====================

if hash_ok:

    client.send(
        b"ACK"
    )

    print(
        "ACK SENT"
    )
    
    write_log(
        "ACK"
    )

else:

    client.send(
        b"NACK"
    )

    print(
        "NACK SENT"
    )

client.close()