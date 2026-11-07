# Changelog

## Unreleased

- Reconcile public documentation with the published release, add a complete
  installation path and reproducible demo, and clarify historical validation.

## [0.1.0](https://github.com/gfonseca-labs/witness/releases/tag/v0.1.0) — 2026-10-10

- SHA-256/Ed25519 detached content records and password-encrypted private keys.
- `keygen`, `export-public-key`, `sign` and `verify` commands.
- Strict version 1 format and permanent public TEST-ONLY compatibility fixture.
- Output publication without overwriting and ordinary concurrent-change detection.
- Tests for empty/Unicode files, permissions and malformed records.
- Distribution and CLI named `blackwood-witness`.

macOS was tested with Python 3.11 and 3.13. Linux and Windows support is not
established. See [validation](docs/VALIDATION-v0.1.md) and the
[threat model](docs/THREAT_MODEL.md) for scope and limitations.
