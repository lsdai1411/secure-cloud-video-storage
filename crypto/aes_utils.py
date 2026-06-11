import os

from cryptography.hazmat.primitives.ciphers import (
    Cipher,
    algorithms,
    modes
)

from cryptography.hazmat.primitives import padding


def generate_session_key():

    return os.urandom(32)


def encrypt_data(data, key):

    iv = os.urandom(16)

    padder = padding.PKCS7(128).padder()

    padded_data = padder.update(data)
    padded_data += padder.finalize()

    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv)
    )

    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(
        padded_data
    ) + encryptor.finalize()

    return iv, ciphertext


def decrypt_data(ciphertext, key, iv):

    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv)
    )

    decryptor = cipher.decryptor()

    padded_data = decryptor.update(
        ciphertext
    ) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()

    data = unpadder.update(
        padded_data
    ) + unpadder.finalize()

    return data