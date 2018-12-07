from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from placethings.definition import (
    Device, DeviceCategory, Flavor, Hardware, NwDevice, NwDeviceCategory,
    GnInfo, GtInfo, LinkType, Unit)


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


# device naming rule: DeviceTypeName.ID
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
    'HOME_ROUTER.0 -> BB_SWITCH.0': {
        GnInfo.SRC_LINK_TYPE: LinkType.WAN,
        GnInfo.DST_LINK_TYPE: LinkType.ANY,
        GnInfo.LATENCY: Unit.ms(20),
    },
    'BB_SWITCH.0 -> HOME_ROUTER.0': {
        GnInfo.SRC_LINK_TYPE: LinkType.ANY,
        GnInfo.DST_LINK_TYPE: LinkType.WAN,
        GnInfo.LATENCY: Unit.ms(20),
    },
    'BB_AP.0 -> BB_SWITCH.0': {
        GnInfo.SRC_LINK_TYPE: LinkType.WAN,
        GnInfo.DST_LINK_TYPE: LinkType.ANY,
        GnInfo.LATENCY: Unit.ms(10),
    },
    'BB_SWITCH.0 -> BB_AP.0': {
        GnInfo.SRC_LINK_TYPE: LinkType.ANY,
        GnInfo.DST_LINK_TYPE: LinkType.WAN,
        GnInfo.LATENCY: Unit.ms(10),
    },
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


# device naming rule: DeviceTypeName.ID
DEVICE_LINKS = {
    'SMOKE.0 -> HOME_IOTGW.0': {
        GnInfo.LATENCY: Unit.ms(3),
    },
    'CAMERA.0 -> HOME_IOTGW.0': {
        GnInfo.LATENCY: Unit.ms(3),
    },
    'T2_MICRO.0 -> HOME_ROUTER.0': {
        GnInfo.LATENCY: Unit.ms(1),
    },
    'HOME_ROUTER.0 -> T2_MICRO.0': {
        GnInfo.LATENCY: Unit.ms(1),
    },
    'T3_LARGE.0 -> HOME_ROUTER.0': {
        GnInfo.LATENCY: Unit.ms(1),
    },
    'HOME_ROUTER.0 -> T3_LARGE.0': {
        GnInfo.LATENCY: Unit.ms(1),
    },
    'T2_MICRO.1 -> CLOUD_SWITCH.0': {
        GnInfo.LATENCY: Unit.ms(1),
    },
    'CLOUD_SWITCH.0 -> T2_MICRO.1': {
        GnInfo.LATENCY: Unit.ms(1),
    },
    'T3_LARGE.1 -> CLOUD_SWITCH.0': {
        GnInfo.LATENCY: Unit.ms(1),
    },
    'CLOUD_SWITCH.0 -> T3_LARGE.1': {
        GnInfo.LATENCY: Unit.ms(1),
    },
    'P3_2XLARGE.0 -> CLOUD_SWITCH.0': {
        GnInfo.LATENCY: Unit.ms(1),
    },
    'CLOUD_SWITCH.0 -> P3_2XLARGE.0': {
        GnInfo.LATENCY: Unit.ms(1),
    },
    'PHONE.0 -> BB_AP.0': {
        GnInfo.LATENCY: Unit.ms(10),
    },
    'BB_AP.0 -> PHONE.0': {
        GnInfo.LATENCY: Unit.ms(10),
    },
}


# device naming rule: DeviceTypeName.ID
TASK_MAPPING = {
    'task_smoke': 'SMOKE.0',
    'task_camera': 'CAMERA.0',
    'task_broadcast': 'PHONE.0',
    'task_getAvgReading': None,
    'task_findObject': None,
    'task_checkAbnormalEvent': None,
    'task_sentNotificatoin': None,
}


