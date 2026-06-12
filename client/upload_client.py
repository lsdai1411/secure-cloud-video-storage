import sys
import os
import json
import time
import socket

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from crypto.rsa_utils import *
from crypto.aes_utils import *
from crypto.hash_utils import *
from logs.logger import write_log

HOST = "127.0.0.1"
PORT = 9999

video_path = "test_files/video.mp4"

if len(sys.argv) > 1:

    video_path = sys.argv[1]


def upload_once(video_path):

    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    client.settimeout(5)

    try:

        client.connect(
            (HOST, PORT)
        )

        # =====================
        # HELLO
        # =====================

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

        if response != "READY":

            client.close()

            return False

        # =====================
        # NHẬN PUBLIC KEY
        # =====================

        public_key_bytes = client.recv(
            4096
        )

        cloud_public = serialization.load_pem_public_key(
            public_key_bytes
        )

        print(
            "PUBLIC KEY RECEIVED"
        )

        # =====================
        # SESSION KEY
        # =====================

        session_key = generate_session_key()

        print(
            "SESSION KEY GENERATED"
        )

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
        # METADATA
        # =====================

        metadata = {
            "filename": os.path.basename(
                video_path
            ),
            "size": os.path.getsize(
                video_path
            ),
            "timestamp": str(
                time.time()
            )
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

        print(
            "METADATA SENT"
        )

        # =====================
        # READ VIDEO
        # =====================

        with open(
            video_path,
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

        client.sendall(
            len(iv).to_bytes(
                4,
                "big"
            )
        )

        client.sendall(
            iv
        )

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

        print(
            "PACKET SENT"
        )

        # =====================
        # RECEIVE ACK/NACK
        # =====================

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

            client.close()

            return True

        client.close()

        return False

    except socket.timeout:

        print(
            "TIMEOUT"
        )

        write_log(
            "TIMEOUT"
        )

        client.close()

        return False

    except Exception as e:

        print(
            "ERROR:",
            e
        )

        client.close()

        return False


# =====================
# RETRY LOGIC
# =====================

MAX_RETRY = 3

for attempt in range(MAX_RETRY):

    print()
    print(
        f"UPLOAD ATTEMPT {attempt + 1}"
    )

    success = upload_once(
        video_path
    )

    if success:

        print(
            "UPLOAD SUCCESS"
        )

        break

    if attempt < MAX_RETRY - 1:

        print(
            "RETRYING..."
        )

        time.sleep(5)

else:

    print(
        "UPLOAD FAILED AFTER 3 RETRIES"
    )