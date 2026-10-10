# Witness record format — version 1

This specification describes the implemented version 1 format.
It supersedes the original planned format with filenames, sizes,
timestamps and Base64url signatures. Those fields are not implemented.

## Record structure

A UTF-8 JSON record contains exactly two top-level fields:
`payload` and `signature`.

The payload contains exactly:

| Field | Required value |
| --- | --- |
| `version` | JSON integer `1`; booleans are rejected |
| `file_sha256` | Exactly 64 lowercase hexadecimal characters |
| `signer` | `sha256:` followed by exactly 64 lowercase hexadecimal characters |

`signature` is exactly 128 lowercase hexadecimal characters representing
the 64-byte Ed25519 signature.

Unknown fields, missing fields, duplicate object fields, unsupported
versions and invalid field types or encodings are rejected.

## File digest

`file_sha256` is SHA-256 of the file's bytes, without text decoding or
newline normalization. Hashing reads chunks of at most 1 MiB.

The format does not sign a filename, path, size, permission, timestamp
or named identity. Renaming an unchanged file does not invalidate it.

## Public-key fingerprint

The signer fingerprint is:

`sha256:` + lowercase hexadecimal SHA-256 of the public key's
SubjectPublicKeyInfo DER encoding.

Exported public keys use SubjectPublicKeyInfo PEM.
CLI-created private keys use password-encrypted PKCS#8 PEM.

## Exact signing bytes

1. Serialize only the payload with Python's equivalent of:
   `json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)`.
2. Encode that JSON as ASCII.
3. Prepend the ASCII bytes `witness-record-v1` and one LF byte (`0x0a`).
4. Sign the resulting bytes with Ed25519.

There is no trailing newline in the signing bytes.
The signature field is excluded.

The saved JSON is human-readable and ends with a newline. Its whitespace
and field order do not change the canonical signing bytes.

## Verification

The supplied public key must be Ed25519. Its fingerprint must match
`payload.signer`, and the Ed25519 signature must verify against the
canonical signing bytes. File verification additionally requires the
supplied file's SHA-256 digest to match `payload.file_sha256`.

Authenticating the supplied public key is the caller's responsibility.

## Compatibility reference

`tests/fixtures/reference/` contains a fixed sample, public key, record
and exact signing bytes. Its deterministic private seed is public,
documented and TEST ONLY. It must never be used for real signing.

Preserve this fixture unchanged. An incompatible format change requires
a new version and separate fixtures.