TASK_LINKS = {
    'task_smoke -> task_getAvgReading': {
        GtInfo.TRAFFIC: Unit.kbyte(1),
    },
    'task_getAvgReading -> task_checkAbnormalEvent': {
        GtInfo.TRAFFIC: Unit.byte(1),
    },
    'task_camera -> task_findObject': {
        GtInfo.TRAFFIC: Unit.mbyte(10),
    },
    'task_findObject -> task_checkAbnormalEvent': {
        GtInfo.TRAFFIC: Unit.byte(10),
    },
    'task_checkAbnormalEvent -> task_sentNotificatoin': {
        GtInfo.TRAFFIC: Unit.byte(1),
    },
    'task_sentNotificatoin -> task_broadcast': {
        GtInfo.TRAFFIC: Unit.byte(1),
    },

}


TASK_INFO = {
    'task_smoke': {
        GtInfo.LATENCY_INFO: {},
        GtInfo.RESRC_RQMT: {}
    },
    'task_camera': {
        GtInfo.LATENCY_INFO: {},
        GtInfo.RESRC_RQMT: {},
    },
    'task_broadcast': {
        GtInfo.LATENCY_INFO: {},
        GtInfo.RESRC_RQMT: {},
    },
    'task_getAvgReading': {
        GtInfo.LATENCY_INFO: {
            Device.T2_MICRO: {
                # TODO: assume one flavor per device type for now.
                # may extend to multiple flavor later
                Flavor.CPU: Unit.ms(15),
            },
            Device.T3_LARGE: {
                Flavor.CPU: Unit.ms(10),
            },
            Device.P3_2XLARGE: {
                Flavor.CPU: Unit.ms(5),
            },
        },
        GtInfo.RESRC_RQMT: {
            Flavor.CPU: {
                Hardware.RAM: Unit.mbyte(1),
                Hardware.HD: Unit.kbyte(3),
                Hardware.GPU: Unit.percentage(0),
                Hardware.CPU: Unit.percentage(5),
            }
        },
    },
    'task_findObject': {
        GtInfo.LATENCY_INFO: {
            Device.T2_MICRO: {
                Flavor.CPU: Unit.sec(6),
            },
            Device.T3_LARGE: {
                Flavor.CPU: Unit.sec(2),
            },
            Device.P3_2XLARGE: {
                Flavor.GPU: Unit.ms(600),
            },
        },
        GtInfo.RESRC_RQMT: {
            Flavor.GPU: {
                Hardware.RAM: Unit.gbyte(4),
                Hardware.HD: Unit.mbyte(30),
                Hardware.GPU: Unit.percentage(60),
                Hardware.CPU: Unit.percentage(5),
            },
            Flavor.CPU: {
                Hardware.RAM: Unit.gbyte(1),
                Hardware.HD: Unit.mbyte(30),
                Hardware.GPU: Unit.percentage(0),
                Hardware.CPU: Unit.percentage(60),
            },
        },
    },
    'task_checkAbnormalEvent': {
        GtInfo.LATENCY_INFO: {
            Device.T2_MICRO: {
                Flavor.CPU: Unit.ms(5),
            },
            Device.T3_LARGE: {
                Flavor.CPU: Unit.ms(5),
            },
            Device.P3_2XLARGE: {
                Flavor.CPU: Unit.ms(5),
            },
        },
        GtInfo.RESRC_RQMT: {
            Flavor.CPU: {
                Hardware.RAM: Unit.mbyte(1),
                Hardware.HD: Unit.kbyte(3),
                Hardware.GPU: Unit.percentage(0),
                Hardware.CPU: Unit.percentage(5),
            },
        },
    },
    'task_sentNotificatoin': {
        GtInfo.LATENCY_INFO: {
            Device.T2_MICRO: {
                Flavor.CPU: Unit.ms(5),
            },
            Device.T3_LARGE: {
                Flavor.CPU: Unit.ms(5),
            },
            Device.P3_2XLARGE: {
                Flavor.CPU: Unit.ms(5),
            },
        },
        GtInfo.RESRC_RQMT: {
            Flavor.CPU: {
                Hardware.RAM: Unit.mbyte(1),
                Hardware.HD: Unit.kbyte(3),
                Hardware.GPU: Unit.percentage(0),
                Hardware.CPU: Unit.percentage(5),
            },
        },
    },
}
