from crypto.rsa_utils import generate_keypair

generate_keypair(
    "keys/sender_private.pem",
    "keys/sender_public.pem"
)

generate_keypair(
    "keys/cloud_private.pem",
    "keys/cloud_public.pem"
)

print("KEYS CREATED")