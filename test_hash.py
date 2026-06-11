from crypto.hash_utils import *

message = b"HELLO CLOUD"

hash_value = calculate_hash(
    message
)

tampered_message = b"HACKED CLOUD"

result = verify_hash(
    tampered_message,
    hash_value
)

print(result)