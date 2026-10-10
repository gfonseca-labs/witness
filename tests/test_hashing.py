from pathlib import Path

from witness.hashing import sha256_file


def test_sha256_file(tmp_path: Path) -> None:
    file = tmp_path / "example.txt"
    file.write_bytes(b"hello witness\n")

    digest = sha256_file(file)

    assert digest == "a38a1b2130fd6b757c19107d41f4bbefb14486f28dc59c0501328ed32db0d6be"