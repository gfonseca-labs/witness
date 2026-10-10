"""Streaming hashes for regular files with change detection."""

import os
import stat
from hashlib import sha256
from pathlib import Path

CHUNK_SIZE = 1024 * 1024


def _state(info: os.stat_result) -> tuple[int, int, int, int, int]:
    return (
        info.st_dev,
        info.st_ino,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
    )


def sha256_file(path: Path) -> str:
    """Hash a regular file, rejecting observed changes during the read.

    The final path component must not be a symlink. Metadata comparisons
    detect ordinary concurrent changes; they do not provide a snapshot.
    """
    initial = path.lstat()
    if not stat.S_ISREG(initial.st_mode):
        raise ValueError(f"Expected a regular file, not a symlink or special file: {path}")

    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
    descriptor = os.open(path, flags)
    try:
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode):
            raise ValueError(f"Expected a regular file: {path}")
        if _state(initial) != _state(opened):
            raise ValueError(f"File changed before hashing: {path}")

        digest = sha256()
        total = 0
        while chunk := os.read(descriptor, CHUNK_SIZE):
            digest.update(chunk)
            total += len(chunk)

        finished = os.fstat(descriptor)
        current = path.lstat()
        if (
            not stat.S_ISREG(current.st_mode)
            or _state(opened) != _state(finished)
            or _state(opened) != _state(current)
            or total != opened.st_size
        ):
            raise ValueError(f"File changed during hashing: {path}")

        return digest.hexdigest()
    finally:
        os.close(descriptor)
