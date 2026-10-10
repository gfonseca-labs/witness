"""CLI acceptance checks for real filesystem permission failures."""

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

pytestmark = pytest.mark.skipif(
    os.geteuid() == 0, reason="Permission denial requires a non-root user."
)


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


@pytest.mark.parametrize("input_index", [0, 2, 3])
def test_verify_unreadable_input(
    example: tuple[Path, Path, Path, Path],
    input_index: int,
    capsys: pytest.CaptureFixture[str],
) -> None:
    source, _, public, record = example
    denied = example[input_index]
    original_mode = denied.stat().st_mode & 0o777
    denied.chmod(0o000)
    try:
        assert main([
            "verify", str(source),
            "--public-key", str(public),
            "--record", str(record),
        ]) == 1
    finally:
        denied.chmod(original_mode)

    output = capsys.readouterr()
    assert "Error:" in output.err
    assert "Traceback" not in output.err
    assert "Verified:" not in output.out


@pytest.mark.parametrize("input_index", [0, 1])
def test_sign_unreadable_input(
    example: tuple[Path, Path, Path, Path],
    tmp_path: Path,
    input_index: int,
    capsys: pytest.CaptureFixture[str],
) -> None:
    source, private, _, _ = example
    destination = tmp_path / "new-record.json"
    denied = example[input_index]
    original_mode = denied.stat().st_mode & 0o777
    denied.chmod(0o000)
    try:
        assert main([
            "sign", str(source),
            "--private-key", str(private),
            "--record", str(destination),
        ]) == 1
    finally:
        denied.chmod(original_mode)

    assert not destination.exists()
    output = capsys.readouterr()
    assert "Error:" in output.err
    assert "Traceback" not in output.err
    assert "saved to:" not in output.out


@pytest.mark.parametrize("command", ["keygen", "export-public-key", "sign"])
def test_unwritable_output_directory(
    example: tuple[Path, Path, Path, Path],
    tmp_path: Path,
    command: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    source, private, _, _ = example
    folder = tmp_path / "unwritable"
    folder.mkdir()
    destination = folder / "output"
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

    folder.chmod(0o500)
    try:
        assert main(arguments) == 1
    finally:
        folder.chmod(0o700)

    assert list(folder.iterdir()) == []
    output = capsys.readouterr()
    assert "Error:" in output.err
    assert "Traceback" not in output.err
    assert "saved to:" not in output.out
