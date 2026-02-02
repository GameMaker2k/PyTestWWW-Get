# pywwwget (Python 3 only)

A multi-protocol transfer module (HTTP(S), FTP(S), TFTP, SFTP, Bluetooth RFCOMM (`bt:`), `file:`, `data:`, plus custom `tcp:` / `udp:` streaming),
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


## Bluetooth RFCOMM (`bt://`)

This build adds **optional Bluetooth RFCOMM** support using either:
- Python's native Bluetooth socket support (Linux builds with `AF_BLUETOOTH` / `BTPROTO_RFCOMM`), or
- **PyBluez** (`bluetooth` module) if installed.

### Receive (listener) + print URL
```bash
wwwget get "bt://00:00:00:00:00:00:3/out.bin?print_url=1" -o out.bin
```

### Send (connect to listener)
```bash
wwwget put ./in.bin "bt://AA:BB:CC:DD:EE:FF:3/out.bin"
```

Notes:
- `00:00:00:00:00:00` is **BDADDR_ANY** (bind all). If you use it, replace the printed address with the
  receiver device’s actual Bluetooth MAC address when sharing the URL.
- Default channel is `1` if omitted.


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
