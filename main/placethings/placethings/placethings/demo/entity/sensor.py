from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import os
import random
import sched
import time

from placethings.demo.entity.base_client import ClientGen
from placethings.definition import Device


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


class SensorGen(object):
    _DELAY_START_TIME_TICK = 5
    _CYCLE_S = 5
    _DURATION = 20

    @classmethod
    def _get_delay_start_time(cls):
        now = int(time.time())
        return (
            now - (now % cls._DELAY_START_TIME_TICK)
            + (2 * cls._DELAY_START_TIME_TICK))

    @staticmethod
    def _gen_random_byte_str(n):
        return os.urandom(n)

    @classmethod
    def _gen_random_size_byte_str(cls, a, b):
        n = random.randint(a, b)
        return cls._gen_random_byte_str(n)

    @staticmethod
    def _gen_random_int_list(a, b, n):
        return [random.randint(a, b) for _ in range(n)]

    @classmethod
    def start_sensor(cls, name, device_type, receiver_list):
        t_start = cls._get_delay_start_time()

        if device_type == Device.SMOKE:
            # cls._gen_random_int_bytearry(40, 120, 100)
            datagen_func = cls._gen_random_int_list
            datagen_args = (40, 120, 100)
        elif device_type == Device.CAMERA:
            # cls._gen_random_bytearray(random.randint(2000, 4000))
            datagen_func = cls._gen_random_size_byte_str
            datagen_args = (2000, 4000)
        else:
            log.error('no sensor for device type: {}'.format(device_type))
            exit(1)

        BaseSensor(
            name, datagen_func, datagen_args, receiver_list,
            t_start, cls._CYCLE_S, cls._DURATION).start()
