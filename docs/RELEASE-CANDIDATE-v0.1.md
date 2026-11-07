# Historical candidate validation — 10 October 2026

This records an earlier candidate, not the published release. Use
[release validation](VALIDATION-v0.1.md) for the release commit and asset hashes.

Checkpoint: 63e0bd422ef4ac11a44e053df9f369111216558c

Candidate checkpoint: 63e0bd422ef4ac11a44e053df9f369111216558c. Fresh PR #4 is merged. macOS Python 3.11.9 and 3.13.15 CI passed 85 tests and Ruff. Run: https://github.com/gfonseca-labs/witness/actions/runs/38085266592

At 63e0bd4, Gitleaks 8.30.1 reported no leaks across 4 scanned commits, approximately 105.98 KB, exit 0. A separate audit checked all 6 reachable commits and 50 unique file versions, including commit metadata; no checked machine identifiers were found. Supplied final CI job logs showed hosted-runner paths and no checked personal machine identifiers. These are bounded reviews, not exhaustive guarantees or independent audits.

## Artifacts and installations

The 63e0bd4 wheel and ownership-normalized source archive matched committed files. Separate fresh installations passed pip check and help. The installed wheel returned original / one-byte changed copy / original results 0 / 1 / 0. The normalized source passed all 85 tests without skips, Ruff and reference verification. Observed runtime: cryptography 50.0.2, cffi 2.1.1 and pycparser 3.11; local Python 3.13.16, pytest 9.1.1 and Ruff 0.17.0. These observations are not a lock.

Source ownership was normalized to IDs 0/0 and empty names. Gzip filename
metadata was omitted; every file byte was preserved. Wheel ZIP metadata and
source tar metadata/content passed the checked identifier audit.

## Candidate SHA-256

```text
908717b9b926c9317802bdd70cdb77ed573e43c47bf5d7a2dfcd5fd86270e454  blackwood_witness-0.1.0-py3-none-any.whl
56549b9959cbcf2ce4501e6bf118a09fb6d720b887554fe26d96bd810802bd28  blackwood_witness-0.1.0.tar.gz
```

## Evidence boundaries

Earlier README, large-file/memory, reinstall-preservation and advisory checks
were earlier development observations, not checks rerun at this candidate.
Current artifact comparison established matching committed implementation.
No exhaustive privacy guarantee or independent audit is claimed.
