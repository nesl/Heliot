from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from placethings.config import device_data, nw_device_data, task_data
from placethings.utils import common_utils


log = logging.getLogger()


class FileHelper(object):
    DEFAULT_CONF_NAME = 'config_default'
    _FILES = {
        'device_data',
        'nw_device_data',
        'task_data',
    }

    @classmethod
    def gen_config_filepath(cls, config_name, data_type):
        assert data_type in cls._FILES
        filename = '{}.json'.format(data_type)
        return common_utils.get_config_filepath(config_name, filename)


def export_default_config():
    config_name = FileHelper.DEFAULT_CONF_NAME
    filepath = FileHelper.gen_config_filepath(config_name, 'device_data')
    device_data.export_data(filepath)
    filepath = FileHelper.gen_config_filepath(config_name, 'nw_device_data')
    nw_device_data.export_data(filepath)
    filepath = FileHelper.gen_config_filepath(config_name, 'task_data')
    task_data.export_data(filepath)
