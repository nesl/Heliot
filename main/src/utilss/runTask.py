import paramiko
import sys
import os as sys_os


def runTask(ip, username, password):
    try:
        #print(ip, ' ', username, ' ',password)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, timeout=5, look_for_keys=False, username=username, password=password)

        cmd = 'cd heliot_runtime/Heliot/main/src; python3 runTaskOnDevice.py'
        stdin, stdout, stderr = client.exec_command(cmd)

        exit_status = stdout.channel.recv_exit_status()          # Blocking call

        output = stdout.readlines()
        print('output is:',output,":" ,type(output))
        outputerr = stderr.readlines()
        print('outputerr is:',outputerr,":" ,type(outputerr))


    except Exception as e:
        print(e)
