from crypto.rsa_utils import *

private_key = load_private_key(
    "keys/sender_private.pem"
)

public_key = load_public_key(
    "keys/sender_public.pem"
)

message = b"HELLO CLOUD"

signature = sign_data(
    message,
    private_key
)

tampered_message = b"HACKED CLOUD"

result = verify_signature(
    tampered_message,
    signature,
    public_key
)

print("VERIFY =", result)