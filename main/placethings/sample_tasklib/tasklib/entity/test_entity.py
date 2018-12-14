from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import msgpackrpc
import time

from tasklib.entity.manager import Manager

log = logging.getLogger()


def _call(ip, port, method, *args):
    client = msgpackrpc.Client(msgpackrpc.Address(ip, port))
    result = client.call(method, *args)
    return result


def test_task():
    t1 = time.time()
    ret = _call(
        '127.0.0.1', 19000, 'push', [1, 2, 3], {'trigger': (t1, time.time())})
    log.info('push: {}'.format(ret))
    ret = _call('127.0.0.1', 19000, 'STOP')
    log.info('stop task: {}'.format(ret))


def test_basic():
    fileserver_ip = '127.0.0.1'
    fileserver_port = 18800
    manager = Manager('manager', fileserver_ip, fileserver_port, None, None)
    device_addr = {
        'device1': ('127.0.0.1', 18901),
        'device2': ('127.0.0.1', 18902),
        'device3': ('127.0.0.1', 18903),
        'device4': ('127.0.0.1', 18904)}
    task_map = {
        'task1': 'device1',
        'task2': 'device2',
        'task3': 'device3',
        'task4': 'device4'}
    manager.init_deploy(task_map, device_addr)
    task_map = {
        'task1': 'device2',
        'task2': 'device1',
        'task3': 'device3',
        'task4': 'device4'}
    manager.re_deploy(task_map, device_addr)
    task_map = {
        'task1': 'device1',
        'task2': 'device2',
        'task3': 'device4',
        'task4': 'device3'}
    manager.re_deploy(task_map, device_addr)
