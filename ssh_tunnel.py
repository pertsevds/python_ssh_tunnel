"""Ports and sockets forwarding tunnel over SSH with systems SSH client."""
import logging
import os
import subprocess
import tempfile
from contextlib import contextmanager
from typing import Generator, Optional

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class SSHTunnelConnectionError(Exception):
    """Connection error exception."""


@contextmanager
def create_ssh_tunnel(
    hostname: str, local_socket: str, remote_socket: str, timeout: int = 10
) -> Generator[str, None, None]:
    """Create SSH tunnel."""
    ssh_socket_filename = gen_temp_socket_filename(f"{hostname}.")
    ssh_tunnel_cmd = [
        "ssh",
        "-fN",
        "-M",
        "-S",
        ssh_socket_filename,
        "-o",
        "ExitOnForwardFailure=yes",
        "-o",
        "BatchMode=yes",
        "-o",
        "ServerAliveInterval=1",
        "-o",
        "ServerAliveCountMax=5",
        "-L",
        f"{local_socket}:{remote_socket}",
        hostname,
    ]
    ssh_tunnel_terminate_cmd = [
        "ssh",
        "-S",
        ssh_socket_filename,
        "-O",
        "exit",
        hostname,
    ]
    try:
        logger.debug(f"Execute cmd: {' '.join(ssh_tunnel_cmd)}")
        subprocess.run(
            ssh_tunnel_cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout,
        )
        yield ssh_socket_filename
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError) as ex:
        logger.exception(
            f"Exception occurred when trying to open SSH tunnel:\n{ex}",
            exc_info=False,
        )
        raise SSHTunnelConnectionError(ex) from ex
    finally:
        try:
            logger.debug(
                f"Execute cmd: {' '.join(ssh_tunnel_terminate_cmd)}",
            )
            subprocess.run(
                ssh_tunnel_terminate_cmd,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            logger.debug("Deleting socket file")
            os.remove(local_socket)
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass


def gen_temp_socket_filename(
    prefix: Optional[str] = None, suffix: Optional[str] = None
) -> str:
    """Get filename for temporary socket file."""
    temp_socket_filename = None
    with tempfile.NamedTemporaryFile(
        suffix=suffix, prefix=prefix, dir=tempfile.gettempdir()
    ) as tmpfile:
        temp_socket_filename = tmpfile.name
    if temp_socket_filename is not None:
        return temp_socket_filename
    raise RuntimeError("Unable to create temp file")
