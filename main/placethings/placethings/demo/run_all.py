from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import os
import importlib
import inspect
import sys

from placethings.demo.base_test import BaseTestCase

log = logging.getLogger()


class Test(BaseTestCase):
    @staticmethod
    def test(config_name=None, is_export=True):
        fs = [
            f for f in os.listdir('placethings/demo')
            if f.startswith('test') and f.endswith('.py')]
        all_test_names = []
        for filename in fs:
            test_case_module = importlib.import_module(
                'placethings.demo.{}'.format(filename[:-3]))
            for member in inspect.getmembers(test_case_module):
                if member[0].startswith('Test'):
                    test_name = '{}.{}'.format(filename[:-3], member[0])
                    log.info('===============================================')
                    log.info('running Test: {}'.format(test_name))
                    log.info('===============================================')
                    try:
                        obj = getattr(test_case_module, member[0])
                        obj.test(
                            config_name=config_name,
                            is_export=is_export,
                            is_interactive=False)
                        all_test_names.append(test_name)
                    except (Exception, RuntimeError, TypeError, NameError):
                        log.error(sys.exc_info()[0])
                        log.error('test case {} failed.'.format(test_name))
                        log.info('passed test cases:')
                        for test_name in all_test_names:
                            log.info('ran Test: {}'.format(test_name))
                        exit(0)
        log.info('===============================================')
        for test_name in all_test_names:
            log.info('ran Test: {}'.format(test_name))
