import paramiko
import sys
import os as sys_os

# Given the device connection parameters and the task
# We start the task using the task file name
def runTask(ip, username, password, taskFile):
    try:
        #print(ip, ' ', username, ' ',password)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, timeout=5, look_for_keys=False, username=username, password=password)

        print("Running", str(taskFile))
        cmd = 'cd /home/prince/Desktop/Heliot/main/src; /home/prince/miniconda3/envs/mininet/bin/python runTaskOnDevice.py '+ str(taskFile) + ' &'
        # TODO: Send mapping JSON file

        stdin, stdout, stderr = client.exec_command(cmd)

        # pid=0
        #pid = int(stdout.readline())

        #exit_status = stdout.channel.recv_exit_status()          # Blocking call

        # output = stdout.readlines()
        # print('output is:',output,":" ,type(output))
        # outputerr = stderr.readlines()
        # print('outputerr is:',outputerr,":" ,type(outputerr))
        #print('started task:', taskFile,' :pid is:',pid)
        # client.close()

    except Exception as e:
        print(e)
