from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from placethings.config.wrapper.config_gen import Config
from placethings.demo.base_test import BaseTestCase
from placethings.graph_gen.wrapper import graph_gen
from placethings import ilp_solver

log = logging.getLogger()


class TestBasic(BaseTestCase):
    @staticmethod
    def test(config_name=None, is_export=False):
        if not config_name:
            config_name = 'config_sample'
        cfg = Config(folderpath=config_name)
        # graph_gen.create_topo_graph(cfg, is_export)
        Gd = graph_gen.create_device_graph(cfg, is_export)
        Gt = graph_gen.create_task_graph(cfg, is_export)
        ilp_solver.place_things(Gt, Gd, is_export)
