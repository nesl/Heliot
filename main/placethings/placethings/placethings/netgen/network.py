from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future.utils import iteritems
import logging

from placethings.netgen.netmanager import NetManager
from placethings.definition import (
    GInfo, GnInfo, GdInfo, GtInfo, NwLink, NodeType, Device, DeviceCategory)


log = logging.getLogger()


_PKT_LOSS = {
    NwLink.WIFI: 0.0,
    NwLink.ETHERNET: 0.0,
}


class AddressManager(object):
    def __init__(self, net):
        self.net = net
        self.address_book = {}

    def get_address_book(self):
        return self.address_book

    def get_task_address(self, task_name, device_name):
        if task_name in self.address_book:
            _, ip, port = self.address_book[task_name]
        else:
            ip = self.net.get_device_ip(device_name)
            port = self.net.get_device_free_port(device_name)
            self.address_book[task_name] = (device_name, ip, port)
        return ip, port


class ControlPlane(object):

    _cmd_agent_template = (
        'cd {progdir} && python main_entity.py run_agent '
        '-n {name} -a {ip}:{port}')
    _cmd_stop_template = (
        'cd {progdir} && python main_entity.py stop_server -n stopper -a {ip}:{port}')
    _PROG_DIR = '/home/kumokay/github/placethings'
    _AGENT_PORT = 18800
    _MANAGER_NAME = 'Manager'

    def __init__(self, Gn):
        self.agent_dict = {}
        self.net = NetManager.create()
        for node in Gn.nodes():
            node_type = Gn.node[node][GInfo.NODE_TYPE]
            if node_type == NodeType.DEVICE:
                self.net.addHost(node)
            elif node_type == NodeType.NW_DEVICE:
                self.net.addSwitch(node)
            else:
                assert False, 'unkown node_type: {}'.format(node_type)
        for d1, d2 in Gn.edges():
            edge_info = Gn[d1][d2]
            self.net.addLink(
                d1, d2,
                bw_bps=edge_info[GnInfo.BANDWIDTH],
                delay_ms=edge_info[GnInfo.LATENCY],
                pkt_loss_rate=_PKT_LOSS[edge_info[GnInfo.PROTOCOL]])

    def get_agent_address(self, name):
        return self.net.get_device_ip(name), self._AGENT_PORT

    @staticmethod
    def get_agent_name(device_name):
        return 'A-{}'.format(device_name)

    def gen_agent_run_cmd(self, device_name, agent_name):
        ip, port = self.get_agent_address(device_name)
        cmd = self._cmd_agent_template.format(
            progdir=self._PROG_DIR,
            name=agent_name,
            ip=ip,
            port=port)
        return cmd

    def add_agent_to_host(self, host_name):
        agent_name = self.get_agent_name(host_name)
        log.info('add agent {} to host {}'.format(agent_name, host_name))
        self.agent_dict[agent_name] = self.gen_agent_run_cmd(
            host_name, agent_name)

    def deploy_agent(self):
        for host_name in self.net.get_host_list():
            self.add_agent_to_host(host_name)

    def add_manager(self, device_name):
        """
        add manager and link it to a nw device
        """
        self.net.addHost(self._MANAGER_NAME)
        self.net.addLink(
            self._MANAGER_NAME, device_name,
            bw_bps=None,
            delay_ms=0,
            pkt_loss_rate=0)

    def run_manager_cmd(self, command):
        return self.net.run_cmd(self._MANAGER_NAME, command, async=False)

    def run_agent(self, name):
        log.info('run agent: {}'.format(name))
        run_worker_cmd = self.worker_dict[name]
        self.net.run_cmd(name, run_worker_cmd, async=True)

    def stop_agent(self, name):
        log.info('stop worker: {}'.format(name))
        ip, port = self.get_agent_address(name)
        command = self._cmd_stop_template.format(
            progdir=self._PROG_DIR,
            ip=ip,
            port=port)
        self.run_manager_cmd(command, async=True)

    def start(self):
        log.info('start control plane. run all agents')
        for name in self.agent_dict:
            self.run_agent(name)

    def stop(self):
        log.info('stop control plane. stop all agents')
        for name in self.agent_dict:
            self.stop_agent(name)


