from pathlib import Path

import pytest

from witness.cli import main
from witness.keys import (
    generate_private_key,
    load_public_key,
    public_key_fingerprint,
    serialize_private_key,
)


def test_export_public_key_round_trip(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    key = generate_private_key()
    private_path = tmp_path / "private.pem"
    pem = serialize_private_key(key, password=b"test-password")
    private_path.write_bytes(pem)
    public_path = tmp_path / "public.pem"
    monkeypatch.setattr("witness.cli.getpass.getpass", lambda prompt: "test-password")
    assert (
        main(
            [
                "export-public-key",
                "--private-key",
                str(private_path),
                "--public-key",
                str(public_path),
            ]
        )
        == 0
    )
    public_pem = public_path.read_bytes()
    assert b"BEGIN PUBLIC KEY" in public_pem
    assert b"PRIVATE KEY" not in public_pem
    public_key = load_public_key(public_pem)
    public_key.verify(key.sign(b"hello witness"), b"hello witness")
    assert private_path.read_bytes() == pem
    output = capsys.readouterr().out
    assert public_key_fingerprint(key.public_key()) in output
    assert "test-password" not in output


@pytest.mark.parametrize("password", ["wrong-password", ""])
def test_export_rejects_bad_password(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, password: str
) -> None:
    key = generate_private_key()
    private_path = tmp_path / "private.pem"
    private_path.write_bytes(serialize_private_key(key, password=b"test-password"))
    public_path = tmp_path / "public.pem"
    monkeypatch.setattr("witness.cli.getpass.getpass", lambda prompt: password)
    assert (
        main(
            [
                "export-public-key",
                "--private-key",
                str(private_path),
                "--public-key",
                str(public_path),
            ]
        )
        == 1
    )
    assert not public_path.exists()


def test_export_never_overwrites(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    public_path = tmp_path / "public.pem"
    public_path.write_bytes(b"existing file")

    def unexpected_prompt(prompt: str) -> str:
        pytest.fail("An existing output should be rejected before asking for a password.")

    monkeypatch.setattr("witness.cli.getpass.getpass", unexpected_prompt)
    assert (
        main(
            [
                "export-public-key",
                "--private-key",
                str(tmp_path / "private.pem"),
                "--public-key",
                str(public_path),
            ]
        )
        == 1
    )
    assert public_path.read_bytes() == b"existing file"


def test_export_missing_private_key(tmp_path: Path) -> None:
    public_path = tmp_path / "public.pem"
    assert (
        main(
            [
                "export-public-key",
                "--private-key",
                str(tmp_path / "missing.pem"),
                "--public-key",
                str(public_path),
            ]
        )
        == 1
    )
    assert not public_path.exists()


def test_export_handles_cancellation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    private_path = tmp_path / "private.pem"
    key = generate_private_key()
    private_path.write_bytes(serialize_private_key(key, password=b"test-password"))
    public_path = tmp_path / "public.pem"

    def cancel(prompt: str) -> str:
        raise KeyboardInterrupt

    monkeypatch.setattr("witness.cli.getpass.getpass", cancel)
    assert (
        main(
            [
                "export-public-key",
                "--private-key",
                str(private_path),
                "--public-key",
                str(public_path),
            ]
        )
        == 1
    )
    assert not public_path.exists()
