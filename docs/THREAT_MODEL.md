# Witness v0.1 threat model

## Protected property

Given an authentic verification public key, successful verification
establishes that the signed record verifies under that key and that the
supplied file's bytes match its signed SHA-256 digest, subject to the
security of SHA-256, Ed25519 and the implementation.

## Trust assumptions

The user authenticates the public key or its fingerprint through a
trusted channel. The signing private key and password remain protected.
The operating system, Python runtime, cryptography dependency and
installed Witness code are trusted.

The file should remain unchanged throughout signing or verification.

## Attacker capabilities considered

An attacker may supply altered files, records or public keys.
Strict parsing rejects malformed and ambiguous records. Verification
rejects mismatched fingerprints, invalid signatures and digest mismatches.

An attacker-selected public key does not establish the identity of a
claimed signer. Replacing both a record and its supplied key can produce
a valid check under the attacker's key.

## Key compromise and replay

A compromised private key allows new valid signatures. Witness has no
key revocation, key recovery, trusted timestamp or freshness mechanism.

An old valid file and record remain valid under the same trusted key.
Verification does not establish that they are the latest version.

## Local file handling

Content hashing accepts regular files and rejects a symlink in the final
path component, directories and special files. Opening without following
that final symlink and comparing file identity, size and modification
metadata detects ordinary changes or replacement during the read.

This is not an atomic filesystem snapshot or a guarantee against an
attacker controlling the filesystem. Parent-directory symlinks are not
explicitly rejected. Changes after hashing are outside the observed check.

Outputs are written to temporary files beside the destination, flushed,
then published using a hard link that cannot replace an existing path.
Private output permissions are 0600; public keys and records use 0644.

Handled failures clean up temporary files. Forced termination can leave
a temporary file. Publication is not a guarantee of survival after power
loss, and requires filesystem hard-link support. Use trusted directories.

## Non-goals

Witness does not prove truthfulness, original authorship, named identity,
creation time, malware safety, legal validity or uncompromised keys.
It does not provide encryption of signed files, a network service,
a transparency log or protection against a compromised local machine.

## Support and review scope

The tested platform is macOS, with CI on Python 3.11 and 3.13.
Linux and Windows support is not established.

Automated tests and development review are not an independent security
audit. No independent audit is established by the development evidence.
No production-grade security assurance is claimed.
