# Witness by Blackwood — owner release decision

Owner: Blackwood
Decision date: 10 October 2026

## D-030 — Accepted route and limitations

D-030 accepts a technical GitHub-only v0.1 release with the disclosed limitations. Article and social publication are deferred and incomplete. Fresh issues #1, #2 and #3 preserve deferred technical work. D-032 permits personal-name attribution and account identifiers while excluding personal machine identifiers and local paths. Final release approval remains pending.

- Hard-link support required; power-loss durability not guaranteed.
- Concurrent-change detection is not an atomic snapshot.
- Parent-directory symlink protection incomplete; no general input resource quota.
- Linux/Windows support, independent audit, separate-user trial and demand not established.

No new features before release.

## D-031/D-032 — Accepted privacy scope

Original machine-identified development history remains private. Fresh sanitized
history is used. Personal-name attribution and GitHub account identifiers are
accepted. Machine identifiers, local usernames, hostnames and personal local
paths must be excluded from published files and commit metadata. D-032
supersedes the earlier personal-name prohibition.

## Follow-ups

- [#1 — durability/portability](https://github.com/gfonseca-labs/witness/issues/1)
- [#2 — path/input hardening and limits](https://github.com/gfonseca-labs/witness/issues/2)
- [#3 — Linux/Windows validation](https://github.com/gfonseca-labs/witness/issues/3)

## Final approval — Pending

Scope approval is not release completion. Record final commit, CI URL, tag,
asset hashes, release URL, public reproduction and owner sign-off before
technical SHIPPED. Article/social remain deferred and incomplete.
