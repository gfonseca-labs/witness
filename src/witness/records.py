"""Version 1 signed file records."""

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

from witness.hashing import sha256_file
from witness.keys import public_key_fingerprint


@dataclass(frozen=True)
class RecordPayload:
    """The information protected by the signature."""

    version: int
    file_sha256: str
    signer: str

    def __post_init__(self) -> None:
        if type(self.version) is not int or self.version != 1:
            raise ValueError("Unsupported record version.")
        if not isinstance(self.file_sha256, str) or not re.fullmatch(
            r"[0-9a-f]{64}", self.file_sha256
        ):
            raise ValueError("Expected a lowercase SHA-256 digest.")
        if not isinstance(self.signer, str) or not re.fullmatch(
            r"sha256:[0-9a-f]{64}", self.signer
        ):
            raise ValueError("Expected a SHA-256 public-key fingerprint.")


def signing_bytes(payload: RecordPayload) -> bytes:
    """Encode the payload using the fixed Witness v1 signing rules."""
    encoded = json.dumps(
        asdict(payload), sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")
    return b"witness-record-v1\n" + encoded


@dataclass(frozen=True)
class SignedRecord:
    payload: RecordPayload
    signature: str

    def __post_init__(self) -> None:
        if not isinstance(self.signature, str) or not re.fullmatch(
            r"[0-9a-f]{128}", self.signature
        ):
            raise ValueError("Expected a lowercase Ed25519 signature in hex.")


def create_record(path: Path, private_key: Ed25519PrivateKey) -> SignedRecord:
    """Hash a file and sign its record without writing keys to disk."""
    payload = RecordPayload(
        version=1,
        file_sha256=sha256_file(path),
        signer=public_key_fingerprint(private_key.public_key()),
    )
    signature = private_key.sign(signing_bytes(payload)).hex()
    return SignedRecord(payload=payload, signature=signature)


def verify_record(record: SignedRecord, public_key: Ed25519PublicKey) -> bool:
    """Verify against a public key supplied by the caller."""
    if record.payload.signer != public_key_fingerprint(public_key):
        return False
    try:
        public_key.verify(bytes.fromhex(record.signature), signing_bytes(record.payload))
    except InvalidSignature:
        return False
    return True


def verify_file(path: Path, record: SignedRecord, public_key: Ed25519PublicKey) -> bool:
    """Check both the record signature and the current file contents."""
    return verify_record(record, public_key) and sha256_file(path) == record.payload.file_sha256


def record_to_json(record: SignedRecord) -> str:
    """Produce human-readable JSON for storage."""
    return json.dumps(asdict(record), sort_keys=True, indent=2) + "\n"


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON field: {key}")
        result[key] = value
    return result


def record_from_json(data: str) -> SignedRecord:
    """Read a record, rejecting ambiguous or unsupported formats."""
    try:
        document = json.loads(data, object_pairs_hook=_unique_object)
    except RecursionError as error:
        raise ValueError("Record JSON is nested too deeply.") from error
    if not isinstance(document, dict) or set(document) != {"payload", "signature"}:
        raise ValueError("Expected exactly payload and signature fields.")
    payload = document["payload"]
    if not isinstance(payload, dict) or set(payload) != {"version", "file_sha256", "signer"}:
        raise ValueError("Unexpected payload fields.")
    return SignedRecord(RecordPayload(**payload), document["signature"])
