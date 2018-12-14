from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import sched
import time

from tasklib.entity.base_client import ClientGen


log = logging.getLogger()


class BaseSensor(object):

    def __init__(
            self, name, datagen_func, datagen_args, receiver_list,
            t_start, cycle_s, running_time_s, priority=1):
        self.name = name
        self.datagen_func = datagen_func
        self.datagen_args = datagen_args
        self.receiver_list = receiver_list
        self.t_start = t_start
        self.cycle = cycle_s
        self.t_end = t_start + running_time_s
        self.priority = 1
        log.info('start BaseSensor: {}'.format(self.name))

    def _send_data(self, *args):
        data = self.datagen_func(*args)
        for ip, port in self.receiver_list:
            ClientGen.call(ip, port, 'push', data)

    def create_schedule(self):
        log.info('create schedule from {} to {}, cycle={}'.format(
            self.t_start, self.t_end, self.cycle))
        scheduler = sched.scheduler(time.time, time.sleep)
        for t_event in range(self.t_start, self.t_end, self.cycle):
            log.info('add event at {}'.format(t_event))
            scheduler.enterabs(
                t_event, self.priority, self._send_data, self.datagen_args)
        return scheduler

    def start(self):
        log.info('sensor start at {}'.format(time.time()))
        self.create_schedule().run()
