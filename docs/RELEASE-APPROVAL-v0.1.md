# Witness by Blackwood v0.1.0 — owner release decision

Owner: Blackwood
Decision date: 10 October 2026
Reviewed baseline: private development archive.
Fresh sanitized release commit: pending.

## D-030 — Technical GitHub release route — Accepted

Witness by Blackwood v0.1.0 will ship as a technical GitHub release.
Article and social publication are deferred post-release work.
They remain incomplete and must not be described as published.

This supersedes their status as prerequisites for the technical release.
Historical planning requirements remain preserved.

No new features will be added before v0.1.0.

## Residual limitations — Accepted

The owner explicitly accepts the documented v0.1 limitations:

- Output publication requires hard-link support.
- Power-loss durability is not guaranteed.
- Concurrent-change detection does not provide an atomic filesystem snapshot.
- Parent-directory symlink protection is incomplete.
- Input reads have no general resource quota.
- Linux and Windows support is not established.
- No independent security audit is established.
- No separate-user usability trial or demonstrated demand is established.

These are disclosed limitations, not claims that the risks have been
eliminated. Deferred technical work will be recorded in GitHub issues.

## Final release approval — Pending

Scope and limitations approval does not establish release completion.

Final approval remains conditional on final artifact checks, passing CI,
final secret scanning, public security-reporting verification and
successful reproduction from the public release.

Record the final commit, tag, artifact hashes, CI URL, release URL and
reproduction results before marking the technical release SHIPPED.
Article and social publication must retain their separate deferred status.

## Deferred technical follow-up work

- Improve output publication durability and hard-link portability.
- Evaluate additional path/input hardening and resource limits.
- Validate Linux and Windows support.

Earlier issues belong to the private development archive.
These issues must be recreated in the fresh repository and their actual
links recorded before technical release completion.

## D-031 — Public repository privacy — Accepted

Public project attribution uses Blackwood.
Personal names, personal email addresses and local user paths must not
appear in repository contents or Git author/committer metadata.

The original development repository remains private. The sanitized
repository starts with fresh history. Historical test and scan results
are private-development evidence, not validation of this fresh history.

Rebuild and revalidate distributions from the sanitized release commit.
Do not publish the earlier distributions.
