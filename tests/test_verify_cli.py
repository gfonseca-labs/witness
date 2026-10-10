import json
import subprocess
import sys
from pathlib import Path

import pytest

from witness.cli import main
from witness.keys import generate_private_key, serialize_public_key
from witness.records import create_record, record_to_json


@pytest.fixture
def signed_example(tmp_path: Path) -> tuple[Path, Path, Path]:
    file_path = tmp_path / "example.txt"
    file_path.write_bytes(b"hello witness\n")
    key = generate_private_key()
    public_path = tmp_path / "public.pem"
    public_path.write_bytes(serialize_public_key(key.public_key()))
    record_path = tmp_path / "record.json"
    record_path.write_text(record_to_json(create_record(file_path, key)), encoding="utf-8")
    return file_path, public_path, record_path


def _arguments(example: tuple[Path, Path, Path]) -> list[str]:
    file_path, public_path, record_path = example
    return [
        "verify",
        str(file_path),
        "--public-key",
        str(public_path),
        "--record",
        str(record_path),
    ]


def test_verify_success_and_changed_file(
    signed_example: tuple[Path, Path, Path],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def unexpected_prompt(prompt: str) -> str:
        pytest.fail("Verification must not ask for a private-key password.")

    monkeypatch.setattr("witness.cli.getpass.getpass", unexpected_prompt)
    assert main(_arguments(signed_example)) == 0
    assert "Verified:" in capsys.readouterr().out
    file_path, _, record_path = signed_example
    original_record = record_path.read_bytes()
    file_path.write_bytes(b"changed content\n")
    assert main(_arguments(signed_example)) == 1
    output = capsys.readouterr()
    assert "Verification failed:" in output.err
    assert "Verified:" not in output.out
    assert record_path.read_bytes() == original_record


def test_verify_wrong_key(signed_example: tuple[Path, Path, Path]) -> None:
    _, public_path, _ = signed_example
    public_path.write_bytes(serialize_public_key(generate_private_key().public_key()))
    assert main(_arguments(signed_example)) == 1


def test_verify_altered_signature(signed_example: tuple[Path, Path, Path]) -> None:
    _, _, record_path = signed_example
    document = json.loads(record_path.read_text(encoding="utf-8"))
    signature = document["signature"]
    document["signature"] = ("0" if signature[0] != "0" else "1") + signature[1:]
    record_path.write_text(json.dumps(document), encoding="utf-8")
    assert main(_arguments(signed_example)) == 1


@pytest.mark.parametrize("data", ["not json", "[]", '{"payload": {}, "signature": "00"}'])
def test_verify_malformed_record(signed_example: tuple[Path, Path, Path], data: str) -> None:
    _, _, record_path = signed_example
    record_path.write_text(data, encoding="utf-8")
    assert main(_arguments(signed_example)) == 1


@pytest.mark.parametrize("missing_index", [0, 1, 2])
def test_verify_missing_input(signed_example: tuple[Path, Path, Path], missing_index: int) -> None:
    signed_example[missing_index].unlink()
    assert main(_arguments(signed_example)) == 1


def test_verify_invalid_public_key(signed_example: tuple[Path, Path, Path]) -> None:
    _, public_path, _ = signed_example
    public_path.write_bytes(b"not a PEM key")
    assert main(_arguments(signed_example)) == 1


def test_verify_terminal_exit_codes(signed_example: tuple[Path, Path, Path]) -> None:
    command = [sys.executable, "-m", "witness.cli", *_arguments(signed_example)]
    good = subprocess.run(command, capture_output=True, text=True, check=False)
    assert good.returncode == 0
    assert "Verified:" in good.stdout
    signed_example[0].write_bytes(b"changed content\n")
    bad = subprocess.run(command, capture_output=True, text=True, check=False)
    assert bad.returncode == 1
    assert "Verification failed:" in bad.stderr
