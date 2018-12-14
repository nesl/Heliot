from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from aenum import Enum, auto


class EnumHelper(object):
    @staticmethod
    def enum_to_int(enum_obj):
        assert isinstance(enum_obj, Enum)
        return enum_obj.value

    @staticmethod
    def enum_to_str(enum_obj):
        assert isinstance(enum_obj, Enum)
        return str(enum_obj)

    @staticmethod
    def str_to_enum(str_obj):
        try:
            enum_obj = eval(str_obj)
        except (NameError, SyntaxError):
            enum_obj = str_obj
        return enum_obj

    @staticmethod
    def is_enum(obj):
        return isinstance(obj, Enum)


class Const:
    INT_MAX = 2147483647


class NwLink(Enum):
    ETHERNET = auto()
    WIFI = auto()


class LinkInfo(Enum):
    ULINK_BW = auto()
    DLINK_BW = auto()
    PROTOCOL = auto()
    N_LINKS = auto()


class LinkType(Enum):
    LAN = auto()
    WAN = auto()
    ANY = auto()
    P2P = auto()


class NwDevice(Enum):
    # home
    HOME_ROUTER = auto()
    HOME_IOTGW = auto()
    # backbone
    BB_SWITCH = auto()
    BB_AP = auto()
    # third_party
    CLOUD_SWITCH = auto()
    # TODO: clean this
    # ddflow
    FIELD_SWITCH = auto()
    CENTER_SWITCH = auto()


class NwDeviceCategory(Enum):
    HOME = auto()
    BACKBONE = auto()
    CLOUD = auto()
    # TODO: clean this
    # ddflow
    FIELD = auto()
    CENTER = auto()


class Device(Enum):
    # actuator
    PHONE = auto()
    # processor
    T2_MICRO = auto()
    T3_LARGE = auto()
    P3_2XLARGE = auto()
    # sensor
    SMOKE = auto()
    CAMERA = auto()
    # TODO: clean this
    # ddflow
    CONTROLLER = auto()


class DeviceCategory(Enum):
    ACTUATOR = auto()
    PROCESSOR = auto()
    SENSOR = auto()


class Flavor(Enum):
    GPU = auto()
    CPU = auto()


class NodeType(Enum):
    DEVICE = auto()
    NW_DEVICE = auto()


class GInfo(object):
    # common field Gd and Gn
    class GInfoEnum(Enum):
        NODE_TYPE = auto()

    class helper(type):
        # used as keys for **kwargs for networkx.Digraph.add_node
        def __getattr__(self, name):
            return str(getattr(GInfo.GInfoEnum, name))
    __metaclass__ = helper


class GtInfo(object):
    class GtInfoEnum(Enum):
        TRAFFIC = auto()
        LATENCY_INFO = auto()
        RESRC_RQMT = auto()
        DEVICE = auto()  # initial assigned
        # assign on the fly
        CUR_DEVICE = auto()
        CUR_LATENCY = auto()
        # command to run the task
        EXEC_CMD = auto()

    class helper(type):
        # used as keys for **kwargs for networkx.Digraph.add_node
        def __getattr__(self, name):
            return str(getattr(GtInfo.GtInfoEnum, name))
    __metaclass__ = helper


class GdInfo(object):
    class GdInfoEnum(Enum):
        LATENCY = auto()
        BANDWIDTH = auto()
        HARDWARE = auto()
        COST = auto()
        RESRC = auto()
        DEVICE_CAT = auto()
        DEVICE_TYPE = auto()
        NIC = auto()

    class helper(type):
        # used as keys for **kwargs for networkx.Digraph.add_node
        def __getattr__(self, name):
            return str(getattr(GdInfo.GdInfoEnum, name))
    __metaclass__ = helper


class GnInfo(object):
    class GnInfoEnum(Enum):
        # device properties
        DEVICE_CAT = auto()
        DEVICE_TYPE = auto()
        AVAILABLE_LINKS = auto()
        LINK_INFO = auto()
        # link properties
        SRC_LINK_TYPE = auto()
        DST_LINK_TYPE = auto()
        BANDWIDTH = auto()
        LATENCY = auto()
        PROTOCOL = auto()
        DISTANCE = auto()

    class helper(type):
        # used as keys for **kwargs for networkx.Digraph.add_node
        def __getattr__(self, name):
            return str(getattr(GnInfo.GnInfoEnum, name))
    __metaclass__ = helper


class Hardware(Enum):
    # shared
    RAM = auto()
    HD = auto()
    CPU = auto()
    GPU = auto()
    # derived data / shared
    # NIC_INGRESS = auto()
    # NIC_EGRESS = auto()
    # non-shared
    GPS = auto()
    PROXIMITY = auto()
    ACCELEROMETER = auto()
    GYROSCOPE = auto()
    CAMERA = auto()


class Unit(object):

    _UNIT = 1

    @classmethod
    def percentage(cls, n):
        return n * cls._UNIT

    @classmethod
    def ms(cls, n):
        return n * cls._UNIT

    @classmethod
    def sec(cls, n):
        return n * cls.ms(1000)

    @classmethod
    def bit(cls, n):
        return n * cls._UNIT

    @classmethod
    def byte(cls, n):
        return n * cls.bit(8)

    @classmethod
    def kbyte(cls, n):
        return n * cls.byte(1024)

    @classmethod
    def mbyte(cls, n):
        return n * cls.kbyte(1024)

    @classmethod
    def gbyte(cls, n):
        return n * cls.mbyte(1024)

    @classmethod
    def tbyte(cls, n):
        return n * cls.gbyte(1024)

    @classmethod
    def bps(cls, n):
        return n * cls._UNIT

    @classmethod
    def kbps(cls, n):
        return n * cls.bps(1024)

    @classmethod
    def mbps(cls, n):
        return n * cls.kbps(1024)

    @classmethod
    def gbps(cls, n):
        return n * cls.mbps(1024)

    @classmethod
    def tbps(cls, n):
        return n * cls.gbps(1024)

    @classmethod
    def rph(cls, n):
        # rate per hour
        return n
