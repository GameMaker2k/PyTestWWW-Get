"""pywwwget (Python 3 only)

A multi-protocol transfer module supporting HTTP(S), FTP(S), TFTP, SFTP, `file:`, `data:`,
plus custom `tcp:` / `udp:` streaming.

Public exports focus on high-level operations; some helper utilities are also exposed for convenience.
"""

from .core import (  # noqa: F401
    __version__,
    download_file_from_internet_file,
    download_file_from_internet_bytes,
    upload_file_to_internet_file,
    recv_to_fileobj,
    recv_to_path,
    send_from_fileobj,
    send_path,
    # Convenience helpers (still part of the underlying module behavior)
    data_url_encode,
    data_url_decode,
    _parse_net_url,
    _parse_kv_headers,
)
