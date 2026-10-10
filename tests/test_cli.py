import stat
from pathlib import Path

import pytest

from witness.cli import main
from witness.keys import load_private_key, public_key_fingerprint


def test_keygen_creates_encrypted_private_key(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    answers = iter(["test-password", "test-password"])
    monkeypatch.setattr("witness.cli.getpass.getpass", lambda prompt: next(answers))
    path = tmp_path / "private.pem"
    assert main(["keygen", "--private-key", str(path)]) == 0
    pem = path.read_bytes()
    assert b"BEGIN ENCRYPTED PRIVATE KEY" in pem
    key = load_private_key(pem, password=b"test-password")
    output = capsys.readouterr().out
    assert public_key_fingerprint(key.public_key()) in output
    assert "test-password" not in output
    assert stat.S_IMODE(path.stat().st_mode) & 0o077 == 0
    with pytest.raises(ValueError):
        load_private_key(pem, password=b"wrong-password")


def test_keygen_never_overwrites(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = tmp_path / "private.pem"
    path.write_bytes(b"existing file")

    def unexpected_prompt(prompt: str) -> str:
        pytest.fail("An existing file should be rejected before asking for a password.")

    monkeypatch.setattr("witness.cli.getpass.getpass", unexpected_prompt)
    assert main(["keygen", "--private-key", str(path)]) == 1
    assert path.read_bytes() == b"existing file"


@pytest.mark.parametrize("answers", [[""], ["one", "two"]])
def test_keygen_rejects_bad_passwords(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, answers: list[str]
) -> None:
    responses = iter(answers)
    monkeypatch.setattr("witness.cli.getpass.getpass", lambda prompt: next(responses))
    path = tmp_path / "private.pem"
    assert main(["keygen", "--private-key", str(path)]) == 1
    assert not path.exists()


def test_keygen_handles_cancellation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def cancel(prompt: str) -> str:
        raise KeyboardInterrupt

    monkeypatch.setattr("witness.cli.getpass.getpass", cancel)
    path = tmp_path / "private.pem"
    assert main(["keygen", "--private-key", str(path)]) == 1
    assert not path.exists()


def test_help_does_not_create_a_key(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as result:
        main(["--help"])
    assert result.value.code == 0
    assert "keygen" in capsys.readouterr().out
