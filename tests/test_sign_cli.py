from pathlib import Path

import pytest

from witness.cli import main
from witness.keys import generate_private_key, serialize_private_key
from witness.records import record_from_json, verify_file


def test_sign_creates_verifiable_record(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    key = generate_private_key()
    private_path = tmp_path / "private.pem"
    private_pem = serialize_private_key(key, password=b"test-password")
    private_path.write_bytes(private_pem)
    file_path = tmp_path / "example.txt"
    original = b"hello witness\n"
    file_path.write_bytes(original)
    record_path = tmp_path / "example.witness.json"
    monkeypatch.setattr("witness.cli.getpass.getpass", lambda prompt: "test-password")
    assert (
        main(
            [
                "sign",
                str(file_path),
                "--private-key",
                str(private_path),
                "--record",
                str(record_path),
            ]
        )
        == 0
    )
    record = record_from_json(record_path.read_text(encoding="utf-8"))
    assert verify_file(file_path, record, key.public_key())
    assert file_path.read_bytes() == original
    assert private_path.read_bytes() == private_pem
    output = capsys.readouterr().out
    assert record.payload.signer in output
    assert "test-password" not in output
    file_path.write_bytes(b"changed\n")
    assert not verify_file(file_path, record, key.public_key())


@pytest.mark.parametrize("password", ["wrong-password", ""])
def test_sign_rejects_bad_password(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, password: str
) -> None:
    private_path = tmp_path / "private.pem"
    private_path.write_bytes(
        serialize_private_key(generate_private_key(), password=b"test-password")
    )
    file_path = tmp_path / "example.txt"
    file_path.write_bytes(b"hello witness\n")
    record_path = tmp_path / "record.json"
    monkeypatch.setattr("witness.cli.getpass.getpass", lambda prompt: password)
    assert (
        main(
            [
                "sign",
                str(file_path),
                "--private-key",
                str(private_path),
                "--record",
                str(record_path),
            ]
        )
        == 1
    )
    assert not record_path.exists()


def test_sign_never_overwrites(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    record_path = tmp_path / "record.json"
    record_path.write_bytes(b"existing record")

    def unexpected_prompt(prompt: str) -> str:
        pytest.fail("An existing output should be rejected before asking for a password.")

    monkeypatch.setattr("witness.cli.getpass.getpass", unexpected_prompt)
    assert (
        main(
            [
                "sign",
                str(tmp_path / "example.txt"),
                "--private-key",
                str(tmp_path / "private.pem"),
                "--record",
                str(record_path),
            ]
        )
        == 1
    )
    assert record_path.read_bytes() == b"existing record"


def test_sign_missing_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    private_path = tmp_path / "private.pem"
    private_path.write_bytes(
        serialize_private_key(generate_private_key(), password=b"test-password")
    )
    record_path = tmp_path / "record.json"
    monkeypatch.setattr("witness.cli.getpass.getpass", lambda prompt: "test-password")
    assert (
        main(
            [
                "sign",
                str(tmp_path / "missing.txt"),
                "--private-key",
                str(private_path),
                "--record",
                str(record_path),
            ]
        )
        == 1
    )
    assert not record_path.exists()


def test_sign_handles_cancellation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    private_path = tmp_path / "private.pem"
    private_path.write_bytes(
        serialize_private_key(generate_private_key(), password=b"test-password")
    )
    record_path = tmp_path / "record.json"

    def cancel(prompt: str) -> str:
        raise KeyboardInterrupt

    monkeypatch.setattr("witness.cli.getpass.getpass", cancel)
    assert (
        main(
            [
                "sign",
                str(tmp_path / "example.txt"),
                "--private-key",
                str(private_path),
                "--record",
                str(record_path),
            ]
        )
        == 1
    )
    assert not record_path.exists()
