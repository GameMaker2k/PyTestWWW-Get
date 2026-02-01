# pywwwget (Python 3 only)

A multi-protocol transfer module (HTTP(S), FTP(S), TFTP, SFTP, `file:`, `data:`, plus custom `tcp:` / `udp:` streaming),
knowing how to **download**, **serve**, and **receive uploads** with options configured via URL query parameters.

## Install (editable)
```bash
pip install -e .
```

## Install (normal)
```bash
pip install .
```

## CLI
After installation, the `wwwget` command is available:

```bash
wwwget get "https://example.com/file.bin" -o file.bin
wwwget put ./mydir "tcp://0.0.0.0:9000/?print_url=1"
```

## Optional extras
This package uses optional backends when installed:
- `httpx` (preferred HTTP client)
- `requests` (fallback HTTP client)
- `pycurl` (optional)
- `paramiko` / `pysftp` (SFTP)

## Tests
```bash
python -m unittest -q
```


## Development

Install with developer tooling:
```bash
pip install -e ".[dev]"
```

Run lint + type checks:
```bash
ruff check .
mypy src/pywwwget
```

Run tests:
```bash
pytest -q
python -m unittest -q
```

## GitHub Actions CI

This repo includes a workflow at `.github/workflows/ci.yml` that runs:
- ruff (sanity checks)
- mypy (typed surface)
- pytest + unittest

on Python 3.9–3.12.
