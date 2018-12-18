from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import time

from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass


def wait_key(is_interactive, msg):
    if is_interactive:
        user_input = raw_input(msg)
    else:
        time.sleep(3)
        user_input = ''
    return user_input


class BaseTestCase(with_metaclass(ABCMeta, object)):
    @staticmethod
    @abstractmethod
    def test():
        raise NotImplementedError()
