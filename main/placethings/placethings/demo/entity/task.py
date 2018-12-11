from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import time

from placethings.demo.entity.base_client import ClientGen


log = logging.getLogger()


class RPCServer(object):
    def __init__(
            self, name, exec_delay_time_sec,
            receiver_list=None, extra_param_list=None):
        self.name = name
        self.exec_delay_time_sec = exec_delay_time_sec / 1000.0
        self.receiver_list = receiver_list
        if not extra_param_list:
            extra_param_list = []
        self.extra_param_list = extra_param_list
        log.info(
            'start Task RPCServer: {}, delay_exectime={}ms, '
            'receivers={}, extra_params={}'.format(
                self.name, self.exec_delay_time_sec, self.receiver_list,
                self.extra_param_list))

    def _compute(self, data, extra_param_list):
        t1 = time.time()
        log.info('(TIME) start computation: {}'.format(t1))
        if self.exec_delay_time_sec > 0:
            time.sleep(self.exec_delay_time_sec)
        t2 = time.time()
        log.info('(TIME) stop computation: {}'.format(t2))
        return 'spent {} to compute result'.format(t2-t1)

    def push(self, data):
        if not self.receiver_list:
            log.info('got data, size={}'.format(len(data)))
            return 'receive data'
        else:
            result = self._compute(data, self.extra_param_list)
            for next_ip, next_port in self.receiver_list:
                log.info('push data to {}:{}'.format(next_ip, next_port))
                ClientGen.call(next_ip, next_port, 'push', result)
            # logging
            log.info('got data: {}'.format(data))
            log.info('compute result: {}'.format(result))
            return 'recieve and forward data: {} bytes'.format(len(data))
