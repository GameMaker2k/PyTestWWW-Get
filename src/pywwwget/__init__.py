"""PyWWWGet (Python 3 only)

High-level convenience exports:
  - download_file_from_internet_file / bytes
  - upload_file_to_internet_file
  - recv_to_path / recv_to_fileobj
  - send_path / send_from_fileobj
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
)

__all__ = [
    "__version__",
    "download_file_from_internet_file",
    "download_file_from_internet_bytes",
    "upload_file_to_internet_file",
    "recv_to_fileobj",
    "recv_to_path",
    "send_from_fileobj",
    "send_path",
]
