"""
This file is used to test ping to the devices, which is used to check connectivity to the devices.
Ping is tested on all the linux/windows based devices

For other devices (smarphone etc), an alternative functionality such as rest api is used
"""

import subprocess


def check_ping(ip='127.0.0.1'):
    res = subprocess.call(['ping', '-c', '3', ip])
    if res == 0:
        #print("ping to ", ip, " OK")
        return True
    elif res == 2:
        #print("no response from ", ip)
        return False
    else:
        #print("ping to", ip, " failed!")
        return False

    return False
