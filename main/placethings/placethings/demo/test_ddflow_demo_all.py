from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from placethings.config.wrapper.config_gen import Config
from placethings.config.definition.common_def import Unit
from placethings.config.helper import ConfigDataHelper
from placethings.netgen.network import init_netsim
from placethings.demo.base_test import BaseTestCase, wait_key

log = logging.getLogger()

"""
network settings

CONTROLLER.0   P3_2XLARGE.0  T3_LARGE.0
       |         |              |
CENTER_SWITCH.1 CENTER_SWITCH.0  FIELD_SWITCH.1   (manager)      T2_MICRO.0
        |       |                |                 |               |
      BB_SWITCH.0 --------- BB_SWITCH.1 ---- BB_SWITCH.2 ----FIELD_SWITCH.0
        |                    |                 |
     BB_AP.0               BB_AP.1         BB_AP.2
        |
     CAMERA.0


Drone1 ====flying path================>
Drone2 (standby)

Latency:
  all wired link: 2 ms
  except AP -> SW: 30 ms

Scenrios:
(1) all links alive
(2) P3.X2LARGE.0 offline
(3) T3.XLARGE.0 offline
(4) P3.X2LARGE.0 back online

"""


class TestBasic(BaseTestCase):
    _SUPPORTED_CONFIG = {
        "sample_configs/config_ddflow_demo",
    }

    @classmethod
    def test(
            cls, config_name=None, is_export=True, is_simulate=True,
            is_interactive=True):
        if not config_name:
            config_name = 'sample_configs/config_ddflow_demo'
        assert config_name in cls._SUPPORTED_CONFIG
        cfgHelper = ConfigDataHelper(Config(config_name), is_export)
        cfgHelper.init_task_graph()
        cfgHelper.update_topo_device_graph()
        cfgHelper.update_task_map()
        _topo, topo_device_graph, G_map = cfgHelper.get_graphs()
        if is_simulate:
            data_plane = init_netsim(
                topo_device_graph, G_map, 'BB_SWITCH.2')
            data_plane.start(is_validate=True)
            data_plane.start_workers()
            data_plane.stop_workers()
            data_plane.stop()


class TestDynamic(BaseTestCase):
    _SUPPORTED_CONFIG = {
        "sample_configs/config_ddflow_demo_local",
    }

    @classmethod
    def update_nw_latency(
            cls, cfgHelper, data_plane, nw_dev1, nw_dev2, new_latency,
            is_simulate):
        cfgHelper.update_nw_link_latency(nw_dev1, nw_dev2, new_latency)
        cfgHelper.update_topo_device_graph()
        if is_simulate:
            data_plane.modify_link(nw_dev1, nw_dev2, delay_ms=new_latency)
            data_plane.print_net_info()

    @classmethod
    def update_placement(
            cls, cfgHelper, data_plane, is_simulate, is_interactive):
        wait_key(is_interactive, 'press any key to find new placement')
        cfgHelper.update_task_map()
        cfgHelper.update_max_latency_log()
        if is_simulate:
            _topo, topo_device_graph, G_map = cfgHelper.get_graphs()
            data_plane.deploy_task(G_map, topo_device_graph)
            wait_key(is_interactive, 'press any key to re-deploy')
            data_plane.stop_workers()
            data_plane.start_workers()
            data_plane.print_net_info()

    @classmethod
    def test(
            cls, config_name=None, is_export=True, is_interactive=True,
            is_update_map=True, is_simulate=True):
        if not config_name:
            config_name = 'sample_configs/config_ddflow_demo_local'
        assert config_name in cls._SUPPORTED_CONFIG
        cfgHelper = ConfigDataHelper(Config(config_name), is_export)
        cfgHelper.init_task_graph()
        cfgHelper.update_topo_device_graph()
        cfgHelper.update_task_map()
        cfgHelper.update_max_latency_log()
        # scenarios:
        # (1) initial deployment, all links are alive
        # (2) P3.X2LARGE.0 poor connection
        # (3) T3.XLARGE.0 poor connection
        # (4) P3.X2LARGE.0 back online
        data_plane = None
        if is_simulate:
            log.info("=== start mininet ===")
            _topo, topo_device_graph, G_map = cfgHelper.get_graphs()
            data_plane = init_netsim(
                topo_device_graph, G_map, 'BB_SWITCH.2',
                docker_img='kumokay/heliot_host:v4',
                prog_dir='/opt/github/unzip_tasklib')
            wait_key(is_interactive, 'press any key to start the network')
            data_plane.start(is_validate=True)
            data_plane.print_net_info()

        wait_key(is_interactive, 'press any key to start scenario 1')
        log.info('=== running scenario 1: initial deployment ===')
        if is_simulate:
            data_plane.start_workers()
            data_plane.print_net_info()
        wait_key(is_interactive, 'press any key to start scenario 2')
        log.info('=== running scenario 2: P3_2XLARGE.0 poor connection ===')
        nw_dev1 = 'BB_SWITCH.0'
        nw_dev2 = 'CENTER_SWITCH.1'
        new_latency = Unit.ms(3000)
        cls.update_nw_latency(
            cfgHelper, data_plane, nw_dev1, nw_dev2, new_latency, is_simulate)
        if is_update_map:
            cls.update_placement(
                cfgHelper, data_plane, is_simulate, is_interactive)

        wait_key(is_interactive, 'press any key to start scenario 3')
        log.info('=== running scenario 3: T3_LARGE.0 poor connection ===')
        nw_dev1 = 'BB_SWITCH.1'
        nw_dev2 = 'FIELD_SWITCH.1'
        new_latency = Unit.ms(2000)
        cls.update_nw_latency(
            cfgHelper, data_plane, nw_dev1, nw_dev2, new_latency, is_simulate)
        if is_update_map:
            cls.update_placement(
                cfgHelper, data_plane, is_simulate, is_interactive)

        wait_key(is_interactive, 'press any key to start scenario 4')
        log.info('=== running scenario 4: P3_2XLARGE.0 back online ===')
        nw_dev1 = 'BB_SWITCH.0'
        nw_dev2 = 'CENTER_SWITCH.1'
        new_latency = Unit.ms(2)
        cls.update_nw_latency(
            cfgHelper, data_plane, nw_dev1, nw_dev2, new_latency, is_simulate)
        if is_update_map:
            cls.update_placement(
                cfgHelper, data_plane, is_simulate, is_interactive)

        wait_key(is_interactive, 'press any key to end test')
        if is_simulate:
            data_plane.stop_workers()
            data_plane.stop()
        log.info('latency trend: {}'.format(cfgHelper.get_max_latency_log()))
