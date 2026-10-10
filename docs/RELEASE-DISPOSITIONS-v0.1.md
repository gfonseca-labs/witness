# v0.1 release dispositions

> Historical evidence below refers to the private development archive.
> Old commit hashes, PR numbers and scan counts do not describe this
> fresh repository. Fresh-history CI, scanning and rebuilt-artifact
> acceptance remain required before release.


Prepared on 10 October 2026.
Status: owner accepted the technical release scope and documented residual
limitations on 10 October 2026. Final release sign-off remains pending.
See RELEASE-APPROVAL-v0.1.md for the accepted decision.

## Scope

Public name: Witness by Blackwood.
Package and command: blackwood-witness.
Distribution plan: GitHub release; no PyPI publication in this release.

Supported/tested platform: macOS, with Python 3.11 and 3.13 in CI.
Linux and Windows support is not established.

The content-only version 1 record and its signing bytes remain unchanged.

## Reliability limitations to disclose

- Complete outputs are published without replacing existing paths.
  This does not guarantee survival after power loss.
- Forced termination can leave a temporary file.
- Output publication requires filesystem hard-link support.
- Metadata checks detect ordinary file changes during hashing.
  They do not provide a snapshot or defend against filesystem control.
- Content-input checks reject final-component symlinks and special files.
  Parent-directory symlinks are not explicitly rejected.
- Content hashing protections do not constitute equivalent restrictions
  on every key or record input path. Use trusted regular key/record files.
- Permission errors, invalid UTF-8 and parser recursion errors have
  acceptance coverage. Error handling is not exhaustive.
- Key and record reads have no explicit input-size/resource quota.

These limits remain visible in documentation and are accepted for v0.1.
Deferred technical work covers publication durability/portability,
path/input hardening and resource limits, and Linux/Windows validation.
Earlier issues remain in the private archive. Fresh follow-up issues:

- https://github.com/gfonseca-labs/witness/issues/1
- https://github.com/gfonseca-labs/witness/issues/2
- https://github.com/gfonseca-labs/witness/issues/3

Acceptance does not eliminate these limitations.

## Review and usability evidence

Automated tests, dependency advisory checks, history secret scanning
and development review were performed.

No independent security audit or separate-user usability trial has
been completed. No user-demand or production-grade claim is established.

Installation requires Python and Terminal knowledge. This release will
disclose the absence of external usability validation.

The reference fixture's deterministic key is intentionally public and
TEST ONLY. It is unsuitable for real signing.

## Reproduction limits

Validation records identify observed dependency versions and artifacts.
Dependency lower bounds are not an exact installation lock.
Public reproduction must record the versions actually resolved.

## Completed closeout checks — 10 October 2026

- Acceptance-completion changes merged through PR #2.
- Merged checkpoint 557f0d2 passed macOS Python 3.11/3.13 CI.
- Verbatim README installation and workflow passed; recorded in 917d17b.
- Full 64 MiB and 512 MiB signing, saved-record reload, verification,
  one-byte-change rejection and restoration checks passed;
  recorded in 2f3ad17.
- Earlier acceptance evidence includes 85 passing tests, permission
  failures, malformed-record handling, bounded-memory hashing and
  preservation of demonstration files across named-package reinstall.

Documentation-closeout merged through PR #3. Merged checkpoint f98c729
passed macOS Python 3.11/3.13 CI. Technical-release preparation at
79167c9 passed 85 tests, Ruff and pip check; Gitleaks scanned 35 commits
with no recognized leaks, exit 0.

These results apply to their recorded checkpoints. Final technical-closeout
changes and final release artifacts require their own validation.

## Demonstration decision — 10 October 2026

The owner selected an ordered screenshot walkthrough instead of video.
This supersedes the video medium requirement in the planning documents;
the required demonstration behavior remains unchanged.

The walkthrough must show:

- Public command help and the four available commands.
- Key generation and public-key export with matching fingerprints.
- Signing and successful original-file verification.
- Creation of a separate exact one-byte changed copy after the original
  verification, followed by failed verification with exit code 1.
- Successful original-file recheck with exit code 0.
- Clear explanation of the trusted-public-key requirement and limits
  of what the signature proves.

Screenshots must use disposable demonstration keys and must not display
private-key contents or passwords. All five screenshots were captured and
reviewed; the sequence showed verification results 0/1/0.
See DEMO-v0.1.md for behavior and trust limitations.
The updated internal Word package includes the screenshots and explicitly
records the video-medium supersession. It requires a final release update.

## Accepted technical release route

D-030 supersedes article and social publication as prerequisites for the
technical GitHub v0.1.0 release. Those activities remain deferred and
incomplete. No new features will be added before release.

## Outstanding technical release gates

- Final claim/document consistency and final internal release records.
- Passing CI for the final technical-closeout changes.
- Final sanitized-release history scan.
- Final wheel/source inspection, checksums and clean-install acceptance.
- Public visibility and private vulnerability-reporting verification.
- Reviewed tag and GitHub Release with verified assets.
- Reproduction from the actual public release and public-link checks.
- Final owner release sign-off.
- Project index update and technical SHIPPED status after these gates pass.

Article and social publication retain separate deferred status after the
technical release; SHIPPED must not imply those activities were completed.
