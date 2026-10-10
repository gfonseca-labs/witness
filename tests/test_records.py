import json
from dataclasses import replace
from pathlib import Path

import pytest

from witness.keys import generate_private_key
from witness.records import (
    RecordPayload,
    create_record,
    record_from_json,
    record_to_json,
    signing_bytes,
    verify_file,
    verify_record,
)


def test_signing_bytes_are_fixed() -> None:
    payload = RecordPayload(1, "a" * 64, "sha256:" + "b" * 64)
    expected = (
        'witness-record-v1\n{"file_sha256":"' + "a" * 64
        + '","signer":"sha256:' + "b" * 64 + '","version":1}'
    ).encode("ascii")
    assert signing_bytes(payload) == expected


def test_record_round_trip_and_changed_file(tmp_path: Path) -> None:
    path = tmp_path / "example.txt"
    path.write_bytes(b"hello witness\n")
    key = generate_private_key()
    record = create_record(path, key)
    loaded = record_from_json(record_to_json(record))
    assert loaded == record
    assert verify_file(path, loaded, key.public_key())
    # JSON whitespace and field order do not change the signed information.
    compact = json.dumps(json.loads(record_to_json(record)), sort_keys=False)
    assert verify_record(record_from_json(compact), key.public_key())
    path.write_bytes(b"changed content\n")
    assert verify_record(loaded, key.public_key())
    assert not verify_file(path, loaded, key.public_key())


def test_tampering_and_wrong_key(tmp_path: Path) -> None:
    path = tmp_path / "example.txt"
    path.write_bytes(b"hello witness\n")
    key = generate_private_key()
    record = create_record(path, key)
    changed_payload = replace(record.payload, file_sha256="0" * 64)
    assert not verify_record(replace(record, payload=changed_payload), key.public_key())
    changed_signature = ("0" if record.signature[0] != "0" else "1") + record.signature[1:]
    assert not verify_record(replace(record, signature=changed_signature), key.public_key())
    other_key = generate_private_key()
    assert not verify_record(record, other_key.public_key())
    from witness.keys import public_key_fingerprint

    forged_signer = replace(record.payload, signer=public_key_fingerprint(other_key.public_key()))
    assert not verify_record(replace(record, payload=forged_signer), other_key.public_key())


@pytest.mark.parametrize(
    "data",
    [
        "not json",
        "[]",
        '{"payload": {}, "signature": "00"}',
        '{"payload": {}, "payload": {}, "signature": "00"}',
    ],
)
def test_reject_malformed_json(data: str) -> None:
    with pytest.raises(ValueError):
        record_from_json(data)


@pytest.mark.parametrize("version", [2, True, "1"])
def test_reject_unsupported_version(version: object) -> None:
    with pytest.raises(ValueError):
        RecordPayload(version, "a" * 64, "sha256:" + "b" * 64)
