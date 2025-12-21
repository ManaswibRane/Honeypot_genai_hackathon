from parser.event_builder import log_event


class FakeShell:
    def __init__(self, channel, ip):
        self.channel = channel
        self.ip = ip
        self.cwd = "/home/user"
        self.buffer = ""

    def send(self, msg):
        self.channel.send(msg.encode())

    def prompt(self):
        self.send(f"user@honeypot:{self.cwd}$ ")

    def interact(self):
        self.send("Welcome to Ubuntu 20.04 LTS\r\n")
        self.prompt()

        while True:
            data = self.channel.recv(1024)
            if not data:
                break

            for ch in data.decode(errors="ignore"):
                # ENTER pressed
                if ch in ("\r", "\n"):
                    cmd = self.buffer.strip()
                    self.send("\r\n")

                    if cmd:
                        log_event("command", {"ip": self.ip, "cmd": cmd})

                    if cmd in ("exit", "logout"):
                        self.send("logout\r\n")
                        return

                    elif cmd.startswith("cd"):
                        parts = cmd.split(maxsplit=1)
                        self.cwd = parts[1] if len(parts) > 1 else "/home/user"

                    elif cmd:
                        self.send("command not found\r\n")

                    self.buffer = ""
                    self.prompt()

                # BACKSPACE
                elif ch in ("\x7f", "\b"):
                    if self.buffer:
                        self.buffer = self.buffer[:-1]
                        self.send("\b \b")

                # NORMAL CHARACTER
                else:
                    self.buffer += ch
                    self.send(ch)
