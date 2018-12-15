from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from placethings.config.wrapper.config_gen import Config
from placethings.config.helper import ConfigDataHelper
from placethings.netgen.network import init_netsim
from placethings.demo.base_test import BaseTestCase, wait_key


log = logging.getLogger()

"""
Usage:

1. send sample image from your local terminal to the fake camera in mininet:
$ cd placethings/sample_tasklib
$ python main_entity.py client_send_file -n client1 -a 172.17.20.12:20000 \
  -m push -al sample_img/2-0.png

2. use browser open http://172.17.20.12:20001/ to see the result



Network settings

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

Latency:
  all wired link: 2 ms
  except AP -> SW: 30 ms

Scenrios:
(1) all links alive

"""


class Test(BaseTestCase):
    _SUPPORTED_CONFIG = {
        "sample_configs/config_ddflow_demo_local"
    }

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

        log.info("=== start mininet ===")

        _topo, topo_device_graph, G_map = cfgHelper.get_graphs()

        data_plane = init_netsim(
            topo_device_graph, G_map, 'BB_SWITCH.2',
            docker_img='kumokay/heliot_host:v4',
            prog_dir='/opt/github/unzip_tasklib')
        # wait_key(is_interactive, 'press any key to start the network')
        data_plane.start(is_validate=True)

        data_plane.print_net_info()
        # wait_key(is_interactive, 'press any key to start scenario')
        log.info('=== running scenario: initial deployment ===')
        data_plane.start_workers()

        wait_key(is_interactive, 'press any key to end test')
        if is_simulate:
            data_plane.stop_workers()
            data_plane.stop()
        log.info('latency trend: {}'.format(cfgHelper.get_max_latency_log()))
