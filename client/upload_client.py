import sys
import os
import json
import time
import base64

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import socket
import base64

from crypto.rsa_utils import *
from crypto.aes_utils import *
from crypto.hash_utils import *
from logs.logger import write_log

HOST = "127.0.0.1"
PORT = 9999

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client.settimeout(5)

client.connect(
    (HOST, PORT)
)

client.send(
    b"HELLO"
)

response = client.recv(
    1024
).decode()

print(
    "SERVER RESPONSE:",
    response
)

# =====================
# NHẬN PUBLIC KEY
# =====================

public_key_bytes = client.recv(
    4096
)

cloud_public = serialization.load_pem_public_key(
    public_key_bytes
)

print("PUBLIC KEY RECEIVED")

# =====================
# TẠO SESSION KEY
# =====================

session_key = generate_session_key()

print(
    "SESSION KEY:",
    base64.b64encode(session_key).decode()
)

# =====================
# RSA ENCRYPT
# =====================

encrypted_session_key = rsa_encrypt(
    session_key,
    cloud_public
)

client.sendall(
    encrypted_session_key
)

print("SESSION KEY SENT")

metadata = {
    "filename": "video.mp4",
    "size": os.path.getsize(
        "test_files/video.mp4"
    ),
    "timestamp": str(time.time())
}

metadata_bytes = json.dumps(
    metadata
).encode()

sender_private = load_private_key(
    "keys/sender_private.pem"
)

signature = sign_data(
    metadata_bytes,
    sender_private
)

# # GIẢ MẠO DỮ LIỆU SAU KHI ĐÃ KÝ
# metadata_bytes = b"HACKED DATA"

client.sendall(
    len(metadata_bytes).to_bytes(
        4,
        "big"
    )
)

client.sendall(
    metadata_bytes
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

print("METADATA SENT")

# =====================
# READ VIDEO
# =====================

with open(
    "test_files/video.mp4",
    "rb"
) as f:

    video_data = f.read()

# =====================
# AES ENCRYPT
# =====================

iv, ciphertext = encrypt_data(
    video_data,
    session_key
)

print("VIDEO ENCRYPTED")

# =====================
# HASH
# =====================

hash_value = calculate_hash(
    iv + ciphertext
)

# # TEST NACK
# hash_value = "FAKE_HASH"

print("HASH CREATED")

# =====================
# SEND IV
# =====================

client.sendall(
    len(iv).to_bytes(
        4,
        "big"
    )
)

client.sendall(iv)

# =====================
# SEND CIPHERTEXT
# =====================

client.sendall(
    len(ciphertext).to_bytes(
        8,
        "big"
    )
)

client.sendall(
    ciphertext
)

# =====================
# SEND HASH
# =====================

hash_bytes = hash_value.encode()

client.sendall(
    len(hash_bytes).to_bytes(
        4,
        "big"
    )
)

client.sendall(
    hash_bytes
)

print("PACKET SENT")

# =====================
# RECEIVE ACK
# =====================

MAX_RETRY = 3

for attempt in range(MAX_RETRY):

    try:

        response = client.recv(
            1024
        ).decode()

        print(
            "SERVER:",
            response
        )

        if response == "ACK":

            write_log(
                "ACK"
            )

        break

    except socket.timeout:

        print(
            f"TIMEOUT - RETRY {attempt + 1}"
        )

        write_log(
            "TIMEOUT"
        )

else:

    print(
        "UPLOAD FAILED AFTER 3 RETRIES"
    )

client.close()