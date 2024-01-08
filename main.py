import subprocess, platform, re
from typing import Any, List, Tuple
from colorama import init, Fore

init()

MAP = {
    "Windows": "netsh wlan show networks",
    "Linux": "nmcli device wifi list",
}


def get_wifi_networks() -> Tuple[str, str]:
    os_name = platform.system()
    return (os_name, subprocess.check_output(MAP[os_name], shell=True, text=True))


def process_unix_output(output: str):
    networks = []
    # Access the captured stdout.
    for x in output.splitlines()[1:]:
        networks.append(x.split()[1])
    return list(set(networks))


def process_windows_output(output: str):
    networks = []
    for line in output.splitlines():
        try:
            if line and line[0] != " ":
                networks.append(line.split(":")[1].strip())
        except Exception:
            continue
    return networks[1:]


def printer(networks):
    print(f"{Fore.LIGHTMAGENTA_EX}[+] Open Wifi networks in range: \n")
    for ssid in list(set(networks)):
        print(f"{Fore.GREEN}[+] {ssid}")


if __name__ == "__main__":
    os_name, output = get_wifi_networks()
    if os_name == "Windows":
        printer(process_windows_output(output))
    if os_name == "Linux":
        printer(process_unix_output(output))
