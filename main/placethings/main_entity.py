from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import base64
import logging

from placethings.demo.entity import test_entity
from placethings.demo.entity.base_server import ServerGen
from placethings.demo.entity.sensor import SensorGen
from placethings.demo.entity.base_client import ClientGen
from placethings.utils.common_utils import update_rootlogger
from placethings.definition import EnumHelper

update_rootlogger()
log = logging.getLogger()


class SubArgsManager(object):
    def __init__(self, subparser):
        self.subparser = subparser

    def name(self, required=False):
        self.subparser.add_argument(
            '-n',
            '--name',
            type=str,
            dest='name',
            default=None,
            required=required,
            help=('name')
        )

    def address(self, required=False):
        self.subparser.add_argument(
            '-a',
            '--address',
            type=str,
            dest='address',
            default=None,
            required=required,
            help=('address (ip:port). e.g. 10.11.12.13:1234')
        )

    def next_address(self, required=False, nargs=1):
        self.subparser.add_argument(
            '-ra',
            '--recv_address',
            type=str,
            nargs=nargs,
            dest='recv_address',
            default=[],
            required=required,
            help=('receiver address (ip:port). e.g. 10.11.12.13:1234')
        )

    def sensor_type(self, required=False):
        self.subparser.add_argument(
            '-st',
            '--sensor_type',
            type=str,
            dest='sensor_type',
            default=None,
            required=required,
            help=('sensor_type (int)')
        )

    def exectime(self, required=False):
        self.subparser.add_argument(
            '-t',
            '--exectime',
            type=int,
            dest='exectime',
            default=0,
            required=required,
            help=('exectime (ms)')
        )

    def method(self, required=False):
        self.subparser.add_argument(
            '-m',
            '--method',
            type=str,
            dest='method',
            default=None,
            required=required,
            help=('rpc method name')
        )

    def args_list(self, required=False):
        self.subparser.add_argument(
            '-al',
            '--args_list',
            type=str,
            nargs='+',
            dest='args_list',
            default=[],
            required=required,
            help=('args list')
        )

    def testcase(self, required=False):
        self.subparser.add_argument(
            '-tc',
            '--testcase',
            type=str,
            dest='testcase',
            default=None,
            required=required,
            help=('testcase name')
        )

    def entity_name(self, required=False):
        self.subparser.add_argument(
            '-en',
            '--entity',
            type=str,
            dest='entity_name',
            default=None,
            required=required,
            help=('entity name, e.g. task_findObj')
        )


