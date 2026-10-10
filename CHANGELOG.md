# Changelog

> Historical evidence below refers to the private development archive.
> Old commit hashes, PR numbers and scan counts do not describe this
> fresh repository. Fresh-history CI, scanning and rebuilt-artifact
> acceptance remain required before release.


## Unreleased — planned 0.1.0

This section describes the release candidate, not a published release.
The release date and reviewed commit will be recorded at publication.

### Core functionality

- Stream file contents through SHA-256.
- Generate password-encrypted Ed25519 private keys.
- Export SubjectPublicKeyInfo PEM public keys and fingerprints.
- Create detached version 1 signed JSON records.
- Verify record signatures and matching file contents.
- Reject malformed, duplicate, unexpected and unsupported record fields.
- Require explicit key and record paths.
- Return documented CLI success, failure and argument-error exit codes.

### Release preparation

- Publish complete output files without overwriting existing destinations.
- Restrict CLI-created private-key permissions to 0600.
- Reject symlinks in the final content-path component and non-regular files.
- Detect ordinary file changes or replacement during hashing.
- Add CLI acceptance checks for content changes and output failures.
- Add a permanent, explicitly test-only version 1 compatibility fixture.
- Document the format, design, threat model and reporting policy.
- Add the MIT license.

### Validation and limitations

- 85 tests passed locally and from the acceptance source archive on macOS
  with Python 3.13.16, including empty/Unicode workflows, permission
  failures and unusual malformed-record cases.
- Large-file allocation checks and named-package reinstall preservation passed.
- Ruff passed at the same checkpoint.
- PR #1 passed CI on macOS with Python 3.11 and 3.13 at 333fceb.
- Merged PR #2 checkpoint 557f0d2 also passed both CI versions.
- Documentation-closeout checkpoint 75ef73e passed 85 tests and Ruff
  locally; its history scan found no leaks across 31 commits.
- Full 64 MiB and 512 MiB signed-record workflows passed, including
  saved-record reload, one-byte-change rejection and restoration.
- The reviewed screenshot demonstration showed verification results
  0/1/0 and supersedes the planned video medium.
- Merged PR #3 checkpoint f98c729 passed both macOS CI versions.
- Technical-release preparation checkpoint 79167c9 passed 85 tests,
  Ruff and pip check. Gitleaks scanned 35 commits with no recognized leaks.
- Owner approved the technical GitHub release scope and documented
  residual limitations; deferred issues must be recreated in this repository.
- Article and social publication are deferred, not completed.
- Final technical-closeout changes require passing CI before merging.
- Fresh wheel and source installations passed, including the renamed package.
- The installed renamed workflow passed original/changed/original checks (0/1/0).
- Public-release reproduction remains pending.
- Public package and CLI name: blackwood-witness; public title: Witness by Blackwood.
- Linux and Windows support is not established.
- Concurrent-change detection is not an atomic snapshot.
- Forced termination can leave temporary files.
- Output publication requires hard-link support and does not guarantee
  persistence after power loss.
- No independent security audit is established.

See docs/THREAT_MODEL.md for the full scope and limitations.
