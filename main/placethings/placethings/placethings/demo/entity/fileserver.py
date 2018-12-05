from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


class RPCServer(object):

    def __init__(self, name):
        self.name = name

    def fetch(self, filename):
        return 'fetch {}'.format(filename)
