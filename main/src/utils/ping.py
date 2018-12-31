"""
This file is used to test ping to the devices
Ping is tested on all the linux/windows based devices

For other devices (smarphone etc), an alternative functionality such as rest api is used
"""

import subprocess


def check_ping(address='127.0.0.1'):
    res = subprocess.call(['ping', '-c', '3', address])
    if res == 0:
        print("ping to", address, "OK")
        return True
    elif res == 2:
        print("no response from", address)
    else:
        print("ping to", address, "failed!")
    return False
