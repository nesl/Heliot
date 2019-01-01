"""

ssh file is used to connect to linux and window based devices in heliot_runtime
During initialization ssh connection is used to download heliot repo from github and corresponding services on the devices are started.

"""

import paramiko
import sys

def do_intializaton_linux(ip, username, password, logger):
    try:
        #print(ip, ' ', username, ' ',password)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, timeout=5, look_for_keys=False, username=username, password=password)

        cmd = 'rm -r heliot_runtime'
        stdin, stdout, stderr = client.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status()          # Blocking call
        # if exit_status == 0:
        #     print ("File Deleted")
        # else:
        #     print("Error", exit_status)


        cmd = 'mkdir heliot_runtime'
        stdin, stdout, stderr = client.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status()          # Blocking call

        cmd = 'if test -d heliot_runtime; then echo "exist"; fi '
        stdin, stdout, stderr = client.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status()          # Blocking call

        output = stdout.readlines()
        #print('output is:',str(output[0]),":" ,type(output))

        if str(output[0])!= 'exist\n':
            logger.error('heliot_runtime directory cannot be created')
            sys.exit()

        logger.info('heliot_runtime directory created')


        cmd = 'cd heliot_runtime; git clone -b dev --single-branch  https://github.com/nesl/Heliot.git'
        stdin, stdout, stderr = client.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status()          # Blocking call

        #checking is heliot repo cloning was successful and init master file exists
        cmd = 'cd heliot_runtime; if test -d Heliot; then echo "exist"; fi'
        stdin, stdout, stderr = client.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status()          # Blocking call

        output = stdout.readlines()
        #print('output is:',str(output[0]),":" ,type(output))

        if str(output[0])!= 'exist\n':
            logger.error('Not able to download Heliot repo from Github')
            sys.exit()

        logger.info('Heliot repo downloaded from Github')
        client.close()


        # A new client to start a non-blocking call
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, timeout=5, look_for_keys=False, username=username, password=password)

        cmd = 'cd heliot_runtime/Heliot/main/src; python3 init.py &'
        stdin, stdout, stderr = client.exec_command(cmd)

        # output = stdout.readlines()
        # print('stdout output is:',output)
        #
        # output = stderr.readlines()
        # print('stderr output is:',output)

        client.close()
        return True
    except Exception as e:
        print(e)
        return False
