# Witness v0.1 design

## Scope

Witness is a local CLI with four commands:
`keygen`, `export-public-key`, `sign` and `verify`.

It uses explicit file paths. `~/.witness` is a user storage convention,
not an automatically selected configuration directory.

## Module boundaries

- `hashing.py`: streaming SHA-256, regular-file checks and observed-change detection.
- `keys.py`: Ed25519 generation, standard key serialization/loading and fingerprints.
- `records.py`: strict version 1 parsing, canonical signing and verification.
- `file_io.py`: complete-file publication without replacing existing destinations.
- `cli.py`: arguments, password prompts, output and handled errors.

Cryptographic primitives come from cryptography; Witness does not
implement its own SHA-256 or Ed25519 algorithms.

## Key handling

The CLI requires a nonempty password for private-key operations.
Key generation asks for confirmation and writes encrypted PKCS#8 PEM.
Verification uses only a public key and never prompts for a password.

The lower-level serialization helper can produce unencrypted private
keys when called without a password. The CLI does not use that mode.

## Output publication

Existing output paths are rejected before password prompts.
The shared writer also prevents replacement if a destination appears
after that initial check.

A temporary file in the destination directory is written, flushed and
synchronized before hard-link publication. The temporary name is then
removed. This preserves no-overwrite behavior without exposing a
partially written destination.

See THREAT_MODEL.md for cleanup, filesystem and durability limitations.

## Compatibility decisions

Version 1 signs only `version`, `file_sha256` and `signer`.
Signatures use lowercase hex. There is no `seal` command, filename
warning or signed timestamp.

These decisions supersede the original planning contract. The internal
project archive preserves that historical contract and its reconciliation.
The source briefs did not establish every reason for the differences.

## CLI outcomes

- 0: success, including successful verification and help.
- 1: failed verification, handled operational errors or cancellation.
- 2: invalid command-line arguments.

CLI operational handling includes OSError, ValueError and TypeError;
EOFError and KeyboardInterrupt produce a cancellation message.

## Validation

Tests cover the core functions and CLI, integrity failures, strict
record parsing, safe output failures, unsupported content inputs,
observed concurrent changes and a permanent compatibility fixture.

The public reference key is explicitly TEST ONLY. Other cryptographic
tests generate temporary keys. Test coverage does not imply exhaustive
failure handling or independent security certification.
