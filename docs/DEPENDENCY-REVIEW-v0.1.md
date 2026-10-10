# v0.1 runtime dependency review

Observed on 10 October 2026.

Tool: pip-audit 2.10.1, installed in a separate audit environment.
Input: runtime-audit-requirements.txt, recording the resolved third-party
packages from the fresh wheel installation.

Command options: --no-deps --disable-pip

Result: "No known vulnerabilities found"; exit code 0.

The tool recommended hashing pinned dependencies. No hashes were supplied.
The requirements list is an audit input, not an installation lock.

This review covers known advisories for the exact versions listed.
It does not audit Witness code, development/build tools, dependency
source code, unknown vulnerabilities or all versions allowed by metadata.
Repeat the review if final installation resolves different versions.
