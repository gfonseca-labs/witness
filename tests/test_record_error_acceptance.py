"""Process-level rejection of unusual invalid record inputs."""

import subprocess
import sys
from pathlib import Path

import pytest

from witness.keys import generate_private_key, serialize_public_key


@pytest.mark.parametrize("kind", ["invalid-utf8", "excessive-nesting"])
def test_invalid_record_returns_handled_error(tmp_path: Path, kind: str) -> None:
    source = tmp_path / "sample.txt"
    source.write_bytes(b"hello witness\n")
    public = tmp_path / "public.pem"
    public.write_bytes(serialize_public_key(generate_private_key().public_key()))
    record = tmp_path / "record.json"

    if kind == "invalid-utf8":
        data = b"\xff\xfe"
    else:
        depth = sys.getrecursionlimit() * 2
        data = ("[" * depth + "0" + "]" * depth).encode()
    record.write_bytes(data)

    result = subprocess.run(
        [
            sys.executable, "-m", "witness.cli",
            "verify", str(source),
            "--public-key", str(public),
            "--record", str(record),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "Error:" in result.stderr
    assert "Traceback" not in result.stderr
    assert "Verified:" not in result.stdout
    assert record.read_bytes() == data

def test_parser_recursion_error_is_handled(monkeypatch: pytest.MonkeyPatch) -> None:
    from witness.records import record_from_json

    def exceed_recursion(data: str, **kwargs: object) -> object:
        raise RecursionError("simulated JSON parser recursion limit")

    monkeypatch.setattr("witness.records.json.loads", exceed_recursion)

    with pytest.raises(ValueError, match="nested too deeply"):
        record_from_json("{}")
