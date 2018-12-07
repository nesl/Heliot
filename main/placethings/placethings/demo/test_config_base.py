from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from placethings.config.base import device_cfg
from placethings.demo.base_test import BaseTestCase

log = logging.getLogger()

"""
network settings

  home_sw1   home_sw2  home_sw3
      |         |         |
    bb_sw1 -- bb_sw2 -- bb_sw3
      |         |         |
    bb_ap1    bb_ap2    bb_ap3
"""


def create_default_nw_inventory():
    nw_device_spec = device_cfg.DeviceSpec()

    nw_device = device_cfg.NetworkDevice('juniper_ex4300')
    nw_device.add_interface('WAN', device_cfg.NetworkInterface(
        protocol='ethernet', n_ports=24, ul_bw='1Gb',
        dl_bw='1Gb'))
    nw_device_spec.add_device(nw_device)

    nw_device = device_cfg.NetworkDevice('dlink_ac3900')
    nw_device.add_interface('LAN', device_cfg.NetworkInterface(
        protocol='wifi', n_ports=10, ul_bw='100Mb',
        dl_bw='100Mb'))
    nw_device.add_interface('WAN', device_cfg.NetworkInterface(
        protocol='ethernet', n_ports=1, ul_bw='1000Mb',
        dl_bw='1000Mb'))
    nw_device_spec.add_device(nw_device)

    nw_device = device_cfg.NetworkDevice('dlink_dgs105')
    nw_device.add_interface('LAN', device_cfg.NetworkInterface(
        protocol='ethernet', n_ports=4, ul_bw='100Mb',
        dl_bw='100Mb'))
    nw_device.add_interface('WAN', device_cfg.NetworkInterface(
        protocol='ethernet', n_ports=1, ul_bw='1000Mb',
        dl_bw='1000Mb'))
    nw_device_spec.add_device(nw_device)

    nw_device_inventory = device_cfg.DeviceInventory(nw_device_spec)
    nw_device_inventory.add_device('bb_sw1', 'juniper_ex4300')
    nw_device_inventory.add_device('bb_sw2', 'juniper_ex4300')
    nw_device_inventory.add_device('bb_sw3', 'juniper_ex4300')
    nw_device_inventory.add_device('bb_ap1', 'dlink_ac3900')
    nw_device_inventory.add_device('bb_ap2', 'dlink_ac3900')
    nw_device_inventory.add_device('bb_ap3', 'dlink_ac3900')
    nw_device_inventory.add_device('home_sw1', 'dlink_dgs105')
    nw_device_inventory.add_device('home_sw2', 'dlink_dgs105')
    nw_device_inventory.add_device('home_sw3', 'dlink_dgs105')

    return nw_device_inventory


class TestDefineNwConfig(BaseTestCase):
    @staticmethod
    def test(config_name=None, is_export=False):
        assert config_name is None

        nw_device_inventory = create_default_nw_inventory()

        nw_device_data = device_cfg.DeviceData(
            nw_device_inventory=nw_device_inventory)
        network_link = device_cfg.NetworkLink('WAN', 'WAN', 2)
        nw_device_data.add_nw_link('bb_sw1', 'bb_sw2', network_link)
        nw_device_data.add_nw_link('bb_sw2', 'bb_sw3', network_link)
        nw_device_data.add_nw_link('bb_sw1', 'bb_ap1', network_link)
        nw_device_data.add_nw_link('bb_sw2', 'bb_ap2', network_link)
        nw_device_data.add_nw_link('bb_sw3', 'bb_ap3', network_link)
        nw_device_data.add_nw_link('bb_sw1', 'home_sw1', network_link)
        nw_device_data.add_nw_link('bb_sw2', 'home_sw2', network_link)
        nw_device_data.add_nw_link('bb_sw3', 'home_sw3', network_link)

        nw_device_data.export_to_file('config_base/nw_device_data.json')


class TestDefineDeviceConfig(BaseTestCase):
    @staticmethod
    def test(config_name=None, is_export=False):
        assert config_name is None

        device_spec = device_cfg.DeviceSpec()

        device = device_cfg.Device('p3.2xlarge', 'processor')
        device.add_interface('LAN', device_cfg.NetworkInterface(
            protocol='ethernet', n_ports=1, ul_bw='10Gb',
            dl_bw='10Gb'))
        device.add_hardware(device_cfg.Hardware(
            cpu_utilization=100, gpu_utilization=100,
            disk_space='100Gb', ram_size='64Gb'))
        device_spec.add_device(device)

        device = device_cfg.Device('t3.large', 'processor')
        device.add_interface('LAN', device_cfg.NetworkInterface(
            protocol='ethernet', n_ports=1, ul_bw='400Mb',
            dl_bw='400Mb'))
        device.add_hardware(device_cfg.Hardware(
            cpu_utilization=100, gpu_utilization=0,
            disk_space='100Gb', ram_size='8Gb'))
        device_spec.add_device(device)

        device = device_cfg.Device('t3.micro', 'processor')
        device.add_interface('LAN', device_cfg.NetworkInterface(
            protocol='ethernet', n_ports=1, ul_bw='100Mb',
            dl_bw='100Mb'))
        device.add_hardware(device_cfg.Hardware(
            cpu_utilization=100, gpu_utilization=0,
            disk_space='20Gb', ram_size='1Gb'))
        device_spec.add_device(device)

        device = device_cfg.Device('phone', 'auctuator')
        device.add_interface('LAN', device_cfg.NetworkInterface(
            protocol='wifi', n_ports=1, ul_bw='600Mb',
            dl_bw='600Mb'))
        device.add_hardware(device_cfg.Hardware(
            cpu_utilization=0, gpu_utilization=0,
            disk_space='0', ram_size='0'))
        device_spec.add_device(device)

        device = device_cfg.Device('camera', 'sensor')
        device.add_interface('LAN', device_cfg.NetworkInterface(
            protocol='wifi', n_ports=1, ul_bw='600Mb',
            dl_bw='600Mb'))
        device.add_hardware(device_cfg.Hardware(
            cpu_utilization=0, gpu_utilization=0,
            disk_space='0', ram_size='0'))
        device_spec.add_device(device)

        device_inventory = device_cfg.DeviceInventory(device_spec)
        device_inventory.add_device('nuc', 't3.micro')
        device_inventory.add_device('cpu_server', 't3.large')
        device_inventory.add_device('gpu_server', 'p3.2xlarge')
        device_inventory.add_device('samsung_phone', 'phone')
        device_inventory.add_device('drone_camera', 'camera')

        nw_device_inventory = create_default_nw_inventory()
        device_data = device_cfg.DeviceData(
            nw_device_inventory=nw_device_inventory,
            device_inventory=device_inventory)
        network_link = device_cfg.NetworkLink('LAN', 'LAN', 2)

        device_data.add_device_link('gpu_server', 'home_sw1', network_link)
        device_data.add_device_link('cpu_server', 'home_sw2', network_link)
        device_data.add_device_link('nuc', 'home_sw3', network_link)
        device_data.add_device_link('samsung_phone', 'bb_ap1', network_link)
        device_data.add_device_link('drone_camera', 'bb_ap3', network_link)

        device_data.export_to_file('config_base/device_data.json')
