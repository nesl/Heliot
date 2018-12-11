from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from placethings.definition import (
    Const, Device, DeviceCategory, GdInfo, Hardware, LinkInfo, LinkType,
    NwDevice, NwDeviceCategory, NwLink, Unit)


NW_DEVICE_SPEC = {
    NwDeviceCategory.HOME: {
        NwDevice.HOME_ROUTER: {
            LinkType.WAN: {
                LinkInfo.PROTOCOL: NwLink.ETHERNET,
                LinkInfo.N_LINKS: 1,
                LinkInfo.ULINK_BW: Unit.mbps(500),
                LinkInfo.DLINK_BW: Unit.mbps(500),
            },
            LinkType.LAN: {
                LinkInfo.PROTOCOL: NwLink.ETHERNET,
                LinkInfo.N_LINKS: 5,
                LinkInfo.ULINK_BW: Unit.mbps(100),
                LinkInfo.DLINK_BW: Unit.mbps(100),
            },
        },
        NwDevice.HOME_IOTGW: {
            LinkType.WAN: {
                LinkInfo.PROTOCOL: NwLink.ETHERNET,
                LinkInfo.N_LINKS: 1,
                LinkInfo.ULINK_BW: Unit.mbps(500),
                LinkInfo.DLINK_BW: Unit.mbps(500),
            },
            LinkType.LAN: {
                LinkInfo.PROTOCOL: NwLink.WIFI,
                LinkInfo.N_LINKS: 10,
                LinkInfo.ULINK_BW: Unit.mbps(50),
                LinkInfo.DLINK_BW: Unit.mbps(50),
            },
        }
    },
    NwDeviceCategory.BACKBONE: {
        NwDevice.BB_SWITCH: {
            LinkType.ANY: {
                LinkInfo.PROTOCOL: NwLink.ETHERNET,
                LinkInfo.N_LINKS: Const.INT_MAX,
                LinkInfo.ULINK_BW: Const.INT_MAX,
                LinkInfo.DLINK_BW: Const.INT_MAX,
            },
        },
        NwDevice.BB_AP: {
            LinkType.WAN: {
                LinkInfo.PROTOCOL: NwLink.ETHERNET,
                LinkInfo.N_LINKS: 1,
                LinkInfo.ULINK_BW: Const.INT_MAX,
                LinkInfo.DLINK_BW: Const.INT_MAX,
            },
            LinkType.LAN: {
                LinkInfo.PROTOCOL: NwLink.WIFI,
                LinkInfo.N_LINKS: Const.INT_MAX,
                LinkInfo.ULINK_BW: Unit.mbps(150),
                LinkInfo.DLINK_BW: Unit.mbps(50),
            },
        },
    },
    NwDeviceCategory.CLOUD: {
        NwDevice.CLOUD_SWITCH: {
            LinkType.WAN: {
                LinkInfo.PROTOCOL: NwLink.ETHERNET,
                LinkInfo.N_LINKS: 1,
                LinkInfo.ULINK_BW: Const.INT_MAX,
                LinkInfo.DLINK_BW: Const.INT_MAX,
            },
            LinkType.LAN: {
                LinkInfo.PROTOCOL: NwLink.ETHERNET,
                LinkInfo.N_LINKS: Const.INT_MAX,
                LinkInfo.ULINK_BW: Unit.mbps(400),
                LinkInfo.DLINK_BW: Unit.mbps(400),
            },
        },
    },
    NwDeviceCategory.FIELD: {
        NwDevice.FIELD_SWITCH: {
            LinkType.WAN: {
                LinkInfo.PROTOCOL: NwLink.ETHERNET,
                LinkInfo.N_LINKS: 1,
                LinkInfo.ULINK_BW: Const.INT_MAX,
                LinkInfo.DLINK_BW: Const.INT_MAX,
            },
            LinkType.LAN: {
                LinkInfo.PROTOCOL: NwLink.ETHERNET,
                LinkInfo.N_LINKS: Const.INT_MAX,
                LinkInfo.ULINK_BW: Unit.mbps(400),
                LinkInfo.DLINK_BW: Unit.mbps(400),
            },
        },
    },
}