class ArgsManager(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(prog='PROG')
        self.subparsers = self.parser.add_subparsers(help='sub-command help')

    def add_subparser(self, option_name, func, help='help'):
        subparser = self.subparsers.add_parser(
            option_name,
            help=help)
        subparser.set_defaults(func=func)
        return SubArgsManager(subparser)

    def parse_args(self):
        return self.parser.parse_args()


class FuncManager(object):

    @staticmethod
    def _split_addr(address):
        ip, port = address.split(':')
        return ip, int(port)

    @classmethod
    def run_agent(cls, args):
        name = args.name
        ip, port = cls._split_addr(args.address)
        update_rootlogger(name, is_log_to_file=True)
        ServerGen.start_server(name, 'agent', ip, port)

    @classmethod
    def run_fileserver(cls, args):
        name = args.name
        ip, port = cls._split_addr(args.address)
        port = int(port)
        update_rootlogger(name, is_log_to_file=True)
        ServerGen.start_server(name, 'fileserver', ip, port)

    @classmethod
    def run_task(cls, args):
        name = args.name
        ip, port = cls._split_addr(args.address)
        port = int(port)
        exec_time_ms = args.exectime
        addr_list = []
        extra_param_list = args.args_list
        for addr in args.recv_address:
            next_ip, next_port = addr.split(':')
            next_port = int(next_port)
            addr_list.append((next_ip, next_port))
        entity_name = args.entity_name
        if entity_name is None:
            entity_name = 'task'
        update_rootlogger(name, is_log_to_file=True)
        ServerGen.start_server(
            name, entity_name, ip, port,
            exec_time_ms, addr_list, extra_param_list)

    @classmethod
    def run_actuator(cls, args):
        name = args.name
        ip, port = cls._split_addr(args.address)
        update_rootlogger(name, is_log_to_file=True)
        ServerGen.start_server(
            name, 'task', ip, port, 0, None)

    @classmethod
    def run_sensor(cls, args):
        name = args.name
        sensor_type = EnumHelper.str_to_enum(args.sensor_type)
        next_ip, next_port = cls._split_addr(args.recv_address)
        next_port = int(next_port)
        update_rootlogger(name, is_log_to_file=True)
        # def create(cls, name, sensor_type, receiver_dict):
        SensorGen.start_sensor(
            name, sensor_type, [(next_ip, next_port)])

    @classmethod
    def run_client(cls, args):
        name = args.name
        ip, port = cls._split_addr(args.address)
        method = args.method
        args_list = args.args_list
        update_rootlogger(name, is_log_to_file=True)
        result = ClientGen.call(ip, port, method, *args_list)
        log.info('result: {}'.format(result))

    @classmethod
    def client_send_file(cls, args):
        name = args.name
        ip, port = cls._split_addr(args.address)
        method = args.method
        args_list = args.args_list
        update_rootlogger(name, is_log_to_file=True)
        assert len(args_list) == 1
        filepath = args_list[0]
        with open(filepath, 'rb') as binary_file:
            # Read the whole file at once
            data = binary_file.read()
        new_args_list = [base64.b64encode(data)]
        result = ClientGen.call(ip, port, method, *new_args_list)
        log.info('file sent: size={}'.format(len(result)))

    @staticmethod
    def run_test(args):
        case_name = args.testcase
        update_rootlogger(case_name, is_log_to_file=True)
        getattr(test_entity, case_name)()

    @classmethod
    def stop_server(cls, args):
        name = args.name
        ip, port = cls._split_addr(args.address)
        update_rootlogger(name, is_log_to_file=True)
        ServerGen.stop_server(ip, port)


def main():
    args_manager = ArgsManager()

    name = 'run_agent'
    subargs_manager = args_manager.add_subparser(
        name,
        func=getattr(FuncManager, name),
        help='run_agent')
    subargs_manager.name(required=True)
    subargs_manager.address(required=True)

    name = 'run_fileserver'
    subargs_manager = args_manager.add_subparser(
        name,
        func=getattr(FuncManager, name),
        help='run_fileserver')
    subargs_manager.name(required=True)
    subargs_manager.address(required=True)

    name = 'stop_server'
    subargs_manager = args_manager.add_subparser(
        name,
        func=getattr(FuncManager, name),
        help='stop_server')
    subargs_manager.name(required=True)
    subargs_manager.address(required=True)

    name = 'run_task'
    subargs_manager = args_manager.add_subparser(
        name,
        func=getattr(FuncManager, name),
        help='run_task')
    subargs_manager.name(required=True)
    subargs_manager.address(required=True)
    subargs_manager.next_address(required=False, nargs='+')
    subargs_manager.exectime(required=False)
    subargs_manager.entity_name(required=False)
    subargs_manager.args_list(required=False)

    name = 'run_actuator'
    subargs_manager = args_manager.add_subparser(
        name,
        func=getattr(FuncManager, name),
        help='run_actuator')
    subargs_manager.name(required=True)
    subargs_manager.address(required=True)

    name = 'run_sensor'
    subargs_manager = args_manager.add_subparser(
        name,
        func=getattr(FuncManager, name),
        help='run_sensor')
    subargs_manager.name(required=True)
    subargs_manager.address(required=True)
    subargs_manager.sensor_type(required=True)
    subargs_manager.next_address(required=True)

    name = 'run_client'
    subargs_manager = args_manager.add_subparser(
        name,
        func=getattr(FuncManager, name),
        help='run_client')
    subargs_manager.name(required=True)
    subargs_manager.address(required=True)
    subargs_manager.method(required=True)
    subargs_manager.args_list(required=False)

    name = 'client_send_file'
    subargs_manager = args_manager.add_subparser(
        name,
        func=getattr(FuncManager, name),
        help='client_send_file')
    subargs_manager.name(required=True)
    subargs_manager.address(required=True)
    subargs_manager.method(required=True)
    subargs_manager.args_list(required=False)

    name = 'run_test'
    subargs_manager = args_manager.add_subparser(
        name,
        func=getattr(FuncManager, name),
        help='run_test')
    subargs_manager.testcase(required=True)

    args = args_manager.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
