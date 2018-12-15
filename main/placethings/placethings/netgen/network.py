from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import subprocess

from placethings.netgen.netmanager import NetManager
from placethings.config.definition.common_def import (
    GInfo, GnInfo, GdInfo, GtInfo, NodeType, DeviceCategory)


log = logging.getLogger()


def init_netsim(
        Gnd, G_map, manager_attached_nw_device, docker_img=None,
        prog_dir=None, use_assigned_latency=True):
    # get containernet (docker) subnet ip
    # This will be there is containernet is installed, which install the docker
    cmd = (
        "ifconfig | grep -A 1 'docker'"
        " | tail -1 | cut -d ':' -f 2 | cut -d ' ' -f 1")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    docker0_ip = proc.communicate()[0].replace('\n', '')
    log.info("docker0 ip={}, docker_img={}".format(docker0_ip, docker_img))
    # simulate network
    data_plane = DataPlane(
        Gnd, docker0_ip=docker0_ip, docker_img=docker_img,
        prog_dir=prog_dir, use_assigned_latency=use_assigned_latency)
    # attach manager to a nw device, e.g. 'BB_SWITCH.2'
    data_plane.add_manager(manager_attached_nw_device)
    data_plane.deploy_task(G_map, Gnd)
    return data_plane


class DataPlane(object):
    # Dataplane is used for creating the network
    _cmd_get_ip = (
        "ip -4 -o addr show dev eth0| awk '{split($4,a,\"/\");print a[1]}'")
    _DOCKER_IMG = 'kumokay/heliot_host:v1'
    _DOCKER_IP = '172.18.0.1'
    _PROG_DIR = '/opt/github/placethings'
    _TASK_PORT = 18800
    _PUBLIC_PORT = 19000
    _MANAGER_NAME = 'Manager'
    _cmd_stop_template = (
        'cd {progdir} && python main_entity.py stop_server '
        '-n stopper -a {ip}:{port}')

    def __init__(
            self, topo_device_graph, docker0_ip=None, docker_img=None,
            prog_dir=None, use_assigned_latency=True):
        if not docker0_ip:
            docker0_ip = self._DOCKER_IP
        if not docker_img:
            docker_img = self._DOCKER_IMG
        if not prog_dir:
            prog_dir = self._PROG_DIR
        self.worker_dict = {}  # worker_name: start_cmd
        self.task_cmd = {}
        self.prog_dir = prog_dir
        self.use_assigned_latency = use_assigned_latency

        # This is the controller which we are creating
        self.net = NetManager.create(docker0_ip, docker_img)
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
            if self.use_assigned_latency:
                delay_ms = edge_info[GnInfo.LATENCY]
            else:
                speed_of_light = 299792458
                delay_ms = int(edge_info[GnInfo.DISTANCE] / speed_of_light)
            self.net.addLink(
                d1, d2, bw_bps=edge_info[GnInfo.BANDWIDTH], delay_ms=delay_ms)
        self.net.print_net_info()

    def print_net_info(self):
        self.net.print_net_info()

    def run_mininet_cli(self):
        self.net.run_cli()

    def modify_link(self, src, dst, delay_ms=None, bw_bps=None):
        self.net.modifyLinkAttribute(
            src, dst, delay_ms=delay_ms, bw_bps=bw_bps)

    def add_manager(self, device_name):
        self.net.addHost(self._MANAGER_NAME)
        self.net.addLink(
            self._MANAGER_NAME, device_name,
            bw_bps=None,
            delay_ms=0,
            pkt_loss_rate=0)

    def run_manager_cmd(self, command, is_async=False):
        return self.net.run_cmd(self._MANAGER_NAME, command, is_async=is_async)

    def get_worker_address(self, device_name):
        return self.net.get_device_ip(device_name), self._TASK_PORT

    def get_worker_public_addr(self, device_name):
        return self.net.get_device_docker_ip(device_name), self._PUBLIC_PORT

    @staticmethod
    def _get_next_task(G_map, task_name):
        next_task_list = list(G_map.successors(task_name))
        if not next_task_list:
            return None
        assert len(next_task_list) == 1, 'support 1 successor now'
        next_task = next_task_list[0]
        return next_task

    def deploy_task(self, G_map, Gnd):
        # gen info
        progdir = self.prog_dir
        for task_name in G_map.nodes():
            device_name = G_map.node[task_name][GtInfo.CUR_DEVICE]
            log.info('deploy {} to {}'.format(task_name, device_name))
            ip, port = self.get_worker_address(device_name)
            docker_ip, docker_port = self.get_worker_public_addr(device_name)
            device_cat = Gnd.node[device_name][GdInfo.DEVICE_CAT]
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
        self.net.run_cmd(device_name, run_worker_cmd, is_async=False)

    def stop_worker(self, device_name, is_force=False):
        if not is_force:
            log.info('stop {}'.format(device_name))
            ip, port = self.get_worker_address(device_name)
            command = self._cmd_stop_template.format(
                progdir=self.prog_dir,
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
        self.net.run_cmd(device_name, 'kill %python', is_async=False)

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
