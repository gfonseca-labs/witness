from witness.keys import (
    generate_private_key,
    load_private_key,
    load_public_key,
    public_key_fingerprint,
    serialize_private_key,
    serialize_public_key,
)


def test_ed25519_key_round_trip() -> None:
    private_key = generate_private_key()
    public_key = private_key.public_key()

    password = b"test-password"

    private_pem = serialize_private_key(private_key, password=password)
    public_pem = serialize_public_key(public_key)

    loaded_private_key = load_private_key(private_pem, password=password)
    loaded_public_key = load_public_key(public_pem)

    message = b"hello witness"
    signature = loaded_private_key.sign(message)

    loaded_public_key.verify(signature, message)

    assert public_key_fingerprint(loaded_public_key) == public_key_fingerprint(
        public_key
    )