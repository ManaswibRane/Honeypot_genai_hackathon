import re

RULES = {
    "recon": re.compile(r"(ls|whoami|uname)", re.I),
    "persistence": re.compile(r"(crontab|systemctl)", re.I),
}