class DataPlane(object):
    _cmd_get_ip = (
        "ip -4 -o addr show dev eth0| awk '{split($4,a,\"/\");print a[1]}'")
    _PROG_DIR = '/opt/github/placethings'
    _TASK_PORT = 18800
    _MANAGER_NAME = 'Manager'
    _cmd_stop_template = (
        'cd {progdir} && python main_entity.py stop_server '
        '-n stopper -a {ip}:{port}')

    def __init__(self, topo_device_graph, docker0_ip='172.18.0.1'):
        self.worker_dict = {}  # worker_name: start_cmd
        self.task_cmd = {}
        self.net = NetManager.create(docker0_ip)
        # add nw devices
        for node in topo_device_graph.nodes():
            node_info = topo_device_graph.node[node]
            node_type = node_info[GInfo.NODE_TYPE]
            if node_type == NodeType.DEVICE:
                log.info('add device: {}, info={}'.format(node, node_info))
                self.net.addHost(node)
            elif node_type == NodeType.NW_DEVICE:
                log.info('add nw_device: {}, info={}'.format(node, node_info))
                self.net.addSwitch(node)
        for d1, d2 in topo_device_graph.edges():
            print('edge: {},{}'.format(d1, d2))
            edge_info = topo_device_graph[d1][d2]
            self.net.addLink(
                d1, d2,
                bw_bps=edge_info[GnInfo.BANDWIDTH],
                delay_ms=edge_info[GnInfo.LATENCY],
                pkt_loss_rate=_PKT_LOSS[edge_info[GnInfo.PROTOCOL]])
        self.net.print_net_info()

    def print_net_info(self):
        self.net.print_net_info()

    def run_mininet_cli(self):
        self.net.run_cli()

    def modify_link(self, src, dst, delay_ms):
        self.net.modifyLinkDelay(src, dst, delay_ms)

    def add_manager(self, device_name):
        self.net.addHost(self._MANAGER_NAME)
        self.net.addLink(
            self._MANAGER_NAME, device_name,
            bw_bps=None,
            delay_ms=0,
            pkt_loss_rate=0)

    def run_manager_cmd(self, command, async=False):
        return self.net.run_cmd(self._MANAGER_NAME, command, async=async)

    def get_worker_address(self, device_name):
        return self.net.get_device_ip(device_name), self._TASK_PORT

    def get_worker_public_addr(self, device_name):
        return self.net.get_device_docker_ip(device_name), self._TASK_PORT

    @staticmethod
    def _get_next_task(G_map, task_name):
        next_task_list = list(G_map.successors(task_name))
        if not next_task_list:
            return None
        assert len(next_task_list) == 1, 'support 1 successor now'
        next_task = next_task_list[0]
        return next_task

    def deploy_task(self, G_map, Gd):
        # gen info
        progdir = self._PROG_DIR
        for task_name in G_map.nodes():
            device_name = G_map.node[task_name][GtInfo.CUR_DEVICE]
            log.info('deploy {} to {}'.format(task_name, device_name))
            ip, port = self.get_worker_address(device_name)
            docker_ip, docker_port = self.get_worker_public_addr(device_name)
            device_cat = Gd.node[device_name][GdInfo.DEVICE_CAT]
            # device_type = Gd.node[device_name][GdInfo.DEVICE_TYPE]
            # exectime = G_map.node[task_name][GtInfo.CUR_LATENCY]
            next_task = self._get_next_task(G_map, task_name)
            if not next_task:
                assert device_cat == DeviceCategory.ACTUATOR
                next_ip, next_port = None, None
            else:
                next_device_name = G_map.node[next_task][GtInfo.CUR_DEVICE]
                next_ip, next_port = self.get_worker_address(next_device_name)

            cmd_template_dict = G_map.node[task_name][GtInfo.EXEC_CMD]
            print(cmd_template_dict)
            print(device_name)
            if device_name in cmd_template_dict:
                cmd_template = cmd_template_dict[device_name]
            else:
                cmd_template = cmd_template_dict['default']

            cmd = cmd_template.format(
                progdir=progdir,
                self_addr='{}:{}'.format(ip, port),
                docker_addr='{}:{}'.format(docker_ip, docker_port),
                next_addr='{}:{}'.format(next_ip, next_port))
            self.worker_dict[device_name] = cmd

    def run_worker(self, device_name):
        log.info('run worker on {}'.format(device_name))
        run_worker_cmd = self.worker_dict[device_name]
        self.net.run_cmd(device_name, run_worker_cmd, async=False)

    def stop_worker(self, device_name, is_force=False):
        if not is_force:
            log.info('stop {}'.format(device_name))
            ip, port = self.get_worker_address(device_name)
            command = self._cmd_stop_template.format(
                progdir=self._PROG_DIR,
                name=self._MANAGER_NAME,
                ip=ip,
                port=port)
            # check connectivity
            ret = self.run_manager_cmd('ping {} -c 1'.format(ip))
            if '0% packet loss' in ret:
                # stop server
                self.run_manager_cmd(command)
                return
        log.debug('kill task on {}'.format(device_name))
        # TODO: this is workaround
        self.net.run_cmd(device_name, 'kill %python', async=False)

    def start(self, is_validate=False):
        log.info('start mininet.')
        self.net.start()
        if is_validate:
            self.net.validate()

    def start_workers(self):
        log.info('run all workers')
        for device_name in self.worker_dict:
            self.run_worker(device_name)

    def stop_workers(self, is_force=False):
        log.info('stop all workers')
        for device_name in self.worker_dict:
            self.stop_worker(device_name, is_force=is_force)

    def stop(self):
        log.info('stop mininet.')
        self.net.stop()


