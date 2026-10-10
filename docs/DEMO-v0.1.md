# Witness by Blackwood v0.1.0 screenshot demonstration

Captured and reviewed on 10 October 2026.

The owner selected screenshots instead of video. This supersedes the
demonstration medium requirement; the required behavior is preserved.

## Screenshot sequence

1. 01-command-overview.png — public command and four operations.
2. 02-key-generation-and-export.png — encrypted private-key creation,
   public-key export and matching fingerprints.
3. 03-sign-and-verify.png — signing and original verification, exit 0.
4. 04-one-byte-change-rejected.png — separate changed copy created after
   original verification; comparison shows one differing byte;
   verification fails, exit 1.
5. 05-original-recheck.png — unchanged original verifies again, exit 0.

Screenshots use disposable demonstration keys. No passwords or
private-key contents are displayed.

## What this demonstrates

With an independently trusted public key, successful verification
checks the record's signature and that the supplied file's SHA-256
matches the signed digest.

The changed copy replaces lowercase h with uppercase H in the first
byte. The original file remains unchanged. The observed verification
sequence is 0 / 1 / 0.

## What this does not establish

A matching fingerprint identifies a key; seeing it repeatedly does
not independently establish trust in that key.

Verification does not establish a person's identity, authorship,
ownership, creation time, truthfulness or safety of the file.
The record contains no trusted timestamp.

This demonstration is not an independent security audit or a
reproduction from the final published release assets.

## Media location

The five images belong in the internal 01 — Witness folder under
03 — Demo & Media. Their final placement and inclusion in the
documentation package must be checked before project closeout.
