from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import subprocess

from placethings.demo.entity.base_client import ClientGen
from placethings.demo.utils import ConfigDataHelper
from placethings.netgen.network import ControlPlane, DataPlane


log = logging.getLogger()

"""" network settings

 GPU     CLIENT   CPU             Vision
SERVER   DISPLAY  SERVER Manager  Kit
   |       |       |       |      |
   L1      |      L2       |      |
   |       |       |       |      |
  SW1 --- SW2 --- SW3 --- SW4 -- SW5  <= BB_SWITCH.i
           |       |       |
           |       |       |
           |       |       |
          AP1     AP2     AP3  <= BB_AP.i

Drone1 ====flying path================>
Drone2 (standby)

Latency:
  all wired link: 2 ms
  except AP -> SW: 30 ms

Scenrios:
(1) all links alive
(2) L1 died: Latency +5000, L2 okay
(3) L2 died: Latency +5000, L1 okay

""""

class MininetContorller(object):
    @staticmethod
    def _init_netsim(topo_device_graph, Gd, G_map):
        # simulate network
        control_plane = ControlPlane(topo_device_graph)
        control_plane.add_manager('BB_SWITCH.4')
        control_plane.deploy_agent()
        # control_plane.runAgent()
        data_plane = DataPlane(topo_device_graph)
        data_plane.add_manager('BB_SWITCH.4')
        data_plane.deploy_task(G_map, Gd)
        return control_plane, data_plane

    @staticmethod
    def _simulate(topo_device_graph, Gd, G_map):
        control_plane, data_plane = _init_netsim(topo_device_graph, Gd, G_map)
        data_plane.start(is_validate=True)
        time.sleep(30)
        data_plane.stop()

# TODO: finish this part


class RPCServer(object):

    def __init__(self, name):
        self.name = name
        log.info('start mininet RPCServer: {}'.format(self.name))


    def start_prog(self, prog_name, cmd):
        log.info('try to start prog: {}'.format(prog_name))
        if prog_name in self.proc_dict:
            log.warning('prog is already running: {}'.format(prog_name))
            return 'prog is already running: {}'.format(prog_name)
        log.info('run cmd in shell: {}'.format(cmd))
        proc = subprocess.Popen(cmd, shell=True)
        self.proc_dict[prog_name] = proc
        log.info('prog is running: {}, pid={}'.format(prog_name, proc.pid))
        return 'prog started successfully: {}'.format(prog_name)

    def stop_prog(self, prog_name):
        log.info('try to stop prog: {}'.format(prog_name))
        if prog_name not in self.proc_dict:
            log.warning('prog is not running: {}'.format(prog_name))
            return 'prog is not running: {}'.format(prog_name)
        proc = self.proc_dict[prog_name]
        log.info('stopping prog: {}, pid={}'.format(prog_name, proc.pid))
        proc.terminate()
        del self.proc_dict[prog_name]
        return 'prog stopped successfully: {}'.format(prog_name)






class TestDynamic(BaseTestCase):


    @classmethod
    def test(
            cls, config_name=None, is_export=True,
            is_update_map=False, is_simulate=False):
        cfgHelper = ConfigDataHelper(config_name, is_export)
        cfgHelper.init_task_graph()
        cfgHelper.update_topo_device_graph()
        cfgHelper.update_task_map()
        cfgHelper.update_max_latency_log()
        _topo, topo_device_graph, Gd, G_map = cfgHelper.get_graphs()
        if is_simulate:
            cls._simulate(topo_device_graph, Gd, G_map)
        update_id = 0
        log.info('=== update round {} ==='.format(update_id))
        dev = 'PHONE.0'
        nw_dev = 'BB_AP.0'
        new_nw_dev = 'HOME_IOTGW.0'
        new_latency = Unit.ms(3)
        cfgHelper.update_dev_link(dev, nw_dev, new_nw_dev, new_latency)
        cfgHelper.update_topo_device_graph()
        if is_update_map:
            cfgHelper.update_task_map()
        cfgHelper.update_max_latency_log()
        _topo, topo_device_graph, Gd, G_map = cfgHelper.get_graphs()
        if is_simulate:
            cls._simulate(topo_device_graph, Gd, G_map)
        # update device graph
        update_id += 1
        log.info('=== update round {} ==='.format(update_id))
        nw_dev1 = 'BB_SWITCH.0'
        nw_dev2 = 'CLOUD_SWITCH.0'
        latency = Unit.sec(5)
        cfgHelper.update_nw_link_latency(nw_dev1, nw_dev2, latency)
        cfgHelper.update_topo_device_graph()
        if is_update_map:
            cfgHelper.update_task_map()
        cfgHelper.update_max_latency_log()
        _topo, topo_device_graph, Gd, G_map = cfgHelper.get_graphs()
        if is_simulate:
            cls._simulate(topo_device_graph, Gd, G_map)
        # update device graph
        update_id += 1
        log.info('=== update round {} ==='.format(update_id))
        dev = 'PHONE.0'
        nw_dev = 'HOME_IOTGW.0'
        new_nw_dev = 'BB_AP.0'
        new_latency = Unit.ms(3)
        cfgHelper.update_dev_link(dev, nw_dev, new_nw_dev, new_latency)
        cfgHelper.update_topo_device_graph()
        if is_update_map:
            cfgHelper.update_task_map()
        cfgHelper.update_max_latency_log()
        _topo, topo_device_graph, Gd, G_map = cfgHelper.get_graphs()
        if is_simulate:
            cls._simulate(topo_device_graph, Gd, G_map)
        log.info('latency trend: {}'.format(cfgHelper.get_max_latency_log()))
