"""CLI acceptance checks for integrity failures and safe file handling."""

import os
from pathlib import Path

import pytest

from witness.cli import main
from witness.keys import (
    generate_private_key,
    serialize_private_key,
    serialize_public_key,
)
from witness.records import create_record, record_to_json


@pytest.fixture
def example(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[Path, Path, Path, Path]:
    key = generate_private_key()
    source = tmp_path / "sample.txt"
    source.write_bytes(b"hello witness\n")
    private = tmp_path / "private.pem"
    private.write_bytes(serialize_private_key(key, password=b"test-password"))
    public = tmp_path / "public.pem"
    public.write_bytes(serialize_public_key(key.public_key()))
    record = tmp_path / "record.json"
    record.write_text(record_to_json(create_record(source, key)), encoding="utf-8")
    monkeypatch.setattr("witness.cli.getpass.getpass", lambda prompt: "test-password")
    return source, private, public, record


def verify_arguments(source: Path, public: Path, record: Path) -> list[str]:
    return [
        "verify", str(source),
        "--public-key", str(public),
        "--record", str(record),
    ]


@pytest.mark.parametrize("change", ["one-byte", "append", "truncate", "replace"])
def test_changed_contents_fail_and_original_still_passes(
    example: tuple[Path, Path, Path, Path],
    change: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    source, _, public, record = example
    original = source.read_bytes()
    original_record = record.read_bytes()
    arguments = verify_arguments(source, public, record)
    assert main(arguments) == 0
    capsys.readouterr()

    changed = {
        "one-byte": b"H" + original[1:],
        "append": original + b"extra",
        "truncate": original[:-1],
        "replace": b"entirely different contents",
    }[change]
    source.write_bytes(changed)

    assert main(arguments) == 1
    output = capsys.readouterr()
    assert "Verification failed:" in output.err
    assert "Verified:" not in output.out
    assert record.read_bytes() == original_record

    source.write_bytes(original)
    assert main(arguments) == 0


@pytest.mark.parametrize("kind", ["symlink", "directory", "fifo"])
def test_unsupported_input_fails_without_publishing_a_record(
    example: tuple[Path, Path, Path, Path],
    tmp_path: Path,
    kind: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    source, private, public, record = example
    unsupported = tmp_path / "unsupported"
    if kind == "symlink":
        unsupported.symlink_to(source)
    elif kind == "directory":
        unsupported.mkdir()
    else:
        os.mkfifo(unsupported)

    output_record = tmp_path / "new-record.json"
    assert main([
        "sign", str(unsupported),
        "--private-key", str(private),
        "--record", str(output_record),
    ]) == 1
    assert not output_record.exists()
    assert main(verify_arguments(unsupported, public, record)) == 1

    output = capsys.readouterr()
    assert "regular file" in output.err
    assert "Traceback" not in output.err
    assert "Verified:" not in output.out


@pytest.mark.parametrize("command", ["keygen", "export-public-key", "sign"])
def test_cli_write_failure_does_not_publish_output(
    example: tuple[Path, Path, Path, Path],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    command: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    source, private, _, _ = example
    destination = tmp_path / "new-output"
    arguments = {
        "keygen": ["keygen", "--private-key", str(destination)],
        "export-public-key": [
            "export-public-key", "--private-key", str(private),
            "--public-key", str(destination),
        ],
        "sign": [
            "sign", str(source), "--private-key", str(private),
            "--record", str(destination),
        ],
    }[command]

    def fail_sync(descriptor: int) -> None:
        raise OSError("simulated output failure")

    monkeypatch.setattr("witness.file_io.os.fsync", fail_sync)

    assert main(arguments) == 1
    assert not destination.exists()
    assert not list(tmp_path.glob(".witness-*.tmp"))
    output = capsys.readouterr()
    assert "simulated output failure" in output.err
    assert "Traceback" not in output.err
    assert "saved to:" not in output.out
