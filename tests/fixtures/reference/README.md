# Witness v1 reference fixture

TEST ONLY — this key is public and unsuitable for real signing.

The Ed25519 private seed is bytes(range(32)): the 32 bytes 0x00 through 0x1f. Anyone can reproduce its signatures.

sample.txt contains exactly b"hello witness\n". public.pem is SPKI PEM. record.json uses the Witness v1 format. signing-bytes.bin contains the exact signed bytes.

Generated directly with cryptography, hashlib and json, without using Witness serialization or record-creation functions. This is a compatibility fixture, not an independent security audit.

Preserve these files unchanged. Future format versions should receive separate fixtures.
