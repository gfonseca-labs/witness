# v0.1 release dispositions

## Accepted route

D-030 accepts a technical GitHub-only v0.1 release with the disclosed limitations. Article and social publication are deferred and incomplete. Fresh issues #1, #2 and #3 preserve deferred technical work. D-032 permits personal-name attribution and account identifiers while excluding personal machine identifiers and local paths. Final release approval remains pending.

## Accepted limitations

- Hard-link support required; power-loss durability not guaranteed.
- Concurrent-change detection is not an atomic snapshot.
- Parent-directory symlink protection incomplete; no general input resource quota.
- Linux/Windows support, independent audit, separate-user trial and demand not established.

Acceptance does not eliminate risks.

## Follow-ups

- [#1 — durability/portability](https://github.com/gfonseca-labs/witness/issues/1)
- [#2 — path/input hardening and limits](https://github.com/gfonseca-labs/witness/issues/2)
- [#3 — Linux/Windows validation](https://github.com/gfonseca-labs/witness/issues/3)

Issue creation does not complete the deferred work.

## Observed candidate

Latest sanitized checkpoint: 63e0bd422ef4ac11a44e053df9f369111216558c. Fresh PR #4 is merged. macOS Python 3.11.9 and 3.13.15 CI passed 85 tests and Ruff. Run: https://github.com/gfonseca-labs/witness/actions/runs/38085266592

The 63e0bd4 wheel and ownership-normalized source archive matched committed files. Separate fresh installations passed pip check and help. The installed wheel returned original / one-byte changed copy / original results 0 / 1 / 0. The normalized source passed all 85 tests without skips, Ruff and reference verification. Observed runtime: cryptography 50.0.2, cffi 2.1.1 and pycparser 3.11; local Python 3.13.16, pytest 9.1.1 and Ruff 0.17.0. These observations are not a lock.

## Outstanding gates

1. Review/merge these documents with passing CI; record the new commit.
2. Repeat history/privacy checks; rebuild, normalize and inspect distributions.
3. Record new hashes/resolved versions; repeat clean-install acceptance.
4. Verify public visibility and private vulnerability reporting.
5. Review tag/release/assets; verify downloaded checksums.
6. Reproduce from the actual public release and check links.
7. Obtain final owner sign-off and update technical SHIPPED status.
