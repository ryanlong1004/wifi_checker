""" Responsible for main execution of application
"""
import subprocess
import platform
from typing import Tuple, List
from colorama import init, Fore

init()

MAP = {
    "Windows": "netsh wlan show networks",
    "Linux": "nmcli device wifi list",
}


def get_wifi_networks() -> Tuple[str, str]:
    """returns a tuple of (os_name, network_name)"""
    _os_name = platform.system()
    return (_os_name, subprocess.check_output(MAP[_os_name], shell=True, text=True))


def process_unix_output(_output: str):
    """processes the result of listing networks in unix based OS"""
    networks = []
    # Access the captured stdout.
    for x in _output.splitlines()[1:]:
        networks.append(x.split()[1])
    return list(set(networks))


def process_windows_output(_output: str):
    """processes the result of listing networks in windows based OS"""
    networks = []
    for line in _output.splitlines():
        try:
            if line and line[0] != " ":
                networks.append(line.split(":")[1].strip())
        except Exception as e:
            print(e)
            continue
    return networks[1:]


def printer(networks: List[str]) -> None:
    """pretty prints a list of networks"""
    print(f"{Fore.LIGHTMAGENTA_EX}[+] Open Wifi networks in range: \n")
    for ssid in list(set(networks)):
        print(f"{Fore.GREEN}[+] {ssid}")


if __name__ == "__main__":
    os_name, output = get_wifi_networks()
    if os_name == "Windows":
        printer(process_windows_output(output))
    if os_name == "Linux":
        printer(process_unix_output(output))
