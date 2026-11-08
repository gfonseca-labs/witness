# Reproduce the Witness demonstration

Install Witness using the [README](../README.md#install) or the
[release artifact instructions](VALIDATION.md), then run the
[README example](../README.md#try-it) in an interactive shell.

| Step | Expected observation |
| --- | --- |
| Generate an encrypted private key | Password confirmation and public-key fingerprint |
| Export its public key | The same fingerprint |
| Sign `example.txt` | Detached JSON record and file digest |
| Verify the original | `Verified:` and exit 0 |
| Verify the copy with `h` changed to `H` | Verification failure and exit 1 |
| Verify the original again | `Verified:` and exit 0 |

The example uses disposable keys and keeps the original file and record
unchanged. Passwords and private-key contents should not be displayed.
The repository contains the commands and expected observations needed to
repeat this demonstration.

Matching fingerprints identify the same key; they do not independently
authenticate it. Verification checks the signature and signed content digest.
It does not establish identity, authorship, creation time, truthfulness or file
safety. This demonstration is not an independent security audit.
