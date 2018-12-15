from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from mininet.clean import cleanup
from mininet.net import Containernet
from mininet.link import TCLink
from mininet.node import Controller
from mininet.log import setLogLevel as mininet_SetLogLevel
from mininet.cli import CLI


mininet_SetLogLevel('info')
log = logging.getLogger()


class NetManager(object):
    _NEXT_IP_NUM = 100
    _NEXT_DOCKER_IP_NUM = 2
    # port on baremetal machine binds to the docker exposed port
    _NEXT_DOCKER_BINDING_PORT = 20000
    # port exposed to public in each docker container
    _DOCKER_EXPOSED_PORT = 19000
    # port exposed in mininet only for tasks communication
    _HOST_TASK_PORT = 18800
    _NEXT_HOST_ID = 0
    _NEXT_SWITCH_ID = 0
    _HOST_PREFIX = 'h'
    _SWITCH_PREFIX = 's'

    def __init__(self, net, docker_subnet_ip, docker_img):
        if not docker_img:
            docker_img = self._DEFAULT_IMG
        self._net = net
        self._host_dict = {}
        self._host_ip_dict = {}  # assigned host ip
        self._host_port_dict = {}  # exposed host port
        self._docker_subnet_prefix = '.'.join(docker_subnet_ip.split('.')[:3])
        self._docker_img = docker_img
        self._mininet_subnet_prefix = '10.0.0'
        self._host_docker_ip_dict = {}
        self._host_docker_port_dict = {}
        self._host_docker_binding_port_dict = {}
        self._switch_dict = {}
        self._edge_dict = {}
        self._edge_info_dict = {}
        self._devNameToNodeName = {}

    def print_net_info(self):
        for dev in self._switch_dict:
            log.info('dev={}, v_dev={}'.format(
                dev, self._devNameToNodeName[dev]))
        for edge in self._edge_dict:
            log.info('link={}, config={}'.format(
                edge, self._edge_info_dict[edge]))
        for dev in self._host_dict:
            log.info(
                'dev={}<->{}, ip={}:{}, docker={}:{}<->localhost:{}'.format(
                    dev, self._devNameToNodeName[dev], self._host_ip_dict[dev],
                    self._host_port_dict[dev], self._host_docker_ip_dict[dev],
                    self._host_docker_port_dict[dev],
                    self._host_docker_binding_port_dict[dev]))

    @classmethod
    def create(cls, docker0_ip, docker_img):
        raw_net = Containernet(controller=Controller, link=TCLink)
        log.info('create mininet wtih default controller')
        raw_net.addController('c0')
        return cls(raw_net, docker0_ip, docker_img)

    def _new_address(self):
        ip = '{}.{}'.format(
            self._mininet_subnet_prefix, self._NEXT_IP_NUM)
        docker_ip = '{}.{}'.format(
            self._docker_subnet_prefix, self._NEXT_DOCKER_IP_NUM)
        docker_port = self._NEXT_DOCKER_BINDING_PORT
        self._NEXT_IP_NUM += 1
        self._NEXT_DOCKER_IP_NUM += 1
        self._NEXT_DOCKER_BINDING_PORT += 1
        assert self._NEXT_IP_NUM < 256
        assert self._NEXT_DOCKER_IP_NUM < 256
        return ip, docker_ip, docker_port

    @classmethod
    def _new_host_name(cls):
        name = '{}{}'.format(cls._HOST_PREFIX, cls._NEXT_HOST_ID)
        cls._NEXT_HOST_ID += 1
        return name

    @classmethod
    def _new_switch_name(cls):
        name = '{}{}'.format(cls._SWITCH_PREFIX, cls._NEXT_SWITCH_ID)
        cls._NEXT_SWITCH_ID += 1
        return name

    def addHost(self, device_name):
        # auto generate name bc name cannot be too long =.=
        name = self._new_host_name()
        # TODO: use cmd to get correct docker ip
        ip, docker_ip, docker_port = self._new_address()
        host = self._net.addDocker(
            name, ip=ip, dimage=self._docker_img,
            ports=[self._DOCKER_EXPOSED_PORT],
            port_bindings={self._DOCKER_EXPOSED_PORT: docker_port})
        self._host_dict[device_name] = host
        self._host_ip_dict[device_name] = ip
        self._host_port_dict[device_name] = self._HOST_TASK_PORT
        self._host_docker_ip_dict[device_name] = docker_ip
        self._host_docker_port_dict[device_name] = self._DOCKER_EXPOSED_PORT
        self._host_docker_binding_port_dict[device_name] = docker_port
        self._devNameToNodeName[device_name] = name
        log.debug('add host {}'.format(device_name))

    def addSwitch(self, device_name):
        name = self._new_switch_name()
        switch = self._net.addSwitch(name)
        self._switch_dict[device_name] = switch
        self._devNameToNodeName[device_name] = name
        log.debug('add switch {}'.format(device_name))

    def addLink(
            self, src, dst, bw_bps=None, delay_ms=1, jitter_ms=0,
            max_queue_size=None, pkt_loss_rate=None):
        if (dst, src) in self._edge_dict:
            # mininet is not DiGraph! everything is bidirectional
            return
        # mininet bandwidth supported range 0..1000
        if bw_bps is None:
            bw_mbps = None
        else:
            bw_mbps = None if bw_bps > 1000000 else int(bw_bps / 1000000)
        delay = '{}ms'.format(delay_ms)
        jitter = '{}ms'.format(jitter_ms)
        loss = int(pkt_loss_rate * 100) if pkt_loss_rate else None
        # TODO: fix this
        # if (('AP' in src or 'AP' in dst) and ('CAM' in src or 'CAM' in dst)):
        #    jitter = '5ms'
        link = self._net.addLink(
            self._devNameToNodeName[src], self._devNameToNodeName[dst],
            bw=bw_mbps, delay=delay, jitter=jitter,
            max_queue_size=max_queue_size, loss=loss)
        self._edge_dict[(src, dst)] = link
        self._edge_info_dict[(src, dst)] = dict(
            delay_ms=delay_ms, bw_bps=bw_bps)
        log.debug('link {} <-> {}: {}'.format(
            src, dst, self._edge_info_dict[(src, dst)]))

    def delLink(self, src, dst):
        if (src, dst) in self._edge_dict:
            assert (dst, src) not in self._edge_dict
            self._net.removeLink(
                node1=self._devNameToNodeName[src],
                node2=self._devNameToNodeName[dst])
            del self._edge_dict[(src, dst)]
            del self._edge_info_dict[(src, dst)]
        elif (dst, src) in self._edge_dict:
            self._net.removeLink(
                node1=self._devNameToNodeName[dst],
                node2=self._devNameToNodeName[src])
            del self._edge_dict[(dst, src)]
            del self._edge_info_dict[(src, dst)]
        log.debug('delete link {} <-> {}'.format(src, dst))

    def modifyLinkAttribute(self, src, dst, delay_ms=None, bw_bps=None):
        edge = (src, dst)
        if edge not in self._edge_dict:
            edge = (dst, src)
            assert edge in self._edge_dict
        link = self._edge_dict[edge]
        if delay_ms is None:
            delay_ms = self._edge_info_dict[edge]['delay_ms']
        if bw_bps is None:
            bw_bps = self._edge_info_dict[edge]['bw_bps']
        delay = '{}ms'.format(delay_ms // 2)
        link.intf1.config(delay=delay, bw_bps=bw_bps)
        link.intf2.config(delay=delay, bw_bps=bw_bps)
        self._edge_info_dict[edge] = dict(delay_ms=delay_ms, bw_bps=bw_bps)
        log.debug('link {} <-> {}: {}'.format(
            edge[0], edge[1], self._edge_info_dict[edge]))

    def modifyLink(
            self, src, dst, new_dst=None, bw_bps=None, delay_ms=1,
            max_queue_size=None, pkt_loss_rate=None):
        assert False, 'not implemented'

    def start(self):
        log.info('*** Starting network')
        self._net.start()

    def run_cli(self):
        CLI(self._net)

    def stop(self):
        log.info('*** Stopping network')
        self._net.stop()
        # TODO: this is a hotfix. should stop hosts properly
        cleanup()

    def run_cmd(self, device_name, command, is_async=False):
        host = self._host_dict[device_name]
        log.info('send command to {}({}): {}'.format(
            device_name, host, command))
        if is_async:
            # no waiting
            host.sendCmd(command)
            output = 'command sent'
        else:
            output = host.cmd(command)
        log.info('output: {}'.format(output))
        return output

    def get_device_ip(self, device_name):
        ip = self._host_ip_dict[device_name]
        # ip = self._host_dict[device_name].IP()
        assert ip is not None, 'host={}, ip={}'.format(device_name, ip)
        return ip

    def get_device_docker_ip(self, device_name):
        ip = self._host_docker_ip_dict[device_name]
        # ip = self._host_dict[device_name].IP()
        assert ip is not None, 'host={}, docker_ip={}'.format(device_name, ip)
        return ip

    def validate(self):
        log.info('*** Validate network')
        for h1 in self._host_dict:
            for h2 in self._host_dict:
                if h1 == h2:
                    continue
                output = self.run_cmd(
                    h1, 'ping {} -c 1'.format(self._host_dict[h2].IP()))
                assert ' 0% packet loss' in output, output
        log.info('ping all success!')