DEVICE_SPEC = {
    DeviceCategory.ACTUATOR: {
        Device.PHONE: {
            GdInfo.COST: Unit.rph(0),
            GdInfo.HARDWARE: {},
            GdInfo.NIC: {
                LinkInfo.PROTOCOL: NwLink.WIFI,
                LinkInfo.N_LINKS: 1,
                LinkInfo.ULINK_BW: Unit.mbps(50),
                LinkInfo.DLINK_BW: Unit.mbps(150),
            },
        },
        Device.CONTROLLER: {
            GdInfo.COST: Unit.rph(0),
            GdInfo.HARDWARE: {},
            GdInfo.NIC: {
                LinkInfo.PROTOCOL: NwLink.ETHERNET,
                LinkInfo.N_LINKS: 1,
                LinkInfo.ULINK_BW: Unit.mbps(100),
                LinkInfo.DLINK_BW: Unit.mbps(100),
            },
        },
    },
    DeviceCategory.PROCESSOR: {
        Device.T2_MICRO: {
            GdInfo.COST: Unit.rph(0.0116),
            GdInfo.HARDWARE: {
                Hardware.RAM: Unit.gbyte(1),
                Hardware.HD: Unit.gbyte(30),
                Hardware.CPU: 1,
                Hardware.GPU: 0,
            },
            GdInfo.NIC: {
                LinkInfo.PROTOCOL: NwLink.ETHERNET,
                LinkInfo.N_LINKS: 1,
                LinkInfo.ULINK_BW: Unit.mbps(100),
                LinkInfo.DLINK_BW: Unit.mbps(100),
            },
        },
        Device.T3_LARGE: {
            GdInfo.COST: Unit.rph(0.0928),
            GdInfo.HARDWARE: {
                Hardware.RAM: Unit.gbyte(8),
                Hardware.HD: Unit.tbyte(16),
                Hardware.CPU: 2,
                Hardware.GPU: 0,
            },
            GdInfo.NIC: {
                LinkInfo.PROTOCOL: NwLink.ETHERNET,
                LinkInfo.N_LINKS: 1,
                LinkInfo.ULINK_BW: Unit.gbps(100),
                LinkInfo.DLINK_BW: Unit.gbps(100),
            },
        },
        Device.P3_2XLARGE: {
            GdInfo.COST: Unit.rph(3.06),
            GdInfo.HARDWARE: {
                Hardware.RAM: Unit.gbyte(16),
                Hardware.HD: Unit.tbyte(16),
                Hardware.CPU: 8,
                Hardware.GPU: 1,
            },
            GdInfo.NIC: {
                LinkInfo.PROTOCOL: NwLink.ETHERNET,
                LinkInfo.N_LINKS: 1,
                LinkInfo.ULINK_BW: Unit.gbps(10),
                LinkInfo.DLINK_BW: Unit.gbps(10),
            },
        },
    },
    DeviceCategory.SENSOR: {
        Device.SMOKE: {
            GdInfo.COST: Unit.rph(0),
            GdInfo.HARDWARE: {},
            GdInfo.NIC: {
                LinkInfo.PROTOCOL: NwLink.WIFI,
                LinkInfo.N_LINKS: 1,
                LinkInfo.ULINK_BW: Unit.mbps(10),
                LinkInfo.DLINK_BW: Unit.mbps(10),
            },
        },
        Device.CAMERA: {
            GdInfo.COST: Unit.rph(0),
            GdInfo.HARDWARE: {},
            GdInfo.NIC: {
                LinkInfo.PROTOCOL: NwLink.WIFI,
                LinkInfo.N_LINKS: 1,
                LinkInfo.ULINK_BW: Unit.mbps(60),
                LinkInfo.DLINK_BW: Unit.mbps(60),
            },
        },
    },
}
