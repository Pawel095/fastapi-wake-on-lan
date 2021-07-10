# Builtins
from platform import system
from subprocess import call


def ping(ip: str):
    param = "-n" if system().lower() == "windows" else "-c"
    command = ["ping", param, "1", ip]
    return call(command) == 0
