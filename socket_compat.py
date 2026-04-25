"""Cross-platform socket compatibility layer for Browser Harness."""
import os
import socket
import tempfile
from pathlib import Path

IS_WINDOWS = os.name == 'nt'


def get_socket_path(name="default"):
    """Get socket path or (host, port) tuple based on platform."""
    if IS_WINDOWS:
        import hashlib
        base_port = 19222
        # Use stable hash instead of Python's randomized hash()
        port_offset = int(hashlib.md5(name.encode()).hexdigest(), 16) % 100
        return ("127.0.0.1", base_port + port_offset)
    else:
        return f"/tmp/bu-{name}.sock"


def get_temp_dir():
    """Get temp directory based on platform."""
    if IS_WINDOWS:
        temp = Path(tempfile.gettempdir()) / "browser-harness"
        temp.mkdir(parents=True, exist_ok=True)
        return temp
    else:
        return Path("/tmp")


def create_socket():
    """Create socket based on platform."""
    if IS_WINDOWS:
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        return socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)


def connect_socket(sock, address):
    """Connect socket to address."""
    sock.connect(address)


def bind_socket(sock, address):
    """Bind socket to address."""
    if IS_WINDOWS:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)


def cleanup_socket(address):
    """Clean up socket file (Unix only)."""
    if not IS_WINDOWS and isinstance(address, str):
        try:
            Path(address).unlink(missing_ok=True)
        except Exception:
            pass
