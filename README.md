# Witness by Blackwood

> Historical evidence below refers to the private development archive.
> Old commit hashes, PR numbers and scan counts do not describe this
> fresh repository. Fresh-history CI, scanning and rebuilt-artifact
> acceptance remain required before release.


A local CLI for signing file-integrity records and verifying them later.

**Release status:** v0.1.0 release candidate; not yet publicly released.
The tested platform is macOS. CI targets Python 3.11 and 3.13.

## Working example

From an installed Witness environment, create disposable demonstration
files outside the repository:

```bash
WITNESS_DEMO_DIR="$(mktemp -d)"
printf 'hello witness\n' > "$WITNESS_DEMO_DIR/example.txt"

blackwood-witness keygen --private-key "$WITNESS_DEMO_DIR/private.pem"
blackwood-witness export-public-key --private-key "$WITNESS_DEMO_DIR/private.pem" --public-key "$WITNESS_DEMO_DIR/public.pem"
blackwood-witness sign "$WITNESS_DEMO_DIR/example.txt" --private-key "$WITNESS_DEMO_DIR/private.pem" --record "$WITNESS_DEMO_DIR/record.json"
blackwood-witness verify "$WITNESS_DEMO_DIR/example.txt" --public-key "$WITNESS_DEMO_DIR/public.pem" --record "$WITNESS_DEMO_DIR/record.json"
```

Choose a disposable password and enter it at the prompts. Terminal does
not display password characters. Verification does not ask for a password.

Demonstrate an exact one-byte change in a separate copy:

```bash
printf 'Hello witness\n' > "$WITNESS_DEMO_DIR/changed.txt"
blackwood-witness verify "$WITNESS_DEMO_DIR/changed.txt" --public-key "$WITNESS_DEMO_DIR/public.pem" --record "$WITNESS_DEMO_DIR/record.json"
echo "Verification exit code: $?"
blackwood-witness verify "$WITNESS_DEMO_DIR/example.txt" --public-key "$WITNESS_DEMO_DIR/public.pem" --record "$WITNESS_DEMO_DIR/record.json"
```

The changed copy should fail with exit code 1. The unchanged original
should still succeed. Keep the original record unchanged.

## What verification proves

Successful verification means the record signature verifies against the
supplied public key and the supplied file's bytes match its signed
SHA-256 digest.

Authenticate the public key or its fingerprint through a trusted channel.
A key supplied with an untrusted file does not establish signer identity.

Witness does not prove truthfulness, original authorship, named identity,
creation time, malware safety or uncompromised keys. It signs content,
not the filename, location, permissions or modification time.

## Installation

Use Python 3.11 or newer on macOS. From a Witness source checkout:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
blackwood-witness --help
```

This installs the checkout as a regular package. Clean wheel and source-distribution installations passed on macOS
during preparation. See [validation evidence](docs/VALIDATION-v0.1.md).

For development, use:

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m ruff check .
```

In later Terminal sessions, activate the environment again.
A GitHub release installation link will be added when the release exists.

## Keys and paths

All key and record paths are explicit. Witness does not automatically
create or select a configuration directory. `~/.witness` is a manual
storage convention.

CLI-generated private keys are password-encrypted PKCS#8 PEM with
owner-only permissions. Public keys use SubjectPublicKeyInfo PEM.
Fingerprints are SHA-256 of SubjectPublicKeyInfo DER, prefixed `sha256:`.

Keep real keys and passwords outside Git. Back them up securely.
Witness cannot recover a lost password and has no key revocation service.

## File handling

Content inputs must be regular files. Symlinks in the final input-path
component, directories and special files are rejected. Parent-directory
symlinks are not explicitly rejected.

Files should remain unchanged during signing and verification.
Metadata checks detect ordinary concurrent changes or replacement;
they do not provide an atomic snapshot or protect against an attacker
controlling the filesystem.

Output commands refuse to overwrite existing paths. Complete temporary
files are published using hard links. Handled failures clean up the
temporary file; forced termination can leave it behind. This requires
hard-link support and does not guarantee persistence after power loss.
Use trusted directories.

## Record format

Version 1 has exactly two top-level fields: `payload` and `signature`.
The payload contains only integer `version: 1`, `file_sha256` and `signer`.
The Ed25519 signature uses 128 lowercase hexadecimal characters.

The signature covers a fixed domain prefix and canonical ASCII payload
JSON. No filename, size or timestamp is signed. Renaming unchanged
contents does not invalidate a record.

See [FORMAT.md](docs/FORMAT.md) for the exact signing bytes and parsing rules.

## Exit codes

- 0: success, including successful verification and help.
- 1: failed verification, handled operational errors or cancellation.
- 2: invalid or missing command-line arguments.

## Tests and review

Tests include temporary generated keys and an explicitly public,
deterministic TEST-ONLY key in `tests/fixtures/reference/`.
Never use that reference key for real signing.

85 tests and Ruff passed locally during release preparation.
The acceptance source archive also passed all 85 tests without skips.
Clean wheel and source installation checks passed.
Merged acceptance checkpoint 557f0d2 passed macOS Python 3.11/3.13 CI.
Documentation-closeout checkpoint 75ef73e passed all 85 tests and Ruff
locally. Merged checkpoint f98c729 passed macOS Python 3.11/3.13 CI.
Technical-release preparation checkpoint 79167c9 passed all 85 tests,
Ruff and pip check. Final technical-closeout CI, final artifact validation
and reproduction from the public release remain pending.
No independent security audit is established.
Linux and Windows support is not established.

## Documentation and reporting

- [Record format](docs/FORMAT.md)
- [Threat model and limitations](docs/THREAT_MODEL.md)
- [Design](docs/DESIGN.md)
- [Screenshot demonstration and verification limits](docs/DEMO-v0.1.md)
- [Security reporting policy](SECURITY.md)
- [Owner-approved technical release scope](docs/RELEASE-APPROVAL-v0.1.md)
- [Changelog](CHANGELOG.md)
- [MIT license](LICENSE)

Private vulnerability reporting must be enabled and verified before
the public release is announced.

## Command help

```bash
blackwood-witness --help
blackwood-witness keygen --help
blackwood-witness export-public-key --help
blackwood-witness sign --help
blackwood-witness verify --help
```

## Project identity

Public name: Witness by Blackwood. Package and CLI command: `blackwood-witness`.
The internal Python module remains `witness`; the version 1 record format is unchanged.

This project is unrelated to in-toto Witness. Do not install the unrelated PyPI package named `witness` to obtain this tool.
