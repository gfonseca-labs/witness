"""End-to-end acceptance for empty files and Unicode paths."""

import subprocess
import sys
from pathlib import Path

import pytest

from witness.cli import main
from witness.keys import generate_private_key, serialize_private_key


@pytest.mark.parametrize(
    ("filename", "contents"),
    [
        ("empty.txt", b""),
        ("résumé — 文件.txt", "Hello, 世界\n".encode()),
    ],
)
def test_sign_and_verify_supported_files(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    filename: str,
    contents: bytes,
) -> None:
    private = tmp_path / "private.pem"
    public = tmp_path / "public.pem"
    source = tmp_path / filename
    record = tmp_path / (filename + ".witness.json")

    private.write_bytes(
        serialize_private_key(generate_private_key(), password=b"test-password")
    )
    source.write_bytes(contents)
    monkeypatch.setattr("witness.cli.getpass.getpass", lambda prompt: "test-password")

    assert main([
        "export-public-key",
        "--private-key", str(private),
        "--public-key", str(public),
    ]) == 0
    assert main([
        "sign", str(source),
        "--private-key", str(private),
        "--record", str(record),
    ]) == 0
    assert source.read_bytes() == contents

    command = [
        sys.executable, "-m", "witness.cli",
        "verify", str(source),
        "--public-key", str(public),
        "--record", str(record),
    ]
    original_record = record.read_bytes()
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    assert result.returncode == 0
    assert "Verified:" in result.stdout
    assert not result.stderr

    source.write_bytes(contents + b"x")
    changed = subprocess.run(command, capture_output=True, text=True, check=False)
    assert changed.returncode == 1
    assert "Verification failed:" in changed.stderr
    assert "Verified:" not in changed.stdout
    assert record.read_bytes() == original_record
