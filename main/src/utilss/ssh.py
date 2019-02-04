"""

ssh file is used to connect to linux and window based devices in heliot_runtime
During initialization ssh connection is used to download heliot repo from github and corresponding services on the devices are started.

"""

import paramiko
import sys
import os as sys_os

class MySFTPClient(paramiko.SFTPClient):
    def put_dir(self, source, target):
        ''' Uploads the contents of the source directory to the target path. The
            target directory needs to exists. All subdirectories in source are
            created under target.
        '''
        for item in sys_os.listdir(source):
            if sys_os.path.isfile(sys_os.path.join(source, item)):
                self.put(sys_os.path.join(source, item), '%s/%s' % (target, item))
            else:
                self.mkdir('%s/%s' % (target, item), ignore_existing=True)
                self.put_dir(sys_os.path.join(source, item), '%s/%s' % (target, item))

    def mkdir(self, path, mode=511, ignore_existing=False):
        ''' Augments mkdir by adding an option to not fail if the folder exists  '''
        try:
            super(MySFTPClient, self).mkdir(path, mode)
        except IOError:
            if ignore_existing:
                pass
            else:
                raise



# Transfer heliot repo from master to the device
def transfer_heliot_repo_from_master(ip, username, password, logger):

    try:
        port = 22
        transport = paramiko.Transport((ip,port) )
        #transport.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        transport.connect(username=username, password=password)

        sftp = MySFTPClient.from_transport(transport)



        # Upload

        target_path = '/home/nvidia/heliot_runtime/Heliot/main/src/'
        source_path = '/home/nesl/Heliot/github/Heliot/main/src/'

        sftp.mkdir(target_path, ignore_existing=True)
        sftp.put_dir(source_path, target_path)


        sftp.close()

        transport.close()


        return True
    except Exception as e:
        print(e)
        return False




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

        if len(output) == 0:
            logger.error('heliot_runtime directory cannot be created')
            sys.exit()

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
        # print('output is:',output,":" ,type(output))
        # outputerr = stderr.readlines()
        # print('outputerr is:',outputerr,":" ,type(outputerr))

        if len(output)==0:
            logger.info('Not able to download Heliot repo from Github')
            logger.info('Trying to transfer Heliot repo from master to device')
            if not transfer_heliot_repo_from_master(ip, username, password, logger):
                logger.error('Not able to download Heliot repo from Github')
                logger.error('Not able to transfer Heliot repo from master to device')
                sys.exit()

        if str(output[0])!= 'exist\n':
            logger.error('Not able to download Heliot repo from Github')
            sys.exit()

        logger.info('Heliot repo downloaded from Github')

        cmd = 'cd heliot_runtime/Heliot/main/src; python3 init.py &'
        stdin, stdout, stderr = client.exec_command(cmd)

        #Note should not try to read the output, as this starts a continuous process, and this call will not return
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
