from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from placethings.config.wrapper.config_gen import Config
from placethings.demo.base_test import BaseTestCase
from placethings.graph_gen.wrapper import graph_gen
from placethings.ilp import method

log = logging.getLogger()


class TestBasic(BaseTestCase):
    _SUPPORTED_CONFIG = {
        "sample_configs/config_ddflow_demo",
        "sample_configs/config_ddflow_demo_local",
    }

    @classmethod
    def test(cls, config_name=None, is_export=False, is_interactive=True):
        if not config_name:
            config_name = 'sample_configs/config_ddflow_demo'
        assert config_name in cls._SUPPORTED_CONFIG
        cfg = Config(folderpath=config_name)
        # graph_gen.create_topo_graph(cfg, is_export)
        _Gn, Gnd = graph_gen.create_topo_device_graph(cfg, is_export)
        Gt = graph_gen.create_task_graph(cfg, is_export)
        method.place_things(Gt, Gnd, is_export)


class TestDerivedLatency(BaseTestCase):
    _SUPPORTED_CONFIG = {
        "sample_configs/config_ddflow_bw",
    }

    @classmethod
    def test(cls, config_name=None, is_export=False, is_interactive=True):
        if not config_name:
            config_name = 'sample_configs/config_ddflow_bw'
        assert config_name in cls._SUPPORTED_CONFIG
        cfg = Config(folderpath=config_name)
        # graph_gen.create_topo_graph(cfg, is_export)
        _Gn, Gnd = graph_gen.create_topo_device_graph(cfg, is_export)
        Gt = graph_gen.create_task_graph(cfg, is_export)
        method.place_things(Gt, Gnd, is_export, use_assigned_latency=False)
