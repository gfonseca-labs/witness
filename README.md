# Witness by Blackwood

Has this file changed since its contents were signed?

Witness is a local command-line tool that hashes a file with SHA-256 and signs
a detached integrity record with Ed25519. Later, it checks the record against
a public key and compares the file's current bytes with the signed digest.

With an independently trusted public key, the unchanged file verifies. Changing
even one byte makes verification fail. Renaming unchanged contents still verifies:
the record signs content, not a filename.

Witness does not establish the signer's identity, authorship, creation time,
truthfulness or the safety of a file. You must authenticate the public key
through a trusted channel.

## Install

Python 3.11 or newer on macOS. The tested CI versions are 3.11 and 3.13;
Linux and Windows support has not been established.

```sh
git clone https://github.com/gfonseca-labs/witness.git
cd witness
git checkout v0.1.0
python3 -m venv .venv
. .venv/bin/activate
python -m pip install .
blackwood-witness --help
```

The [v0.1.0 release](https://github.com/gfonseca-labs/witness/releases/tag/v0.1.0)
also provides a wheel, source distribution and checksums. See
[release installation and validation](docs/VALIDATION-v0.1.md).
Runtime dependencies are resolved during installation, not locked.
The unrelated PyPI package named `witness` is not this tool.

## Try it

From the activated environment, create disposable files outside the checkout:

```sh
WITNESS_DEMO_DIR="$(mktemp -d)"
printf 'hello witness\n' > "$WITNESS_DEMO_DIR/example.txt"

blackwood-witness keygen --private-key "$WITNESS_DEMO_DIR/private.pem"
blackwood-witness export-public-key --private-key "$WITNESS_DEMO_DIR/private.pem" --public-key "$WITNESS_DEMO_DIR/public.pem"
blackwood-witness sign "$WITNESS_DEMO_DIR/example.txt" --private-key "$WITNESS_DEMO_DIR/private.pem" --record "$WITNESS_DEMO_DIR/record.json"
blackwood-witness verify "$WITNESS_DEMO_DIR/example.txt" --public-key "$WITNESS_DEMO_DIR/public.pem" --record "$WITNESS_DEMO_DIR/record.json"
```

Choose a disposable password. Key generation asks twice; public-key export and
signing ask once each. Password characters are not displayed. Verification
needs no password and should print `Verified:` with the file path.

Change exactly one byte in a separate copy, then recheck the original:

```sh
printf 'Hello witness\n' > "$WITNESS_DEMO_DIR/changed.txt"
blackwood-witness verify "$WITNESS_DEMO_DIR/changed.txt" --public-key "$WITNESS_DEMO_DIR/public.pem" --record "$WITNESS_DEMO_DIR/record.json"
echo "Verification exit code: $?"
blackwood-witness verify "$WITNESS_DEMO_DIR/example.txt" --public-key "$WITNESS_DEMO_DIR/public.pem" --record "$WITNESS_DEMO_DIR/record.json"
```

Run these commands in an interactive shell: the changed copy intentionally
returns exit code 1. A script with `set -e` would stop there. The original
should verify again with exit code 0. Keep its record unchanged.

This local demonstration creates its own key. It demonstrates the mechanics;
it does not establish trust in a key received from someone else.

## Commands

| Command | Result |
| --- | --- |
| `keygen --private-key PATH` | New password-encrypted Ed25519 private key |
| `export-public-key --private-key PATH --public-key PATH` | Public key and fingerprint |
| `sign FILE --private-key PATH --record PATH` | Detached signed JSON record |
| `verify FILE --public-key PATH --record PATH` | Signature and file-content verification |

Use `blackwood-witness COMMAND --help` for arguments.

Exit codes: **0** for success or help, **1** for failed verification, handled
operational errors or cancellation, and **2** for invalid command-line arguments.

## Keys, files and limitations

- Authenticate the public key or its fingerprint independently. An attacker
  supplying both a record and a key can produce a valid check under their own key.
- Keep real private keys and passwords outside Git and back them up securely.
  Witness has no password recovery, key revocation or trusted timestamp service.
- CLI-created private keys are encrypted PKCS#8 PEM with permissions `0600`.
  Public keys are SubjectPublicKeyInfo PEM. Fingerprints are SHA-256 of
  SubjectPublicKeyInfo DER, prefixed `sha256:`.
- Paths are explicit. No storage or configuration directory is selected automatically.
- Content inputs must be regular files. Final-component symlinks, directories
  and special files are rejected. Key and record inputs use ordinary path reads;
  parent-directory symlinks are not explicitly rejected.
- Keep files unchanged during the operation. Metadata checks detect ordinary
  concurrent changes; they do not provide an atomic snapshot or protection
  against an attacker controlling the filesystem.
- Output commands refuse to overwrite. Publication requires hard links;
  forced termination can leave temporary files, and power-loss persistence is
  not guaranteed. Use trusted directories. Input reads have no general resource quota.

The [threat model](docs/THREAT_MODEL.md) describes the trust boundary and
remaining limitations. No independent security audit is claimed.

## Development

From a checkout of the branch you want to test, with its environment activated:

```sh
python -m pip install -e '.[dev]'
python -m pytest
python -m ruff check .
```

Tests cover parsing, file handling, CLI success and failure paths, and a fixed
version 1 compatibility fixture. Its deterministic key is public and TEST ONLY.

## Documentation

- [Design and module boundaries](docs/DESIGN.md)
- [Version 1 record format](docs/FORMAT.md)
- [Threat model](docs/THREAT_MODEL.md)
- [Reproducible demonstration](docs/DEMO-v0.1.md)
- [Release installation and validation](docs/VALIDATION-v0.1.md)
- [Security reporting](SECURITY.md)
- [Changelog](CHANGELOG.md)

Code: [MIT](LICENSE). Distribution and CLI: `blackwood-witness`; Python module:
`witness`. This project is unrelated to [in-toto Witness](https://github.com/in-toto/witness).
