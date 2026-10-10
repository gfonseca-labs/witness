# v0.1 validation

## Current sanitized candidate

[Complete candidate record](RELEASE-CANDIDATE-v0.1.md).

The 63e0bd4 wheel and ownership-normalized source archive matched committed files. Separate fresh installations passed pip check and help. The installed wheel returned original / one-byte changed copy / original results 0 / 1 / 0. The normalized source passed all 85 tests without skips, Ruff and reference verification. Observed runtime: cryptography 50.0.2, cffi 2.1.1 and pycparser 3.11; local Python 3.13.16, pytest 9.1.1 and Ruff 0.17.0. These observations are not a lock.

## Historical development evidence

Earlier private checkpoints record 85 tests, empty/Unicode workflows,
permission denials, malformed records, bounded-memory hashing, 64/512 MiB
signed-record workflows, README reproduction and reinstall preservation.
Their commit/PR IDs describe the private archive, not this fresh repository.
They are earlier observations, not procedures all rerun at this checkpoint.

Five reviewed screenshots show help, keys, signing and verification 0/1/0.
They supersede video; they do not establish public-release reproduction.

## Completion still required

1. Review/merge these documents with passing CI; record the new commit.
2. Repeat history/privacy checks; rebuild, normalize and inspect distributions.
3. Record new hashes/resolved versions; repeat clean-install acceptance.
4. Verify public visibility and private vulnerability reporting.
5. Review tag/release/assets; verify downloaded checksums.
6. Reproduce from the actual public release and check links.
7. Obtain final owner sign-off and update technical SHIPPED status.
