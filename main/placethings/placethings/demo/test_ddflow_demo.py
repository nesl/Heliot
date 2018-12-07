from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import subprocess

from placethings.config.wrapper.config_gen import Config
from placethings.demo.utils import ConfigDataHelper
from placethings.demo.base_test import BaseTestCase
from placethings.netgen.network import DataPlane

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


def _check_support_config(config_name):
    _SUPPORTED_CONFIG = {
        "config_ddflow_demo",
    }
    assert config_name in _SUPPORTED_CONFIG


def _init_netsim(topo_device_graph, Gd, G_map):
    # get containernet (docker) subnet ip
    cmd = (
        "ifconfig | grep -A 1 'docker'"
        " | tail -1 | cut -d ':' -f 2 | cut -d ' ' -f 1")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    docker0_ip = proc.communicate()[0].replace('\n', '')
    log.info("docker0 ip={}".format(docker0_ip))
    # simulate network
    data_plane = DataPlane(topo_device_graph, docker0_ip=docker0_ip)
    data_plane.add_manager('BB_SWITCH.2')
    data_plane.deploy_task(G_map, Gd)
    return data_plane


class Test(BaseTestCase):

    @classmethod
    def update_nw_latency(
            cls, cfgHelper, data_plane, nw_dev1, nw_dev2, new_latency,
            is_simulate):
        if is_simulate:
            # TODO: this is workaround to make docker works
            # data_plane.stop_workers(is_force=True)
            data_plane.modify_link(nw_dev1, nw_dev2, new_latency)
            # data_plane.start_workers()
            # raw_input('press any key to run cli')
            # data_plane.run_mininet_cli()
        cfgHelper.update_nw_link_latency(nw_dev1, nw_dev2, new_latency)
        cfgHelper.update_topo_device_graph()

    @classmethod
    def update_placement(cls, cfgHelper, data_plane, is_simulate):
        raw_input('press any key to find new placement')
        cfgHelper.update_task_map()
        cfgHelper.update_max_latency_log()
        if is_simulate:
            _topo, topo_device_graph, Gd, G_map = cfgHelper.get_graphs()
            data_plane.deploy_task(G_map, Gd)
            raw_input('press any key to re-deploy')
            data_plane.stop_workers()
            data_plane.start_workers()

    @classmethod
    def test(
            cls, config_name=None, is_export=True,
            is_update_map=True, is_simulate=True):
        _check_support_config(config_name)

        #Config(config_name): This reads the file and all the json data in devices, nw_devices and tasks

        cfgHelper = ConfigDataHelper(Config(config_name), is_export)

        #Task graph is generated, let us print it
        cfgHelper.init_task_graph()

        #Device graph along with links
        cfgHelper.update_topo_device_graph()


        # raw_input('Sandeep Task Graph: Press enter to continue: ')
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
        # raw_input('Sandeep Device Graph: Press enter to continue: ')
        #
        # print('*'*100)
        # print('*'*100)
        # print('Nodes in the graphs')
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



        #exit(0)
        # This is the ILP ilp_solver
        # Katie is solving for all but updating only for the unique_id=0
        cfgHelper.update_task_map()

        # This is again some ILP functionality
        cfgHelper.update_max_latency_log()

        log.info("=== start mininet ===")


        _topo, topo_device_graph, Gd, G_map = cfgHelper.get_graphs()

        #Printing the graphs which we are using in the AirSim

        raw_input('Sandeep Task Graph: Press enter to continue: ')

        print('*'*100)
        print('*'*100)
        print('Nodes in the topo_device_graph graph')
        print(list(topo_device_graph.nodes))

        print('*'*100)
        print('*'*100)
        print('Edges in the topo_device_graph graph')
        print(list(topo_device_graph.edges))

        print('*'*100)
        print('*'*100)
        print('Nodes in the Gd graph')
        print(list(Gd.nodes))

        print('*'*100)
        print('*'*100)
        print('Edges in the Gd graph')
        print(list(Gd.edges))


        print('*'*100)
        print('*'*100)
        print('Nodes in the G_map graph')
        print(list(G_map.nodes))

        print('*'*100)
        print('*'*100)
        print('Edges in the G_map graph')
        print(list(G_map.edges))



        #We are getting some graphs and then calling the _init_netsim
        data_plane = _init_netsim(topo_device_graph, Gd, G_map)
        # raw_input('press any key to start the network')
        data_plane.start(is_validate=True)

        data_plane.print_net_info()
        # raw_input('press any key to start scenario')
        log.info('=== running scenario: initial deployment ===')
        data_plane.start_workers()

        raw_input('press any key to end test')
        if is_simulate:
            data_plane.stop_workers()
            data_plane.stop()
        log.info('latency trend: {}'.format(cfgHelper.get_max_latency_log()))
