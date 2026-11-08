# Large-file hashing validation

> Historical development measurements, not a benchmark of the published
> release. See [release validation](VALIDATION-v0.1.md) for the shipped
> artifacts and their checksums.


Observed on 10 October 2026.

Environment: macOS; Python 3.13.16.
Procedure: tools/check_hashing_memory.py.

Each file was hashed in a separate Python process. Files contained zeros
and were created by truncation, using sparse storage where supported.
Expected digests were calculated independently with hashlib.

| Logical file size | Peak traced Python allocation | Peak process memory |
| --- | --- | --- |
| 64 MiB | 2.00 MiB | 24.08 MiB |
| 512 MiB | 2.00 MiB | 21.89 MiB |

Both digests matched. The allocation checks passed.
Process peaks include interpreter overhead and vary between processes.

This provides evidence of bounded allocation for these measured cases.
It is not a throughput benchmark, proof for every file size or a test
of physical disk performance.

## Full large-file record workflow — 10 October 2026

A manual development check exercised 64 MiB and 512 MiB logical files
containing zero bytes. These are historical observations, not a reproduction
of the published release.

For each size:

- Created an Ed25519 signing key in memory.
- Created a signed record.
- Saved the record as JSON and loaded it again.
- Verified the original file successfully.
- Changed exactly one byte without changing the file size.
- Confirmed verification failed.
- Confirmed the saved record remained byte-for-byte unchanged.
- Restored the original byte and verified successfully again.

Both sizes passed. Disposable files were removed automatically.

This complements the earlier bounded-memory hashing measurements.
It exercises the Python record API, rather than the installed CLI.
The files may be sparse; this is not a physical-disk or throughput
benchmark, nor a guarantee for every file size or concurrent writer.
