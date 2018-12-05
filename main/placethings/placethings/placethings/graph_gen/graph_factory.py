from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from placethings.graph_gen import device_graph, task_graph, topo_graph
from placethings.config.config_factory import FileHelper


log = logging.getLogger()


def gen_device_graph(config_name, is_export=False):
    dev_file = FileHelper.gen_config_filepath(config_name, 'device_data')
    nw_file = FileHelper.gen_config_filepath(config_name, 'nw_device_data')
    Gd = device_graph.create_graph_from_file(dev_file, nw_file, is_export)
    return Gd


def gen_task_graph(config_name, is_export=False):
    filepath = FileHelper.gen_config_filepath(config_name, 'task_data')
    Gt = task_graph.create_graph_from_file(filepath, is_export)
    return Gt


def gen_topo_graph(config_name, is_export=False):
    filepath = FileHelper.gen_config_filepath(config_name, 'nw_device_data')
    Gn = topo_graph.create_graph_from_file(filepath, is_export)
    return Gn
