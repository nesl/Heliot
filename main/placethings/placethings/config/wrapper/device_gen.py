from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


from future.utils import iteritems

from placethings.definition import Device, DeviceCategory, GnInfo
from placethings.config import spec_def
from placethings.utils import json_utils


class DeviceInventory:
    """ wrapper for
        DEVICE_INVENTORY = {
            DeviceCategory.ACTUATOR: {
                Device.PHONE: 1,
            },
            DeviceCategory.PROCESSOR: {
                Device.T2_MICRO: 2,
                Device.T3_LARGE: 2,
                Device.P3_2XLARGE: 1,
            },
            DeviceCategory.SENSOR: {
                Device.SMOKE: 1,
                Device.CAMERA: 1,
            },
        }
    """
    def __init__(self, data=None):
        if not data:
            data = {}
        self.data = data

    def get_device_list(self):
        device_list = []
        for cat, cat_data in iteritems(self.data):
            for dev_type, dev_cnt in iteritems(cat_data):
                for i in range(dev_cnt):
                    _classname, dev_type_short = str(dev_type).split('.')
                    dev_name = '{}.{}'.format(dev_type_short, i)
                    device_list.append(dev_name)
        return device_list

    def add_item(self, device_category, device, num):
        """
        args:
            device_category (DeviceCategory): e.g. DeviceCategory.PROCESSOR
            device (Device): e.g. Device.T2_MICRO
            num (int): how many devices
        """
        assert type(device_category) is DeviceCategory
        assert type(device) is Device
        if device_category not in self.data:
            self.data[device_category] = {}
        assert device not in self.data[device_category]
        self.data[device_category][device] = num


class DeviceLinks:
    """ a wrapper for
        DEVICE_LINKS = {
            'SMOKE.0 -> HOME_IOTGW.0': {
                GnInfo.LATENCY: Unit.ms(3),
            },
            'CAMERA.0 -> HOME_IOTGW.0': {
                GnInfo.LATENCY: Unit.ms(3),
            },
            ...
            'PHONE.0 -> BB_AP.0': {
                GnInfo.LATENCY: Unit.ms(10),
            },
            'BB_AP.0 -> PHONE.0': {
                GnInfo.LATENCY: Unit.ms(10),
            },
        }
        """
    def __init__(self, data=None):
        if not data:
            data = {}
        self.data = data

    def add_item(self, dev, nw_dev, latency, device_list, nw_device_list):
        """
        only support balanced link.
        args:
            dev, nw_dev (str)
            latency (int)
            device_list, nw_device_list (list)
        """
        assert dev in device_list
        assert nw_dev in nw_device_list
        assert type(latency) is int

        link_name = '{} -> {}'.format(dev, nw_dev)
        assert link_name not in self.data
        self.data[link_name] = {
            GnInfo.LATENCY: latency,
        }

        link_name = '{} -> {}'.format(nw_dev, dev)
        assert link_name not in self.data
        self.data[link_name] = {
            GnInfo.LATENCY: latency,
        }


class DeviceSpec(object):
    def __init__(self, data=None):
        if not data:
            data = {}
        self.data = data


class AllDeviceData(object):
    def __init__(self, filepath=None):
        if not filepath:
            self.device_spec = DeviceSpec(data=spec_def.DEVICE_SPEC)
            self.device_inventory = DeviceInventory()
            self.device_links = DeviceLinks()
        else:
            filemap = json_utils.import_bundle(filepath)
            self.device_spec = DeviceSpec(data=filemap['device_spec'])
            self.device_inventory = DeviceInventory(
                data=filemap['device_inventory'])
            self.device_links = DeviceLinks(data=filemap['links'])

    def export_data(self, filepath):
        filemap = dict(
            device_spec=self.device_spec.data,
            device_inventory=self.device_inventory.data,
            links=self.device_links.data)
        json_utils.export_bundle(filepath, filemap)

    def add_device(self, device_category, device, num):
        self.device_inventory.add_item(device_category, device, num)

    def add_dev_link(self, dev, nw_dev, latency, nw_dev_list):
        device_list = self.device_inventory.get_device_list()
        self.device_links.add_item(
            dev, nw_dev, latency, device_list, nw_dev_list)
