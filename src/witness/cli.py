"""The Witness command-line interface."""

import argparse
import getpass
import sys
from pathlib import Path

from witness.file_io import write_new_file
from witness.keys import (
    generate_private_key,
    load_private_key,
    load_public_key,
    public_key_fingerprint,
    serialize_private_key,
    serialize_public_key,
)
from witness.records import create_record, record_from_json, record_to_json, verify_file


def _keygen(path: Path) -> None:
    if path.exists() or path.is_symlink():
        raise FileExistsError(f"Refusing to overwrite: {path}")
    password = getpass.getpass("New key password: ")
    if not password:
        raise ValueError("The password must not be empty.")
    confirmation = getpass.getpass("Confirm key password: ")
    if password != confirmation:
        raise ValueError("The passwords do not match.")

    private_key = generate_private_key()
    pem = serialize_private_key(private_key, password=password.encode("utf-8"))
    write_new_file(path, pem, mode=0o600)

    print(f"Encrypted private key saved to: {path}")
    print(f"Public-key fingerprint: {public_key_fingerprint(private_key.public_key())}")


def _export_public_key(private_path: Path, public_path: Path) -> None:
    if public_path.exists() or public_path.is_symlink():
        raise FileExistsError(f"Refusing to overwrite: {public_path}")
    private_pem = private_path.read_bytes()
    password = getpass.getpass("Private-key password: ")
    if not password:
        raise ValueError("The password must not be empty.")
    private_key = load_private_key(private_pem, password=password.encode("utf-8"))
    public_key = private_key.public_key()
    public_pem = serialize_public_key(public_key)
    write_new_file(public_path, public_pem, mode=0o644)
    print(f"Public key saved to: {public_path}")
    print(f"Public-key fingerprint: {public_key_fingerprint(public_key)}")


def _sign(file_path: Path, private_path: Path, record_path: Path) -> None:
    if record_path.exists() or record_path.is_symlink():
        raise FileExistsError(f"Refusing to overwrite: {record_path}")
    private_pem = private_path.read_bytes()
    password = getpass.getpass("Private-key password: ")
    if not password:
        raise ValueError("The password must not be empty.")
    private_key = load_private_key(private_pem, password=password.encode("utf-8"))
    record = create_record(file_path, private_key)
    encoded = record_to_json(record).encode("utf-8")
    write_new_file(record_path, encoded, mode=0o644)
    print(f"Signed record saved to: {record_path}")
    print(f"File SHA-256: {record.payload.file_sha256}")
    print(f"Public-key fingerprint: {record.payload.signer}")


def _verify(file_path: Path, public_path: Path, record_path: Path) -> int:
    public_key = load_public_key(public_path.read_bytes())
    record = record_from_json(record_path.read_text(encoding="utf-8"))
    if not verify_file(file_path, record, public_key):
        print(
            "Verification failed: the record signature or file contents do not match.",
            file=sys.stderr,
        )
        return 1
    print(f"Verified: {file_path}")
    print(f"Public-key fingerprint: {record.payload.signer}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="blackwood-witness",
        description="Witness by Blackwood file-integrity tools.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    keygen = commands.add_parser("keygen", help="Create a password-protected Ed25519 key.")
    keygen.add_argument(
        "--private-key", type=Path, required=True, help="New private-key PEM file to create."
    )
    export = commands.add_parser(
        "export-public-key", help="Export the public key from an encrypted private key."
    )
    export.add_argument(
        "--private-key", type=Path, required=True, help="Encrypted private-key PEM."
    )
    export.add_argument(
        "--public-key", type=Path, required=True, help="New public-key PEM to create."
    )
    sign = commands.add_parser("sign", help="Create a signed record for a file.")
    sign.add_argument("file", type=Path, help="File whose contents to hash and sign.")
    sign.add_argument("--private-key", type=Path, required=True, help="Encrypted private-key PEM.")
    sign.add_argument(
        "--record", type=Path, required=True, help="New signed JSON record to create."
    )
    verify = commands.add_parser("verify", help="Check a signed record and the file contents.")
    verify.add_argument("file", type=Path, help="File whose current contents to check.")
    verify.add_argument("--public-key", type=Path, required=True, help="Trusted public-key PEM.")
    verify.add_argument("--record", type=Path, required=True, help="Signed JSON record to check.")
    args = parser.parse_args(argv)

    try:
        if args.command == "keygen":
            _keygen(args.private_key.expanduser())
        elif args.command == "export-public-key":
            _export_public_key(args.private_key.expanduser(), args.public_key.expanduser())
        elif args.command == "sign":
            _sign(args.file.expanduser(), args.private_key.expanduser(), args.record.expanduser())
        elif args.command == "verify":
            return _verify(
                args.file.expanduser(), args.public_key.expanduser(), args.record.expanduser()
            )
    except (OSError, ValueError, TypeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    except (EOFError, KeyboardInterrupt):
        print("\nCommand cancelled.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
