from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import importlib

from placethings.config import config_factory
from placethings.graph_gen import graph_factory
from placethings.utils.common_utils import update_rootlogger


update_rootlogger(level=logging.INFO)
log = logging.getLogger()


class SubArgsManager(object):
    def __init__(self, subparser):
        self.subparser = subparser

    def visualize(self, required=False):
        self.subparser.add_argument(
            '-v',
            '--visualize',
            dest='is_export',
            default=False,
            action='store_true',
            required=required,
            help='export graph and data')

    def config(self, required=False):
        self.subparser.add_argument(
            '-c',
            '--config',
            type=str,
            dest='config_name',
            default=None,
            required=required,
            help=(
                'gen graph base on confiig files. '
                'If not specified, use config_dafult')
        )

    def testcase(self, required=False):
        self.subparser.add_argument(
            '-tc',
            '--testcase',
            type=str,
            dest='testcase',
            default=None,
            required=required,
            help=('demo case name')
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
    def create_topograph(args):
        config_name = args.config_name
        graph_factory.gen_topo_graph(config_name, is_export=True)

    @staticmethod
    def create_taskgraph(args):
        config_name = args.config_name
        graph_factory.gen_task_graph(config_name, is_export=True)

    @staticmethod
    def create_devicegraph(args):
        config_name = args.config_name
        graph_factory.gen_device_graph(config_name, is_export=True)

    @staticmethod
    def export_all_graph(args):
        config_name = args.config_name
        graph_factory.gen_device_graph(config_name, is_export=True)
        graph_factory.gen_task_graph(config_name, is_export=True)
        graph_factory.gen_topo_graph(config_name, is_export=True)

    @staticmethod
    def demo(args):
        testcase = args.testcase
        config_name = args.config_name
        is_export = args.is_export
        if not testcase:
            log.error('must specify test case name')
            return
        module_name, case_name = testcase.split('.')
        module_name = 'placethings.demo.{}'.format(module_name)
        log.info('run test case: {} in {}'.format(case_name, module_name))
        demo_case_module = importlib.import_module(module_name)
        demo_case_class = getattr(demo_case_module, case_name)
        demo_case_class.test(config_name, is_export)

    @staticmethod
    def export_default_config(args):
        config_factory.export_default_config()


def main():
    args_manager = ArgsManager()

    name = 'create_topograph'
    subargs_manager = args_manager.add_subparser(
        name,
        func=getattr(FuncManager, name),
        help='generate network topology')
    subargs_manager.config(required=False)

    name = 'create_taskgraph'
    subargs_manager = args_manager.add_subparser(
        name,
        func=getattr(FuncManager, name),
        help='generate task graph')
    subargs_manager.config(required=False)

    name = 'create_devicegraph'
    subargs_manager = args_manager.add_subparser(
        name,
        func=getattr(FuncManager, name),
        help='generate network graph')
    subargs_manager.config(required=False)

    name = 'export_all_graph'
    subargs_manager = args_manager.add_subparser(
        name,
        func=getattr(FuncManager, name),
        help='export all config to json')
    subargs_manager.config(required=False)

    name = 'demo'
    subargs_manager = args_manager.add_subparser(
        name,
        func=getattr(FuncManager, name),
        help=(
            'run demo cases. '
            'e.g. -tc test_deploy.test_deploy_default'))
    subargs_manager.visualize(required=False)
    subargs_manager.config(required=False)
    subargs_manager.testcase(required=False)

    name = 'export_default_config'
    subargs_manager = args_manager.add_subparser(
        name,
        func=getattr(FuncManager, name),
        help='export all default config to json')

    args = args_manager.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
