#!/usr/bin/env python3
"""Minimal CLI wrapper for pywwwget_py3_advanced.

Examples:
  - Download to file:
      python wwwget_cli.py get https://example.com/file.bin -o file.bin
  - Download to stdout:
      python wwwget_cli.py get https://example.com/file.bin > file.bin
  - Send a file/dir using a URL scheme supported by the module:
      python wwwget_cli.py put ./mydir tcp://0.0.0.0:9000/?print_url=1
  - Receive over Bluetooth RFCOMM (listener) and print a shareable URL:
      python wwwget_cli.py get "bt://00:00:00:00:00:00:3/out.bin?print_url=1" -o out.bin
    Then, from another device (sender), connect and upload:
      python wwwget_cli.py put ./in.bin "bt://AA:BB:CC:DD:EE:FF:3/out.bin"
"""

from __future__ import annotations

import argparse
import logging
import sys
from typing import Dict, List, Optional

import pywwwget as wwwget


def _parse_headers(raw_headers: List[str], user_agent: Optional[str]) -> Dict[str, str]:
    headers: Dict[str, str] = {}
    for h in raw_headers or []:
        if ":" not in h:
            raise SystemExit(f"Bad header {h!r}. Use 'Key: Value'.")
        k, v = h.split(":", 1)
        headers[k.strip()] = v.strip()
    if user_agent:
        headers.setdefault("User-Agent", user_agent)
    return headers


def _setup_logger(level: str) -> logging.Logger:
    lvl = getattr(logging, level.upper(), None)
    if not isinstance(lvl, int):
        raise SystemExit(f"Unknown log level: {level}")
    logging.basicConfig(level=lvl, format="%(levelname)s: %(message)s")
    return logging.getLogger("wwwget")


def cmd_get(args: argparse.Namespace) -> int:
    logger = _setup_logger(args.log_level)
    headers = _parse_headers(args.header, args.user_agent)

    if args.out:
        res = wwwget.recv_to_path(
            args.url,
            args.out,
            auto_extract=args.extract,
            extract_dir=args.extract_dir,
            keep_archive=(not args.delete_archive),
            headers=headers if headers else None,
            timeout=args.timeout,
            usehttp=args.backend,
            logger=logger,
        )
        if res is False:
            return 2
        return 0

    # stdout mode (default if no -o)
    fp = wwwget.download_file_from_internet_file(
        args.url,
        headers=headers if headers else None,
        timeout=args.timeout,
        usehttp=args.backend,
        logger=logger,
    )
    if not fp:
        return 2

    out = sys.stdout.buffer
    try:
        while True:
            chunk = fp.read(1024 * 64)
            if not chunk:
                break
            out.write(chunk)
        out.flush()
    finally:
        try:
            fp.close()
        except Exception:
            pass
    return 0


def cmd_put(args: argparse.Namespace) -> int:
    logger = _setup_logger(args.log_level)
    ok = wwwget.send_path(
        args.path,
        args.url,
        fmt=args.format,
        compression=args.compression,
        verbose=args.verbose,
        logger=logger,
    )
    return 0 if ok else 2


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="wwwget", description="CLI wrapper around pywwwget_py3_advanced.")
    p.add_argument("--log-level", default="WARNING", help="Python logging level (DEBUG, INFO, WARNING, ERROR).")

    sub = p.add_subparsers(dest="cmd", required=False)

    pg = sub.add_parser("get", help="Download (or run listen/recv mode if encoded in URL query)")
    pg.add_argument("url")
    pg.add_argument("-o", "--out", help="Output path. If omitted, writes to stdout.")
    pg.add_argument("--timeout", type=float, default=60.0, help="Network timeout seconds.")
    pg.add_argument("--backend", default=None, help="HTTP backend override (httpx/requests/urllib/pycurl if supported).")

    pg.add_argument("--header", action="append", default=[], help="Add HTTP header (repeatable): 'Key: Value'.")
    pg.add_argument("--user-agent", default=None, help="Shortcut for setting User-Agent header.")
    pg.add_argument("--extract", action="store_true", help="Auto-extract .zip/.tar.* archives after download.")

    pg.add_argument("--extract-dir", default=None, help="Directory to extract into (default: out directory).")

    # If extract is set, keep_archive controls whether archive stays on disk after extraction.
    pg.add_argument("--delete-archive", action="store_true", help="Delete downloaded archive after extraction.")

    pp = sub.add_parser("put", help="Send a file or directory (directory is archived first)")
    pp.add_argument("path", help="File or directory to send.")
    pp.add_argument("url", help="Destination URL (tcp://, udp://, ftp://, sftp://, file://, data:, etc.).")
    pp.add_argument("--format", default="tar", choices=["tar", "zip"], help="Archive format for directories.")
    pp.add_argument("--compression", default=None, choices=[None, "gz", "gzip"], help="Compression for tar archives.")
    pp.add_argument("--verbose", action="store_true", help="Enable verbose transfer logs where supported.")

    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    # Default to `get` if no subcommand provided
    if args.cmd in (None, "get"):
        if args.cmd is None:
            # mimic `get` positional if user called: wwwget URL -o OUT
            # argparse would have failed without subcommand; so we interpret first arg as URL.
            # (This path is only reachable if argv is provided programmatically.)
            raise SystemExit("Use: wwwget get <url> [-o out] ...")
        return cmd_get(args)

    if args.cmd == "put":
        return cmd_put(args)

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
