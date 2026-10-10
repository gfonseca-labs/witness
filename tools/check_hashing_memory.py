"""Measure hashing memory for two large files on macOS."""

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

MIB = 1024 * 1024
CHILD = """
import json
import resource
import sys
import tracemalloc
from pathlib import Path
from witness.hashing import sha256_file

tracemalloc.start()
digest = sha256_file(Path(sys.argv[1]))
_, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
print(json.dumps({
    "digest": digest,
    "python_peak_bytes": peak,
    "process_peak_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
}))
"""


def expected_digest(size: int) -> str:
    digest = hashlib.sha256()
    chunk = b"\0" * MIB
    for _ in range(size // MIB):
        digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    if sys.platform != "darwin":
        raise SystemExit("This measurement interprets process memory on macOS only.")

    results = []
    with tempfile.TemporaryDirectory(prefix="witness-memory-") as directory:
        for size_mib in (64, 512):
            path = Path(directory) / f"{size_mib}MiB.bin"
            with path.open("wb") as file:
                file.truncate(size_mib * MIB)

            result = subprocess.run(
                [sys.executable, "-c", CHILD, str(path)],
                capture_output=True,
                text=True,
                check=True,
            )
            measured = json.loads(result.stdout)
            assert measured["digest"] == expected_digest(size_mib * MIB)
            measured["file_size_mib"] = size_mib
            results.append(measured)
            print(
                f"{size_mib} MiB: digest correct; "
                f"Python peak {measured['python_peak_bytes'] / MIB:.2f} MiB; "
                f"process peak {measured['process_peak_bytes'] / MIB:.2f} MiB"
            )

    small, large = results
    assert large["python_peak_bytes"] < 8 * MIB, "Unexpected Python allocation peak."
    assert (
        large["python_peak_bytes"] <= small["python_peak_bytes"] + 2 * MIB
    ), "Python allocations grew unexpectedly with file size."

    print("PASS: measured Python allocation remained bounded across these file sizes.")
    print("Process peaks include interpreter overhead and are reported separately.")


if __name__ == "__main__":
    main()