class NetGen(object):

    _PKT_LOSS = {
        NwLink.WIFI: 0.0,
        NwLink.ETHERNET: 0.0,
    }

    @classmethod
    def create_control_plane(cls, Gn):
        """
        Create an empty network and add nodes to it.

        Args:
            Gn (nx.DiGraph): topo_device_graph
        Returns:
            net (NetManager): a network of switches and devices
        """
        return cls.create(Gn)

    def create_data_plane(cls, Gn):
        """
        Args:
            Gn (nx.DiGraph): topo_device_graph
        Returns:
            net (NetManager): a network of all switches
        """
        net = NetManager.create()
        for node in Gn.nodes():
            node_type = Gn.node[node][GInfo.NODE_TYPE]
            if node_type == NodeType.DEVICE:
                net.addSwitch(node)
            elif node_type == NodeType.NW_DEVICE:
                net.addSwitch(node)
            else:
                assert False, 'unkown node_type: {}'.format(node_type)
        for d1, d2 in Gn.edges():
            edge_info = Gn[d1][d2]
            net.addLink(
                d1, d2,
                bw_bps=edge_info[GnInfo.BANDWIDTH],
                delay_ms=edge_info[GnInfo.LATENCY],
                pkt_loss_rate=cls._PKT_LOSS[edge_info[GnInfo.PROTOCOL]])
        return net

    @classmethod
    def create(cls, Gn):
        """
        Create an empty network and add nodes to it.

        Args:
            Gn (nx.DiGraph): topo_device_graph
        Returns:
            net (NetManager)
        """
        net = NetManager.create()
        for node in Gn.nodes():
            node_type = Gn.node[node][GInfo.NODE_TYPE]
            if node_type == NodeType.DEVICE:
                net.addHost(node)
            elif node_type == NodeType.NW_DEVICE:
                net.addSwitch(node)
            else:
                assert False, 'unkown node_type: {}'.format(node_type)
        for d1, d2 in Gn.edges():
            edge_info = Gn[d1][d2]
            net.addLink(
                d1, d2,
                bw_bps=edge_info[GnInfo.BANDWIDTH],
                delay_ms=edge_info[GnInfo.LATENCY],
                pkt_loss_rate=cls._PKT_LOSS[edge_info[GnInfo.PROTOCOL]])
        return net
