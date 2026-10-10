# Large-file hashing validation

> Historical evidence below refers to the private development archive.
> Old commit hashes, PR numbers and scan counts do not describe this
> fresh repository. Fresh-history CI, scanning and rebuilt-artifact
> acceptance remain required before release.


Observed on 10 October 2026.

Environment: macOS 26.6.2, build 25G83; Python 3.13.16.
Hashing implementation checkpoint: 1f5e358.
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

On the documentation-closeout branch following checkpoint 917d17b,
a manual acceptance check exercised 64 MiB and 512 MiB logical files
containing zero bytes.

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
