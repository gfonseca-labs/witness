# Changelog

## 0.1.0 — unpublished release candidate

- SHA-256/Ed25519 detached content records and encrypted private keys.
- Explicit keygen, export-public-key, sign and verify commands.
- Strict version 1 format and permanent public TEST-ONLY reference fixture.
- Non-overwriting complete-file publication and ordinary-change detection.
- Empty/Unicode, permission and malformed-record acceptance.
- Qualified blackwood-witness naming and sanitized fresh history.
- Reviewed screenshots supersede video. Technical GitHub scope accepted; article/social deferred.

Latest sanitized checkpoint: 63e0bd422ef4ac11a44e053df9f369111216558c. Fresh PR #4 is merged. macOS Python 3.11.9 and 3.13.15 CI passed 85 tests and Ruff. Run: https://github.com/gfonseca-labs/witness/actions/runs/38085266592

The 63e0bd4 wheel and ownership-normalized source archive matched committed files. Separate fresh installations passed pip check and help. The installed wheel returned original / one-byte changed copy / original results 0 / 1 / 0. The normalized source passed all 85 tests without skips, Ruff and reference verification. Observed runtime: cryptography 50.0.2, cffi 2.1.1 and pycparser 3.11; local Python 3.13.16, pytest 9.1.1 and Ruff 0.17.0. These observations are not a lock.

Final validation of this documentation revision and public release remain pending.
