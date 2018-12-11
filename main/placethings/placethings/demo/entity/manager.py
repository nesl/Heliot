from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future.utils import iteritems
import logging

from placethings.demo.entity.base_client import ClientGen


log = logging.getLogger()


class Manager(object):

    def __init__(
            self, name, fileserver_ip, fileserver_port,
            task_data, device_data):
        self.name = name
        self.fileserver_ip = fileserver_ip
        self.fileserver_port = fileserver_port
        self.task_data = task_data
        self.device_data = device_data
        self.cur_map = None
        self.cur_device_addr = None
        self.cur_deploy_cnt = 0

    def clean_up(self, servermap):
        for ip, port in iteritems(servermap):
            result = ClientGen.call(ip, port, 'STOP')
            log.info('stop server @{}:{}, {}'.format(ip, port, result))

    @staticmethod
    def trigger_start_prog(agent, ip, port, command):
        log.info('ask agent {} to run command: {}'.format(agent, command))
        result = ClientGen.call(ip, port, 'start_prog', command)
        log.info('result: {}'.format(result))

    def init_deploy(self, mapping, device_addr):
        log.info('deploy {} ===='.format(self.cur_deploy_cnt))
        for task, device in iteritems(mapping):
            ip, port = device_addr[device]
            result = ClientGen.call(
                ip, port, 'fetch_from', task,
                self.fileserver_ip, self.fileserver_port)
            log.info('depoly {} to {}: {}'.format(task, device, result))
        self.cur_map = mapping
        self.cur_deploy_cnt += 1

    def re_deploy(self, mapping, device_addr):
        log.info('deploy {} ===='.format(self.cur_deploy_cnt))
        for task, device in iteritems(mapping):
            device_has_task = self.cur_map[task]
            if device_has_task == device:
                continue
            ip, port = device_addr[device]
            server_ip, server_port = device_addr[device_has_task]
            result = ClientGen.call(
                ip, port, 'fetch_from', task, server_ip, server_port)
            log.info('move {} from {} to {}: {}'.format(
                task, device_has_task, device, result))
        self.cur_map = mapping
        self.cur_deploy_cnt += 1
