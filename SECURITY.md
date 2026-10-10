# Security policy

## Release status

Witness v0.1.0 is being prepared for release. No public release is
established yet. Private vulnerability reporting must be enabled and
verified before the public release is announced.

After release, security fixes will target the latest published version.
There is no guaranteed response time or long-term support commitment.

## Reporting a vulnerability

When enabled, use GitHub's private reporting feature:

https://github.com/gfonseca-labs/witness/security/advisories

Select "Report a vulnerability". Include:

- The affected version or full commit ID.
- Your operating system and Python version.
- A minimal reproduction using disposable files and test-only keys.
- Expected behavior, observed behavior and potential impact.

Do not include real private keys, passwords or confidential documents.
Do not disclose vulnerability details in public issues or pull requests.

If private reporting is unavailable, a public issue may request a private
contact method without describing the vulnerability or including sensitive
material. The GitHub noreply commit address is not a reporting mailbox.

## Security scope

Witness checks signed file integrity relative to a supplied public key.
The user must authenticate that key independently.

It does not prove named identity, original authorship, truthfulness,
creation time, malware safety or uncompromised keys. It provides no
revocation or trusted timestamp service.

See docs/THREAT_MODEL.md for assumptions and filesystem limitations.
Automated tests are not an independent security audit.
