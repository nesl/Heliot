from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import time

from tasklib.entity import task as BaseTask


log = logging.getLogger()


class RPCServer(BaseTask.RPCServer):
    def __init__(
            self, name, exec_delay_time_ms, receiver_list=None,
            extra_param_list=None):
        super(RPCServer, self).__init__(
            name, exec_delay_time_ms, receiver_list, extra_param_list)
        log.info('Class Flavor: task_forward')

    def _compute(self, data, extra_param_list):
        t1 = time.time()
        log.info('(TIME) start computation: {}'.format(t1))
        log.info('forward data')
        if self.exec_delay_time_sec > 0:
            time.sleep(self.exec_delay_time_sec)
        t2 = time.time()
        log.info('(TIME) stop computation: {}'.format(t2))
        log.info('forward delay: {}'.format(t2 - t1))
        return data
