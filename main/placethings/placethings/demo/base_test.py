from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass


class BaseTestCase(with_metaclass(ABCMeta, object)):
    @staticmethod
    @abstractmethod
    def test():
        raise NotImplementedError()
