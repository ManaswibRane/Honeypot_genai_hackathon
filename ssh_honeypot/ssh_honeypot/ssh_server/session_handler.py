import socket
import threading
import paramiko
from ssh_server.fake_shell import FakeShell
from parser.event_builder import log_event

HOST_KEY = paramiko.RSAKey.generate(2048)


class HoneypotServer(paramiko.ServerInterface):
    def __init__(self, client_ip):
        self.client_ip = client_ip

    def check_auth_password(self, username, password):
        log_event("auth_attempt", {
            "ip": self.client_ip,
            "username": username,
            "password": password
        })
        return paramiko.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        return "password"

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_pty_request(self, *args):
        return True

    def check_channel_shell_request(self, channel):
        return True


def handle_client(client, ip):
    transport = paramiko.Transport(client)
    transport.add_server_key(HOST_KEY)

    server = HoneypotServer(ip)
    transport.start_server(server=server)

    chan = transport.accept(20)
    if chan is None:
        return

    FakeShell(chan, ip).interact()
    transport.close()


def start_server(port=2222):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", port))
    sock.listen(100)

    print(f"[+] SSH Honeypot listening on {port}")

    while True:
        client, addr = sock.accept()
        threading.Thread(
            target=handle_client,
            args=(client, addr[0]),
            daemon=True
        ).start()


if __name__ == "__main__":
    start_server()
