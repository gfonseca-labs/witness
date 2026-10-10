"""Publish complete output files without replacing existing paths."""

import os
import tempfile
from pathlib import Path


def write_new_file(path: Path, data: bytes, *, mode: int = 0o644) -> None:
    """Write and publish a new file on a filesystem supporting hard links.

    The temporary file lives beside the destination. Linking it publishes
    the complete file without replacing an existing destination.
    """
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".witness-", suffix=".tmp", dir=path.parent
    )
    temporary_path = Path(temporary_name)

    try:
        with os.fdopen(descriptor, "wb") as file:
            os.fchmod(file.fileno(), mode)
            file.write(data)
            file.flush()
            os.fsync(file.fileno())

        os.link(temporary_path, path)
    finally:
        temporary_path.unlink()
