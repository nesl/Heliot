from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import subprocess

from tasklib.entity.base_client import ClientGen


log = logging.getLogger()


class RPCServer(object):

    def __init__(self, name):
        self.name = name
        log.info('start Agent RPCServer: {}'.format(self.name))
        self.proc_dict = {}

    def fetch_from(self, filename, from_ip, from_port):
        result = ClientGen.call(from_ip, from_port, 'fetch', filename)
        return 'fetch {} from {}:{}, got: {}'.format(
            filename, from_ip, from_port, result)

    def fetch(self, filename):
        return 'fetch {}'.format(filename)

    def delete(self, filename):
        return 'delete {}'.format(filename)

    def get_prog_list(self):
        log.info('getting prog list')
        proc = subprocess.Popen("ps", stdout=subprocess.PIPE)
        result = proc.communicate()[0]
        log.info('result from ps: \n{}'.format(result))
        log.info('result from proc_dict: \n{}'.format(self.proc_dict))
        return [name for name in self.proc_dict]

    def start_prog(self, prog_name, cmd):
        log.info('try to start prog: {}'.format(prog_name))
        if prog_name in self.proc_dict:
            log.warning('prog is already running: {}'.format(prog_name))
            return 'prog is already running: {}'.format(prog_name)
        log.info('run cmd in shell: {}'.format(cmd))
        proc = subprocess.Popen(cmd, shell=True)
        self.proc_dict[prog_name] = proc
        log.info('prog is running: {}, pid={}'.format(prog_name, proc.pid))
        return 'prog started successfully: {}'.format(prog_name)

    def stop_prog(self, prog_name):
        log.info('try to stop prog: {}'.format(prog_name))
        if prog_name not in self.proc_dict:
            log.warning('prog is not running: {}'.format(prog_name))
            return 'prog is not running: {}'.format(prog_name)
        proc = self.proc_dict[prog_name]
        log.info('stopping prog: {}, pid={}'.format(prog_name, proc.pid))
        proc.terminate()
        del self.proc_dict[prog_name]
        return 'prog stopped successfully: {}'.format(prog_name)
