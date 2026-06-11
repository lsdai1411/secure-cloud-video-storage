import hashlib


def calculate_hash(data):

    return hashlib.sha512(
        data
    ).hexdigest()


def verify_hash(data, received_hash):

    new_hash = hashlib.sha512(
        data
    ).hexdigest()

    return new_hash == received_hash