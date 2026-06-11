import sys
import os
import socket
import base64

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from crypto.aes_utils import *
from crypto.rsa_utils import *

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
    "SESSION KEY:",
    base64.b64encode(
        session_key
    ).decode()
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

client.close()