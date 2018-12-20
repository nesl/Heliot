"""
Heliot Framework abstractions are Devices, Nodes and Tasks
Devices are part of Testbed and Nodes are part of the scenario which are mapped to Devices

device.py define the device abstrction which refers to testbed physical devices.
"""

#Heliot imports
from .compute import *
from .memory import *
from .connection import *
from .sensor import *
from .os import *

#other imports
import sys
import logging

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
ch.setLevel(logging.DEBUG)

logger.addHandler(ch)

logger.setLevel(logging.DEBUG)



class device:

# device type is one of [mininet_server, airsim_server, server, nvidia_jetson_tx2, google_vision_kit, smartphone , ..]
# device attributes  defines the device in more details

# device attributes are: list of compute, memory, list of connection, list of sensors, os and description


    def __init__(self,type=''):
        self._type = type
        #compute is list of compute objects
        self._compute=[]

        #_memory store the memory objects
        self._memory =None

        # _connection store the list of connection object
        self._connection = []

        # _sensor store the list of sensors
        self._sensor = []

        # _os store the os object
        self._os = None

    def add_compute(self, c):
        #verify c is compute object
        if type(c) is compute:
            self._compute.append(c)
        else:
            logger.error('add_compute called with wrong input')
            sys.exit()

    def add_memory(self, m):
        #verify m is memory object
        if type(m) is memory:
            self._memory = m
        else:
            logger.error('add_memory called with wrong input')
            sys.exit()

    def add_connection(self, con):
        #verify c is compute object
        if type(con) is connection:
            self._connection.append(con)
        else:
            logger.error('add_connection called with wrong input')
            sys.exit()

    def add_sensor(self, s):
        #verify c is compute object
        if type(s) is sensor:
            self._sensor.append(s)
        else:
            logger.error('add_sensor called with wrong input')
            sys.exit()

    def add_os(self, o):
        #verify m is memory object
        if type(o) is os:
            self._os = o
        else:
            logger_device.error('add_os called with wrong input')
            sys.exit()


    def get_info(self):

        attributes = {
        '_compute':self._compute,
        '_memory' : self._memory,
        '_connection' : self._connection,
        '_sensor': self._sensor,
        '_os': self._os
        }


        return self._type, attributes


    # def __repr__(self):
    #     return self.get_info()
    #
    # def __str__(self):
    #     return self.get_info()
