from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes


def generate_keypair(private_path, public_path):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    with open(private_path, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    with open(public_path, "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )


def load_private_key(path):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None
        )


def load_public_key(path):
    with open(path, "rb") as f:
        return serialization.load_pem_public_key(
            f.read()
        )


def sign_data(data, private_key):
    return private_key.sign(
        data,
        padding.PKCS1v15(),
        hashes.SHA512()
    )


def verify_signature(data, signature, public_key):
    try:
        public_key.verify(
            signature,
            data,
            padding.PKCS1v15(),
            hashes.SHA512()
        )
        return True
    except:
        return False


def rsa_encrypt(data, public_key):
    return public_key.encrypt(
        data,
        padding.PKCS1v15()
    )


def rsa_decrypt(ciphertext, private_key):
    return private_key.decrypt(
        ciphertext,
        padding.PKCS1v15()
    )