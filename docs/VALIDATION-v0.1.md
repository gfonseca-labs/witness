# Witness v0.1 validation evidence

> Historical evidence below refers to the private development archive.
> Old commit hashes, PR numbers and scan counts do not describe this
> fresh repository. Fresh-history CI, scanning and rebuilt-artifact
> acceptance remain required before release.


Observed on 10 October 2026 through Blackwood's Terminal results.

Source checkpoint: ac08274, following the packaging fix.
The tested artifacts preceded this evidence document.
Repeat validation for final release artifacts if they change.

## Environment

macOS with Python 3.13.16.
Wheel and source installations used fresh virtual environments outside
the development checkout. Installed Witness version: 0.1.0.

## Confirmed results

- Wheel and source archive built successfully.
- Wheel modules matched the checkout.
- Wheel included the MIT license and license metadata.
- Source archive included documentation, tests and reference fixtures.
- Fresh wheel installation passed pip check and displayed CLI help.
- Key generation, public-key export, signing and verification succeeded.
- Original verification returned 0.
- A separate copy with exactly one changed byte returned 1.
- The unchanged original still returned 0.
- Uninstall/reinstall preserved all five demonstration files unchanged.
- Verification after reinstall returned 0.
- Fresh source installation passed pip check.
- All 72 tests passed against the extracted source archive.
- Ruff passed against the extracted source archive.
- Permanent reference verification returned 0.

## Observed dependency versions

The fresh runtime installation resolved cryptography 50.0.2,
cffi 2.1.1 and pycparser 3.11.

The source-check environment additionally used pytest 9.1.1
and Ruff 0.17.0.

These are observed versions, not a dependency lock or vulnerability review.

## Remaining release gates

Final candidate CI, dependency vulnerability review, repository-history
review, naming review, public release and public-install reproduction.

No independent security audit or separate-user usability trial is established.

## Public-name validation — 10 October 2026

Renamed source checkpoint: e62152d3bfd7d1cbb90e553e4ef2275017deeffc

The public package and command are blackwood-witness; the internal module and record format remain unchanged.

- Renamed wheel and source archive built successfully.
- Fresh renamed-wheel installation passed pip check, help and existing reference-record verification (exit 0).
- Following the manifest update, the renamed source archive included the runtime audit input.
- Fresh renamed-source installation passed pip check, all 72 tests, Ruff and reference verification (exit 0).
- Resolved runtime versions remained cryptography 50.0.2, cffi 2.1.1 and pycparser 3.11.

The earlier manual four-command and reinstall checks used the original package name. The renamed manual workflow and final published-artifact checks remain to be performed.

## Renamed installed manual workflow — 10 October 2026

Using the separately installed blackwood-witness wheel outside the checkout:

- Key generation, public-key export and signing succeeded.
- Fingerprints matched across all operations.
- Original-file verification returned 0.
- A separate copy with exactly one changed byte returned 1.
- The unchanged original recheck returned 0.
- The sample digest matched the permanent reference sample.

This completes the renamed manual workflow previously marked pending.
Final published-artifact reproduction remains pending.

## Pull-request CI checkpoint

PR: Private development archive PR #1; public link omitted.
Commit: 333fcebfb97c2c6a7bd998b2bd2f3cc5af23c01b

On 10 October 2026, GitHub showed successful macOS Python 3.11 and
3.13 jobs for this commit. This records that checkpoint; subsequent
commits require their own passing checks.

## Acceptance completion — 10 October 2026

Source checkpoint: 9ab27b6.
Environment: macOS 26.6.2, build 25G83; Python 3.13.16.

