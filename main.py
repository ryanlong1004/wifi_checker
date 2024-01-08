""" Responsible for main execution of application
"""
import subprocess
import platform
from typing import Tuple, List
from colorama import init, Fore
import click

from loguru import logger

init()

class OsUnknown(Exception):
    def __init__(self, message, errors):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        # Now for your custom code...
        self.errors = errors

def get_wifi_networks() -> str:
    MAP = {
        "Windows": "netsh wlan show networks",
        "Linux": "nmcli device wifi list",
    }

    _os_name = platform.system()
    if _os_name not in MAP:
        raise OsUnknown(f"Unknown operating system: {_os_name}", errors=None)
    return subprocess.check_output(MAP.get(platform.system(), ""), shell=True, text=True)


if __name__ == "__main__":
    print(get_wifi_networks())
