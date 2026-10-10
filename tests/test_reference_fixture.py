"""Compatibility checks against the permanent Witness v1 reference."""

import json
from pathlib import Path

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from witness.cli import main
from witness.keys import load_public_key, serialize_public_key
from witness.records import (
    create_record,
    record_from_json,
    signing_bytes,
    verify_file,
)

REFERENCE = Path(__file__).parent / "fixtures" / "reference"


def test_permanent_reference_verifies() -> None:
    record = record_from_json(
        (REFERENCE / "record.json").read_text(encoding="utf-8")
    )
    public = load_public_key((REFERENCE / "public.pem").read_bytes())

    assert signing_bytes(record.payload) == (
        REFERENCE / "signing-bytes.bin"
    ).read_bytes()
    assert verify_file(REFERENCE / "sample.txt", record, public)
    assert main([
        "verify", str(REFERENCE / "sample.txt"),
        "--public-key", str(REFERENCE / "public.pem"),
        "--record", str(REFERENCE / "record.json"),
    ]) == 0


def test_current_signer_reproduces_reference() -> None:
    # Public, deterministic TEST-ONLY seed. Never use for real signing.
    key = Ed25519PrivateKey.from_private_bytes(bytes(range(32)))
    expected = record_from_json(
        (REFERENCE / "record.json").read_text(encoding="utf-8")
    )

    assert serialize_public_key(key.public_key()) == (
        REFERENCE / "public.pem"
    ).read_bytes()
    assert create_record(REFERENCE / "sample.txt", key) == expected


@pytest.mark.parametrize(
    "case",
    [
        "extra-envelope-field",
        "extra-payload-field",
        "duplicate-payload-field",
        "uppercase-digest",
        "uppercase-signature",
        "invalid-signer",
    ],
)
def test_rejects_nonconforming_reference_records(case: str) -> None:
    document = json.loads(
        (REFERENCE / "record.json").read_text(encoding="utf-8")
    )
    if case == "extra-envelope-field":
        document["extra"] = "unexpected"
    elif case == "extra-payload-field":
        document["payload"]["filename"] = "sample.txt"
    elif case == "uppercase-digest":
        document["payload"]["file_sha256"] = (
            document["payload"]["file_sha256"].upper()
        )
    elif case == "uppercase-signature":
        document["signature"] = document["signature"].upper()
    elif case == "invalid-signer":
        document["payload"]["signer"] = "sha256:not-a-fingerprint"

    encoded = json.dumps(document)
    if case == "duplicate-payload-field":
        encoded = encoded.replace('"version": 1', '"version": 1, "version": 1')

    with pytest.raises(ValueError):
        record_from_json(encoded)
