"""Acceptance tests for safe, non-overwriting output publication."""

import stat
from pathlib import Path

import pytest

from witness.file_io import write_new_file


def test_publishes_complete_private_file(tmp_path: Path) -> None:
    destination = tmp_path / "private.pem"
    data = b"test-only contents\n" * 1000

    write_new_file(destination, data, mode=0o600)

    assert destination.read_bytes() == data
    assert stat.S_IMODE(destination.stat().st_mode) == 0o600
    assert list(tmp_path.iterdir()) == [destination]


def test_existing_destination_is_preserved(tmp_path: Path) -> None:
    destination = tmp_path / "record.json"
    destination.write_bytes(b"original")

    with pytest.raises(FileExistsError):
        write_new_file(destination, b"replacement")

    assert destination.read_bytes() == b"original"
    assert list(tmp_path.iterdir()) == [destination]


def test_dangling_symlink_is_preserved(tmp_path: Path) -> None:
    destination = tmp_path / "record.json"
    target = tmp_path / "missing.json"
    destination.symlink_to(target)

    with pytest.raises(FileExistsError):
        write_new_file(destination, b"replacement")

    assert destination.is_symlink()
    assert not target.exists()
    assert list(tmp_path.iterdir()) == [destination]


@pytest.mark.parametrize("failure", [OSError, KeyboardInterrupt])
def test_failed_write_is_not_published(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failure: type[BaseException]
) -> None:
    destination = tmp_path / "private.pem"

    def fail_sync(descriptor: int) -> None:
        raise failure("simulated interruption before publication")

    monkeypatch.setattr("witness.file_io.os.fsync", fail_sync)

    with pytest.raises(failure):
        write_new_file(destination, b"test-only contents", mode=0o600)

    assert not destination.exists()
    assert list(tmp_path.iterdir()) == []
