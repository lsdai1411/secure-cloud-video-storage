import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import socket
import base64

from crypto.aes_utils import decrypt_data
from crypto.hash_utils import verify_hash
from crypto.rsa_utils import *

HOST = "127.0.0.1"
PORT = 9999

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind((HOST, PORT))
server.listen(1)

print("SERVER STARTED")

client_socket, address = server.accept()

print("CLIENT:", address)

message = client_socket.recv(
    1024
).decode()

if message == "HELLO":

    client_socket.send(
        b"READY"
    )

    print("READY SENT")

# =====================
# GỬI PUBLIC KEY CLOUD
# =====================

with open(
    "keys/cloud_public.pem",
    "rb"
) as f:

    public_key_bytes = f.read()

client_socket.sendall(
    public_key_bytes
)

print("PUBLIC KEY SENT")

# =====================
# NHẬN SESSION KEY
# =====================

encrypted_session_key = client_socket.recv(
    4096
)

cloud_private = load_private_key(
    "keys/cloud_private.pem"
)

session_key = rsa_decrypt(
    encrypted_session_key,
    cloud_private
)

print(
    "SESSION KEY:",
    base64.b64encode(session_key).decode()
)

import json
metadata_length = int.from_bytes(
    client_socket.recv(4),
    "big"
)

metadata_bytes = client_socket.recv(
    metadata_length
)

signature_length = int.from_bytes(
    client_socket.recv(4),
    "big"
)

signature = client_socket.recv(
    signature_length
)

sender_public = load_public_key(
    "keys/sender_public.pem"
)

result = verify_signature(
    metadata_bytes,
    signature,
    sender_public
)

metadata = json.loads(
    metadata_bytes.decode()
)

print()
print("METADATA:")
print(metadata)

print()
print(
    "SIGNATURE VALID:",
    result
)


# =====================
# RECEIVE IV
# =====================

iv_length = int.from_bytes(
    client_socket.recv(4),
    "big"
)

iv = client_socket.recv(
    iv_length
)

# =====================
# RECEIVE CIPHERTEXT
# =====================

cipher_length = int.from_bytes(
    client_socket.recv(8),
    "big"
)

ciphertext = b""

while len(ciphertext) < cipher_length:

    chunk = client_socket.recv(
        min(4096, cipher_length - len(ciphertext))
    )

    ciphertext += chunk

# =====================
# RECEIVE HASH
# =====================

hash_length = int.from_bytes(
    client_socket.recv(4),
    "big"
)

received_hash = client_socket.recv(
    hash_length
).decode()

print()
print("VIDEO RECEIVED")

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

if not hash_ok:

    client_socket.send(
        b"NACK"
    )

else:

    video_data = decrypt_data(
        ciphertext,
        session_key,
        iv
    )

    with open(
        "cloud_storage/video.mp4",
        "wb"
    ) as f:

        f.write(video_data)

    print("FILE SAVED")

    client_socket.send(
        b"ACK"
    )

    print("ACK SENT")




# print()
# print("RAW METADATA:")
# print(metadata_bytes)

# print()
# print(
#     "SIGNATURE VALID:",
#     result
# )

client_socket.close()
server.close()