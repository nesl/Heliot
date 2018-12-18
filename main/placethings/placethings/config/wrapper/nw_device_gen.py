from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future.utils import iteritems

from placethings.config.definition.common_def import NwDevice, NwDeviceCategory, GnInfo, LinkType
from placethings.config.definition import spec_def
from placethings.utils import json_utils


class NwDeviceInventory(object):
    """ wrapper for
        NW_DEVICE_INVENTORY = {
            NwDeviceCategory.HOME: {
                NwDevice.HOME_ROUTER: 1,
                NwDevice.HOME_IOTGW: 1,
            },
            NwDeviceCategory.BACKBONE: {
                NwDevice.BB_SWITCH: 1,
                NwDevice.BB_AP: 1,
            },
            NwDeviceCategory.CLOUD: {
                NwDevice.CLOUD_SWITCH: 1,
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

    def add_item(self, nw_device_category, nw_device, num):
        """
        args:
            nw_device_category (NwDeviceCategory): e.g. NwDeviceCategory.HOME
            nw_device (NwDevice): e.g. NwDeviceCategory.BACKBONE
            num (int): how many devices
        """
        assert type(nw_device_category) is NwDeviceCategory
        assert type(nw_device) is NwDevice
        if nw_device_category not in self.data:
            self.data[nw_device_category] = {}
        assert nw_device not in self.data[nw_device_category]
        self.data[nw_device_category][nw_device] = num


class NwLinks(object):
    """ wrapper for
        NW_LINKS = {
            'HOME_IOTGW.0 -> HOME_ROUTER.0': {
                GnInfo.SRC_LINK_TYPE: LinkType.WAN,
                GnInfo.DST_LINK_TYPE: LinkType.LAN,
                GnInfo.LATENCY: Unit.ms(1),
            },
            'HOME_ROUTER.0 -> HOME_IOTGW.0': {
                GnInfo.SRC_LINK_TYPE: LinkType.LAN,
                GnInfo.DST_LINK_TYPE: LinkType.WAN,
                GnInfo.LATENCY: Unit.ms(1),
            },
            ...
            'CLOUD_SWITCH.0 -> BB_SWITCH.0': {
                GnInfo.SRC_LINK_TYPE: LinkType.WAN,
                GnInfo.DST_LINK_TYPE: LinkType.ANY,
                GnInfo.LATENCY: Unit.ms(15),
            },
            'BB_SWITCH.0 -> CLOUD_SWITCH.0': {
                GnInfo.SRC_LINK_TYPE: LinkType.ANY,
                GnInfo.DST_LINK_TYPE: LinkType.WAN,
                GnInfo.LATENCY: Unit.ms(15),
            }
        }
    """
    def __init__(self, data=None):
        if not data:
            data = {}
        self.data = data

    def add_item(
            self, src, dst, src_link_type, dst_link_type, latency,
            nw_device_list):
        """
        only support balanced link.
        args:
            src, dst (str)
            src_link_type, dst_link_type (LinkType)
            latency (int)
            nw_devic_list (list)
        """
        assert src in nw_device_list
        assert dst in nw_device_list
        assert type(src_link_type) is LinkType
        assert type(dst_link_type) is LinkType
        assert type(latency) is int

        link_name = '{} -> {}'.format(src, dst)
        assert link_name not in self.data
        self.data[link_name] = {
            GnInfo.SRC_LINK_TYPE: src_link_type,
            GnInfo.DST_LINK_TYPE: dst_link_type,
            GnInfo.LATENCY: latency,
        }

        link_name = '{} -> {}'.format(dst, src)
        assert link_name not in self.data
        self.data[link_name] = {
            GnInfo.SRC_LINK_TYPE: dst_link_type,
            GnInfo.DST_LINK_TYPE: src_link_type,
            GnInfo.LATENCY: latency,
        }


class NwDeviceSpec(object):
    def __init__(self, data=None):
        if not data:
            data = {}
        self.data = data


class AllNwDeviceData(object):
    def __init__(self, filepath=None):
        if not filepath:
            self.nw_device_spec = NwDeviceSpec(data=spec_def.NW_DEVICE_SPEC)
            self.nw_device_inventory = NwDeviceInventory()
            self.nw_device_links = NwLinks()
        else:
            filemap = json_utils.import_bundle(filepath)
            self.nw_device_spec = NwDeviceSpec(data=filemap['device_spec'])
            self.nw_device_inventory = NwDeviceInventory(
                data=filemap['device_inventory'])
            self.nw_device_links = NwLinks(data=filemap['links'])

    def export_data(self, filepath):
        filemap = dict(
            device_spec=self.nw_device_spec.data,
            device_inventory=self.nw_device_inventory.data,
            links=self.nw_device_links.data)
        json_utils.export_bundle(filepath, filemap)

    def add_nw_device(self, nw_device_category, nw_device, num):
        self.nw_device_inventory.add_item(nw_device_category, nw_device, num)

    def add_nw_dev_link(self, src, dst, src_link_type, dst_link_type, latency):
        nw_device_list = self.nw_device_inventory.get_device_list()
        self.nw_device_links.add_item(
            src, dst, src_link_type, dst_link_type, latency, nw_device_list)
