# History and privacy review

At 63e0bd4, Gitleaks 8.30.1 reported no leaks across 4 scanned commits, approximately 105.98 KB, exit 0. A separate audit checked all 6 reachable commits and 50 unique file versions, including commit metadata; no checked machine identifiers were found. Supplied final CI job logs showed hosted-runner paths and no checked personal machine identifiers. These are bounded reviews, not exhaustive guarantees or independent audits.

Git reports 6 reachable commits including 2 merges; the scan reports 4.
These counts cover different scopes. Author/committer metadata, messages,
filenames and unique file contents were checked for known machine identifiers.
Accepted author names and account identifiers are permitted. Archive metadata
was checked separately, including tar ownership. Ignored/untracked files,
unreachable objects and unrecognized secrets/identifiers are outside these
bounded reviews. Original development history and prior scans remain private.
Subsequent commits and rebuilt assets require new reviews before publication.
