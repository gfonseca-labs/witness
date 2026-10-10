"""Acceptance tests for supported files and concurrent changes."""

import os
from hashlib import sha256
from pathlib import Path

import pytest

from witness.hashing import CHUNK_SIZE, sha256_file


@pytest.mark.parametrize(
    "data",
    [b"", b"hello witness\n", b"x" * (CHUNK_SIZE * 2 + 17)],
)
def test_hashes_supported_contents(tmp_path: Path, data: bytes) -> None:
    path = tmp_path / "résumé — sample.txt"
    path.write_bytes(data)
    assert sha256_file(path) == sha256(data).hexdigest()


def test_rejects_directory(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="regular file"):
        sha256_file(tmp_path)


def test_rejects_symlink(tmp_path: Path) -> None:
    target = tmp_path / "target.txt"
    target.write_bytes(b"sample")
    link = tmp_path / "link.txt"
    link.symlink_to(target)

    with pytest.raises(ValueError, match="regular file"):
        sha256_file(link)

    assert target.read_bytes() == b"sample"


def test_rejects_fifo_without_waiting_for_a_writer(tmp_path: Path) -> None:
    path = tmp_path / "pipe"
    os.mkfifo(path)

    with pytest.raises(ValueError, match="regular file"):
        sha256_file(path)


def test_detects_content_change_during_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "sample.txt"
    path.write_bytes(b"original")
    real_read = os.read
    changed = False

    def changing_read(descriptor: int, size: int) -> bytes:
        nonlocal changed
        chunk = real_read(descriptor, size)
        if chunk and not changed:
            changed = True
            path.write_bytes(b"changed and longer")
        return chunk

    monkeypatch.setattr("witness.hashing.os.read", changing_read)

    with pytest.raises(ValueError, match="changed during hashing"):
        sha256_file(path)


def test_detects_path_replacement_during_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "sample.txt"
    path.write_bytes(b"original")
    replacement = tmp_path / "replacement.txt"
    replacement.write_bytes(b"original")
    real_read = os.read
    replaced = False

    def replacing_read(descriptor: int, size: int) -> bytes:
        nonlocal replaced
        chunk = real_read(descriptor, size)
        if chunk and not replaced:
            replaced = True
            replacement.replace(path)
        return chunk

    monkeypatch.setattr("witness.hashing.os.read", replacing_read)

    with pytest.raises(ValueError, match="changed during hashing"):
        sha256_file(path)
