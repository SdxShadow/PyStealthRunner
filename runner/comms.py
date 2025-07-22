import os
import sys
import socket
import json

PORT = int(os.environ.get("PYSTEALTH_PORT", 50506))

def get_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect(("127.0.0.1", PORT))
    return s

def send_command(cmd):
    s = get_socket()
    s.sendall(json.dumps(cmd).encode())
    s.shutdown(socket.SHUT_WR)
    try:
        data = s.recv(4096)
    except socket.timeout:
        s.close()
        raise TimeoutError("Timed out waiting for response from background service.")
    s.close()
    if data:
        try:
            return json.loads(data.decode())
        except Exception:
            return data.decode()
    return None
