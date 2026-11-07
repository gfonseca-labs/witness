# Witness v0.1.0: installation and validation

Published on 10 October 2026:
[v0.1.0](https://github.com/gfonseca-labs/witness/releases/tag/v0.1.0).
Release commit: `66cf824475e9e9cb6ee27a02814b942b07c0fb6b`.
Later documentation on `main` is not part of the original release artifacts.

## Install a release artifact

Download the wheel and `SHA256SUMS.txt` from the release into a disposable
directory. On macOS, verify the wheel against the published digest:

```sh
printf '%s  %s\n' b1eefbbf1b8719a2040a4b1da961ea85638953b23af4c45bffefee99c5fbc70a blackwood_witness-0.1.0-py3-none-any.whl | shasum -a 256 -c -
python3 -m venv .venv
. .venv/bin/activate
python -m pip install ./blackwood_witness-0.1.0-py3-none-any.whl
python -m pip check
blackwood-witness --help
```

The source distribution is an alternative. Its published SHA-256 is
`2c9b4e9d5e525501f91a5bddae7462ab5ce87141c878e07dd1f023132fd8dd5c`.
Install it with `python -m pip install ./blackwood_witness-0.1.0.tar.gz`.
Checksums detect mismatch with the published assets; they do not independently
authenticate the publisher. Dependencies are resolved during installation.

Run the [README example](../README.md#try-it). Expected verification sequence:
original **0**, one-byte changed copy **1**, original **0**.

## Published release evidence

The release notes report:

- [macOS Python 3.11/3.13 CI passed](https://github.com/gfonseca-labs/witness/actions/runs/38088319649).
- The shipped source passed 85 tests without skips, Ruff and reference verification.
- Fresh wheel and normalized-source installations passed dependency checks and help.
- The installed wheel passed the original/changed/original sequence above.
- Bounded secret, history, machine-identifier and archive-metadata checks passed.

These are release-time observations, not a fresh audit of every subsequent
commit or dependency resolution.

## Public-download check — 7 November 2026

The wheel and source distribution were downloaded from the public release and
both matched the hashes above. All 85 tests in the downloaded source passed
on macOS with Python 3.13. The wheel was installed into a separate target
directory and its command dispatcher completed key generation, public-key
export, signing and the original/changed/original sequence **0 / 1 / 0**.
Password prompts were supplied by a test harness with a disposable password;
this was not a separate-user interactive usability trial or a dependency-lock
reproduction. The check used cryptography 50.0.2, cffi 2.1.1 and pycparser 3.12.
It does not establish independent security certification or owner sign-off.

## Additional evidence and limits

- [Earlier candidate validation](RELEASE-CANDIDATE-v0.1.md)
- [Large-file measurements](LARGE-FILE-VALIDATION-v0.1.md)
- [Dependency review](DEPENDENCY-REVIEW-v0.1.md)
- [History review](HISTORY-REVIEW-v0.1.md)

Historical checks have the dates and scopes stated on those pages. They are
not current security certifications. macOS is the tested platform; Linux and
Windows support and an independent security audit are not established.
