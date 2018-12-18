from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from placethings.config.wrapper.config_gen import Config
from placethings.config.wrapper.task_gen import TaskFlavor
from placethings.demo.base_test import BaseTestCase
from placethings.config.definition.common_def import (
    Device, DeviceCategory, Flavor, Hardware, NwDevice, NwDeviceCategory,
    LinkType, Unit)

log = logging.getLogger()

"""
network settings

CONTROLLER.0   P3_2XLARGE.0     T3_LARGE.0
       |         |                 |
CLOUD_SWITCH.1 CLOUD_SWITCH.0  FIELD_SWITCH.1   (manager)      T2_MICRO.0
        |       |                 |                 |               |
      BB_SWITCH.0 --------- BB_SWITCH.1 ---- BB_SWITCH.2 ----FIELD_SWITCH.0
        |                    |                 |
     BB_AP.0               BB_AP.1         BB_AP.2
        |
     CAMERA.0
"""


def compare_cfg(cfg, cfg2):
    assert(
        cfg.all_device_data.device_spec.data
        == cfg2.all_device_data.device_spec.data)
    assert(
        cfg.all_device_data.device_inventory.data
        == cfg2.all_device_data.device_inventory.data)
    assert(
        cfg.all_device_data.device_links.data
        == cfg2.all_device_data.device_links.data)

    assert(
        cfg.all_nw_device_data.nw_device_spec.data
        == cfg2.all_nw_device_data.nw_device_spec.data)
    assert(
        cfg.all_nw_device_data.nw_device_inventory.data
        == cfg2.all_nw_device_data.nw_device_inventory.data)
    assert(
        cfg.all_nw_device_data.nw_device_links.data
        == cfg2.all_nw_device_data.nw_device_links.data)

    assert(
        cfg.all_task_data.task_info.data
        == cfg2.all_task_data.task_info.data)
    assert(
        cfg.all_task_data.task_links.data
        == cfg2.all_task_data.task_links.data)
    assert(
        cfg.all_task_data.task_mapping.data
        == cfg2.all_task_data.task_mapping.data)


class TestDefineConfig(BaseTestCase):
    @staticmethod
    def test(config_name=None, is_export=False, is_interactive=True):
        if not config_name:
            config_name = 'sample_configs/config_sample'
        cfg = Config()

        cfg.add_nw_device(NwDeviceCategory.FIELD, NwDevice.FIELD_SWITCH, 2)
        cfg.add_nw_device(NwDeviceCategory.BACKBONE, NwDevice.BB_SWITCH, 3)
        cfg.add_nw_device(NwDeviceCategory.BACKBONE, NwDevice.BB_AP, 3)
        cfg.add_nw_device(NwDeviceCategory.CLOUD, NwDevice.CLOUD_SWITCH, 2)

        cfg.add_nw_dev_link(
            'CLOUD_SWITCH.1', 'BB_SWITCH.0',
            LinkType.WAN, LinkType.ANY, Unit.ms(2))
        cfg.add_nw_dev_link(
            'CLOUD_SWITCH.0', 'BB_SWITCH.0',
            LinkType.WAN, LinkType.ANY, Unit.ms(2))
        cfg.add_nw_dev_link(
            'FIELD_SWITCH.1', 'BB_SWITCH.1',
            LinkType.WAN, LinkType.ANY, Unit.ms(2))
        cfg.add_nw_dev_link(
            'FIELD_SWITCH.0', 'BB_SWITCH.2',
            LinkType.WAN, LinkType.ANY, Unit.ms(2))
        cfg.add_nw_dev_link(
            'BB_AP.0', 'BB_SWITCH.0',
            LinkType.WAN, LinkType.ANY, Unit.ms(2))
        cfg.add_nw_dev_link(
            'BB_AP.1', 'BB_SWITCH.1',
            LinkType.WAN, LinkType.ANY, Unit.ms(2))
        cfg.add_nw_dev_link(
            'BB_AP.2', 'BB_SWITCH.2',
            LinkType.WAN, LinkType.ANY, Unit.ms(2))
        cfg.add_nw_dev_link(
            'BB_SWITCH.0', 'BB_SWITCH.1',
            LinkType.ANY, LinkType.ANY, Unit.ms(2))
        cfg.add_nw_dev_link(
            'BB_SWITCH.1', 'BB_SWITCH.2',
            LinkType.ANY, LinkType.ANY, Unit.ms(2))

        cfg.add_device(DeviceCategory.SENSOR, Device.CAMERA, 1)
        cfg.add_device(DeviceCategory.PROCESSOR, Device.P3_2XLARGE, 1)
        cfg.add_device(DeviceCategory.PROCESSOR, Device.T3_LARGE, 1)
        cfg.add_device(DeviceCategory.PROCESSOR, Device.T2_MICRO, 1)
        cfg.add_device(DeviceCategory.ACTUATOR, Device.CONTROLLER, 1)

        cfg.add_dev_link('CAMERA.0', 'BB_AP.0', Unit.ms(30))
        cfg.add_dev_link('P3_2XLARGE.0', 'CLOUD_SWITCH.0', Unit.ms(2))
        cfg.add_dev_link('T3_LARGE.0', 'FIELD_SWITCH.1', Unit.ms(2))
        cfg.add_dev_link('T2_MICRO.0', 'FIELD_SWITCH.0', Unit.ms(2))
        cfg.add_dev_link('CONTROLLER.0', 'CLOUD_SWITCH.1', Unit.ms(2))

        cfg.add_task('task_takePic')
        cfg.add_task('task_findObj')
        cfg.add_task('task_notify')
        cfg.add_task_link('task_takePic', 'task_findObj', Unit.mbyte(12))
        cfg.add_task_link('task_findObj', 'task_notify', Unit.byte(10))

        flavor = TaskFlavor(Flavor.CPU)
        flavor.add_requirement(Hardware.RAM, Unit.gbyte(1))
        flavor.add_requirement(Hardware.HD, Unit.mbyte(30))
        flavor.add_requirement(Hardware.GPU, Unit.percentage(0))
        flavor.add_requirement(Hardware.CPU, Unit.percentage(60))
        flavor.add_latency_info(Device.T2_MICRO, Unit.sec(6))
        flavor.add_latency_info(Device.T3_LARGE, Unit.sec(2))
        flavor.add_latency_info(Device.P3_2XLARGE, Unit.ms(600))
        cfg.add_task_flavor('task_findObj', flavor)

        flavor = TaskFlavor(Flavor.GPU)
        flavor.add_requirement(Hardware.RAM, Unit.gbyte(4))
        flavor.add_requirement(Hardware.HD, Unit.mbyte(30))
        flavor.add_requirement(Hardware.GPU, Unit.percentage(60))
        flavor.add_requirement(Hardware.CPU, Unit.percentage(5))
        flavor.add_latency_info(Device.P3_2XLARGE, Unit.ms(20))
        cfg.add_task_flavor('task_findObj', flavor)

        cfg.add_task_mapping('task_takePic', 'CAMERA.0')
        cfg.add_task_mapping('task_notify', 'CONTROLLER.0')

        cfg.export_data(config_name)
        cfg2 = Config(folderpath=config_name)
        compare_cfg(cfg, cfg2)
