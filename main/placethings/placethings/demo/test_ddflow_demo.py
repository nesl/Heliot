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

Latency:
  all wired link: 2 ms
  except AP -> SW: 30 ms

Scenrios:
(1) all links alive

"""


class Test(BaseTestCase):
    _SUPPORTED_CONFIG = {
        "sample_configs/config_ddflow_demo",
    }

    @classmethod
    def test(
            cls, config_name=None, is_export=True, is_interactive=True,
            is_update_map=True, is_simulate=True):
        if not config_name:
            config_name = 'sample_configs/config_ddflow_demo'
        assert config_name in cls._SUPPORTED_CONFIG

        # Config(config_name): This reads the file and all the json data in
        #   devices, nw_devices and tasks
        cfgHelper = ConfigDataHelper(Config(config_name), is_export)

        # Task graph is generated, let us print it
        cfgHelper.init_task_graph()
        # Task Name with the node names.
        # Task links is the connectivity, used for data flow
        # Task attributes are the attributes from task file about how to invoke
        #   the task.
        # Task attributed also have the resources required

        # Device graph along with links
        cfgHelper.update_topo_device_graph()
        #

        #
        # wait_key(is_interactive, 'Sandeep Task Graph: Press enter to continue: ')
        #
        # print('*'*100)
        # print('*'*100)
        # print('Nodes in the task graph')
        # print(list(cfgHelper.Gt.nodes))
        #
        # print('*'*100)
        # print('*'*100)
        # print('Edges in the task graph')
        # print(list(cfgHelper.Gt.edges))
        #
        #
        # wait_key(is_interactive, 'Sandeep Device Graphs: Press enter to continue: ')
        #
        # print('*'*100)
        # print('*'*100)
        # #print('Nodes in the graphs')
        #
        # print(list(cfgHelper.Gn.nodes))
        # print('*'*100)
        # print(list(cfgHelper.Gn.edges))
        # print('*'*100)
        # print('*'*100)
        #
        # print(list(cfgHelper.Gnd.nodes))
        # print('*'*100)
        # print(list(cfgHelper.Gnd.edges))
        # print('*'*100)
        # print('*'*100)
        #
        #
        # print(list(cfgHelper.Gd.nodes))
        # print('*'*100)
        # print(list(cfgHelper.Gd.edges))
        #
        #
        #
        # exit(0)

        # This is the ILP ilp_solver
        # Katie is solving for all but updating only for the unique_id=0
        # ILP solver is using Gt and Gd.  Gd is devices connectivity and has
        #   nothing about network. network is included in the terms of devices
        #   connectivity
        cfgHelper.update_task_map()

        # This is again some ILP functionality
        # Getting the maximum latency for the current mapping
        # Max latency canbe obtained only once the solution is fully mapped
        cfgHelper.update_max_latency_log()

        log.info("=== start mininet ===")

        # Gd is the devices graphs (All has the network devices (switches,AP)
        #   and links)
        # G_map is the ILP solved mapping of the tasks to devices
        # _topo: this is not used. Is the network graph, only network devices
        # topo_device_graph: network devices + devices (We use this for the
        #   creation of mininet)
        _topo, topo_device_graph, G_map = cfgHelper.get_graphs()

        # Printing the graphs which we are using in the AirSim

        # wait_key(is_interactive, 'Sandeep Task Graph: Press enter to continue: ')
        #
        # print('*'*100)
        # print('*'*100)
        # print('Nodes in the topo_device_graph graph')
        # print(list(topo_device_graph.nodes))
        #
        # print('*'*100)
        # print('*'*100)
        # print('Edges in the topo_device_graph graph')
        # print(list(topo_device_graph.edges))

        # print('*'*100)
        # print('*'*100)
        # print('Nodes in the Gd graph')
        # print(list(Gd.nodes))
        #
        # print('*'*100)
        # print('*'*100)
        # print('Edges in the Gd graph')
        # print(list(Gd.edges))
        #
        #
        # print('*'*100)
        # print('*'*100)
        # print('Nodes in the G_map graph')
        # print(list(G_map.nodes))
        #
        # print('*'*100)
        # print('*'*100)
        # print('Edges in the G_map graph')
        # print(list(G_map.edges))

        # exit(0)

        # We are getting some graphs and then calling the _init_netsim
        # To every device container/host container in the Mininet, we
        # have two IPS: Mininer_ip = ip, and docker_ip. ip is used
        # to talk containers with each other (so that they follow the Mininet
        #   network characteristics)
        # docker_ip is used by the external process in the same machine to
        #   forward data to the mininet hosts(docker container)
        # Docker containers by default have access to outside network (external
        #   machines, internet)

        data_plane = init_netsim(topo_device_graph, G_map, 'BB_SWITCH.2')
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
