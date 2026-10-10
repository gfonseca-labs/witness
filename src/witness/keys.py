"""Ed25519 key utilities."""

from hashlib import sha256

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)


def generate_private_key() -> Ed25519PrivateKey:
    """Generate a new Ed25519 private key."""
    return Ed25519PrivateKey.generate()


def serialize_private_key(
    private_key: Ed25519PrivateKey,
    password: bytes | None = None,
) -> bytes:
    """Serialize an Ed25519 private key as PKCS#8 PEM."""
    if password is None:
        encryption = serialization.NoEncryption()
    else:
        encryption = serialization.BestAvailableEncryption(password)

    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption,
    )


def serialize_public_key(public_key: Ed25519PublicKey) -> bytes:
    """Serialize an Ed25519 public key as SubjectPublicKeyInfo PEM."""
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def load_private_key(
    data: bytes,
    password: bytes | None = None,
) -> Ed25519PrivateKey:
    """Load an Ed25519 private key from PEM data."""
    key = serialization.load_pem_private_key(data, password=password)

    if not isinstance(key, Ed25519PrivateKey):
        raise TypeError("Expected an Ed25519 private key.")

    return key


def load_public_key(data: bytes) -> Ed25519PublicKey:
    """Load an Ed25519 public key from PEM data."""
    key = serialization.load_pem_public_key(data)

    if not isinstance(key, Ed25519PublicKey):
        raise TypeError("Expected an Ed25519 public key.")

    return key


def public_key_fingerprint(public_key: Ed25519PublicKey) -> str:
    """Return a SHA-256 fingerprint for an Ed25519 public key."""
    der = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return f"sha256:{sha256(der).hexdigest()}"