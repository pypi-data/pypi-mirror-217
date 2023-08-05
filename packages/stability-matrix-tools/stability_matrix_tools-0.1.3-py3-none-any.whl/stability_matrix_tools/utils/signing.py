from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519


def generate_private_key():
    return ed25519.Ed25519PrivateKey.generate()


def generate_public_key(private_key):
    return private_key.public_key()
