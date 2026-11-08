# Witness v0.1.0 release scope

The [technical release](https://github.com/gfonseca-labs/witness/releases/tag/v0.1.0)
was published on 10 October 2026. Its source commit, checksums and reported
validation are collected in [release validation](VALIDATION-v0.1.md).

These are the historical v0.1.0 scope and limitations. Use the
[current installation guide](VALIDATION.md) for the latest source and artifacts.

## Accepted technical scope

Four local commands: key generation, public-key export, signing and verification.
Version 1 signs content digests, not identity, filenames or timestamps.

## Remaining limitations

- [Durability and portability](https://github.com/gfonseca-labs/witness/issues/1):
  hard links required; power-loss persistence is not guaranteed.
- [Path handling and input limits](https://github.com/gfonseca-labs/witness/issues/2):
  no atomic snapshot, incomplete parent-symlink protection and no general input quota.
- [Additional platforms](https://github.com/gfonseca-labs/witness/issues/3):
  Linux and Windows support is not established.

Issue links identify follow-up topics; they do not imply those limitations
have been resolved. No independent security audit is claimed.