- Empty-file and Unicode-path signing/verification passed.
- Eight real permission-denial checks passed without skips.
- Invalid UTF-8 and deeply nested record inputs returned handled CLI errors.
- A simulated parser recursion error was translated to ValueError.
- All 85 tests and Ruff passed locally.
- Large-file measurements passed; see LARGE-FILE-VALIDATION-v0.1.md.
- Acceptance wheel metadata, MIT license and module contents passed inspection.
- Acceptance source archive included the new tests and memory-check procedure.
- Named-package uninstall/reinstall preserved all five demo files unchanged.
- Installed metadata reported blackwood-witness 0.1.0.
- Imports resolved inside the separate wheel environment.
- After reinstall, original verification returned 0; changed-copy verification returned 1.
- Fresh acceptance-source installation passed pip check.
- All 85 archived tests passed without skips; Ruff passed.
- Archived reference verification returned 0.

These results supersede earlier pending statements for these acceptance cases.
They do not establish final candidate CI or public-release reproduction.

### Acceptance artifact SHA-256 values

- blackwood_witness-0.1.0-py3-none-any.whl: 28319d667c5c47e1b264941daf3d0cf860fe51003de935b55181a769d499b115
- blackwood_witness-0.1.0.tar.gz: e2f247494121e45cd906ca4aa92b24cc5854a3a221210ec8351df14fdd26ffc6

## Verbatim README check — 10 October 2026

Source: separate local clone at
557f0d25c46fcd196e2cd1b111eef7c2a20c0e05.

The README installation commands were executed as written:
python3 -m venv .venv; activate; python -m pip install .;
blackwood-witness --help.

The working example was executed as written using disposable files.
Key generation, export, signing and original verification succeeded.
The exact one-byte changed copy failed with exit code 1.
The original then verified successfully again.
Fingerprints matched within each demonstration run.

This establishes the documented local-checkout installation and example.
It does not establish installation from a public release.

## Documentation-closeout checkpoint — 10 October 2026

At commit 75ef73e on release/documentation-closeout:

- All 85 tests passed locally on macOS with Python 3.13.16.
- Ruff passed.
- git diff --check reported no whitespace errors.
- The five demonstration screenshots were reviewed and showed the
  expected original / changed copy / original verification results:
  exit codes 0 / 1 / 0.
- Demonstration behavior and trust limitations are recorded in
  docs/DEMO-v0.1.md.
- Screenshot selection supersedes the earlier video medium requirement.

Internal media placement, the updated Word documentation package,
final closeout CI and final published-artifact reproduction remain
pending. This checkpoint does not establish public-release completion.

## Technical-release preparation — 10 October 2026

Checkpoint: 79167c959cf2d9cb717fb691110c7cbccafe8bd8
Branch: release/technical-v0.1-closeout

- All 85 tests passed locally on macOS with Python 3.13.16.
- Ruff passed.
- pip check reported no broken requirements.
- blackwood-witness help displayed all four commands.
- Owner-approved release scope and residual limitations are recorded in
  docs/RELEASE-APPROVAL-v0.1.md.
- Deferred technical issues existed in the private development archive;
  fresh-repository issues must be recreated.

Final merged-commit CI, final artifact validation and public-release
reproduction remain pending.

## Fresh sanitized repository — 10 October 2026

Checkpoint: 4406b7f113ff2f95d6269cdd60b49480c0faa1e2

- A fresh local environment installed this checkout.
- All 85 tests passed on macOS with Python 3.13.16, without skips.
- Ruff passed; pip check reported no broken requirements.
- Both macOS Python 3.11 and 3.13 CI jobs passed:
  https://github.com/gfonseca-labs/witness/actions/runs/38084814507
- The known-personal-identifier audit passed for all 46 staged source files.
  Approved account links were excluded from that audit.
- Git history excludes the old machine-identified development commits.
- The owner accepts personal-name attribution and account identifiers;
  machine identifiers and personal local paths remain prohibited.
- Fresh follow-up issues are #1, #2 and #3.

Gitleaks reported no leaks across 2 scanned commits at this checkpoint.
Git history contains 3 commits including the merge. The scan exit-code
line was not captured, so this record does not assert its numeric value.

Final closeout CI, final history/privacy checks, rebuilt distributions
and public-release reproduction remain pending.
Earlier distributions must not be published.
