# Installing and checking Witness 0.1.1

Use the [0.1.1 release](https://github.com/gfonseca-labs/witness/releases/tag/v0.1.1)
for the wheel, source archive and SHA256SUMS.txt. Download all three files into
one disposable directory and check their bytes before installation:

```sh
shasum -a 256 -c SHA256SUMS.txt
python3 -m venv .venv
. .venv/bin/activate
python -m pip install ./blackwood_witness-0.1.1-py3-none-any.whl
python -m pip check
blackwood-witness --help
```

The source archive is an alternative:
`python -m pip install ./blackwood_witness-0.1.1.tar.gz`.
Dependencies are resolved during installation rather than locked. A checksum
comparison detects changed bytes; it does not independently authenticate the
publisher.

Follow the [README demonstration](../README.md#try-it). The expected sequence
is original **0**, one-byte changed copy **1**, original **0**. Use disposable
keys and authenticate real verification keys through a trusted channel.

Version 0.1.1 changes documentation and release checks, not the version 1
signed record or cryptographic behavior. The [threat model](THREAT_MODEL.md)
still applies. macOS is the tested platform; Linux and Windows support and
an independent security audit are not established.

## Development and packaging

From a source checkout with the development dependencies installed:

```sh
python -m pytest
python -m ruff check .
python tools/check_publication.py
python tools/build_release.py dist
python tools/check_publication.py dist/*.whl dist/*.tar.gz
```

The builder requires a new output directory. It clears owner/group names,
numeric ownership and timestamps in the source archive, and omits the gzip
filename and timestamp. The wheel keeps its standard ZIP structure. Inspect
the final artifacts, not just the source checkout.

Public CI uses hosted runners. Their account paths and image information are
infrastructure metadata; developer-machine paths and document links are
rejected by the publication check. This bounded check supplements secret
scanning and review; it is not an exhaustive privacy guarantee.

The [v0.1.0 observations](VALIDATION-v0.1.md) remain historical evidence for
that release and its unchanged artifacts.
