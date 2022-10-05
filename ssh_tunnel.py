import subprocess
import tempfile
from contextlib import contextmanager


@contextmanager
def create_ssh_tunnel(hostname, local_socket, remote_socket):
    ssh_socket_filename = gen_temp_socket_filename(f"{hostname}.")
    ssh_tunnel_cmd = [
        "ssh",
        "-qfN",
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
        "-q",
        "-S",
        ssh_socket_filename,
        "-O",
        "exit",
        hostname,
    ]
    try:
        yield subprocess.run(ssh_tunnel_cmd, check=True)
    finally:
        try:
            subprocess.run(ssh_tunnel_terminate_cmd)
        except subprocess.CalledProcessError:
            pass


def gen_temp_socket_filename(prefix=None, suffix=None):
    temp_socket_filename = None
    with tempfile.NamedTemporaryFile(
        suffix=suffix, prefix=prefix, dir=tempfile.gettempdir()
    ) as tmpfile:
        temp_socket_filename = tmpfile.name
    if temp_socket_filename is not None:
        return temp_socket_filename
    else:
        raise RuntimeError("Unable to create temp file")
