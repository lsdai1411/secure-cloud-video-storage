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

# from crypto.aes_utils import decrypt_data
# from crypto.hash_utils import verify_hash
from crypto.rsa_utils import *
from crypto.aes_utils import *
from crypto.hash_utils import *
from logs.logger import write_log


def get_network_mode():

    try:

        with open(
            "server/network_mode.txt",
            "r"
        ) as f:

            return f.read().strip()

    except:

        return "NORMAL"

used_timestamps = set()

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

# =====================
# UPLOAD MODE
# =====================

if message == "HELLO":

    is_download = False

    client_socket.send(
        b"READY"
    )

    print("UPLOAD MODE")
    print("READY SENT")



# =====================
# DOWNLOAD MODE
# =====================

elif message == "DOWNLOAD":
    is_download = True

    client_socket.send(
        b"READY"
    )

    print("DOWNLOAD MODE")
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
    "SESSION KEY ESTABLISHED"
)

if is_download:

    print("DOWNLOAD HANDSHAKE SUCCESS")

    # =====================
    # RECEIVE REQUEST
    # =====================

    request_length = int.from_bytes(
        client_socket.recv(4),
        "big"
    )

    request_bytes = client_socket.recv(
        request_length
    )

    signature_length = int.from_bytes(
        client_socket.recv(4),
        "big"
    )

    signature = client_socket.recv(
        signature_length
    )

    # =====================
    # VERIFY SIGNATURE
    # =====================

    sender_public = load_public_key(
        "keys/sender_public.pem"
    )

    result = verify_signature(
        request_bytes,
        signature,
        sender_public
    )

    print()
    print("DOWNLOAD REQUEST:")
    print(request_bytes.decode())

    print()
    print(
        "AUTH VALID:",
        result
    )

    if result:

        client_socket.send(
            b"ACK_AUTH"
        )

        # =====================
        # READ VIDEO
        # =====================

        with open(
            "cloud_storage/video.mp4",
            "rb"
        ) as f:

            video_data = f.read()

        print()
        print(
            "VIDEO SIZE:",
            len(video_data),
            "bytes"
        )

    # =====================
    # AES ENCRYPT
    # =====================

    iv, ciphertext = encrypt_data(
        video_data,
        session_key
    )

    print(
        "VIDEO ENCRYPTED"
    )

    # =====================
    # HASH
    # =====================

    hash_value = calculate_hash(
        iv + ciphertext
    )

    print(
        "HASH CREATED"
    )

    # =====================
    # SEND IV
    # =====================

    client_socket.sendall(
        len(iv).to_bytes(
            4,
            "big"
        )
    )

    client_socket.sendall(
        iv
    )

    print(
        "IV SENT"
    )

    # =====================
    # SEND CIPHERTEXT
    # =====================

    client_socket.sendall(
        len(ciphertext).to_bytes(
            8,
            "big"
        )
    )

    client_socket.sendall(
        ciphertext
    )

    print(
        "CIPHERTEXT SENT"
    )

    # =====================
    # SEND HASH
    # =====================

    hash_bytes = hash_value.encode()

    client_socket.sendall(
        len(hash_bytes).to_bytes(
            4,
            "big"
        )
    )

    client_socket.sendall(
        hash_bytes
    )

    print(
        "HASH SENT"
    )

    # =====================
    # RECEIVE ACK/NACK
    # =====================

    response = client_socket.recv(
        1024
    ).decode()

    print()
    print(
        "CLIENT RESPONSE:",
        response
    )

    client_socket.close()
    server.close()
    exit()

import json
import time

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
# ANTI REPLAY CHECK
# =====================

timestamp = float(
    metadata["timestamp"]
)

if timestamp in used_timestamps:

    print()
    print(
        "REPLAY DETECTED"
    )

    write_log(
        "REPLAY DETECTED"
    )

    client_socket.close()
    server.close()
    exit()

used_timestamps.add(
    timestamp
)

current_time = time.time()

if abs(
    current_time - timestamp
) > 30:

    print()
    print(
        "EXPIRED REQUEST"
    )

    write_log(
        "EXPIRED REQUEST"
    )

    client_socket.close()
    server.close()
    exit()


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

# import random

# if random.random() < 0.3:

#     print("PACKET LOST")

#     client_socket.close()

#     exit()

print(
    "HASH VALID:",
    hash_ok
)

if not hash_ok:

    client_socket.send(
        b"NACK"
    )

    write_log(
        "INTEGRITY ERROR"
    )

    write_log(
        "NACK"
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

    write_log(
        f"UPLOAD SUCCESS - {metadata['filename']}"
    )

    # import time

    # time.sleep(6)

    mode = get_network_mode()

    if mode == "PACKET_LOSS":

        write_log(
            "PACKET LOSS SIMULATED"
        )

        client_socket.send(
            b"NACK"
        )

        print(
            "NACK SENT"
        )

    else:

        client_socket.send(
            b"ACK"
        )

        print(
            "ACK SENT"
        )



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