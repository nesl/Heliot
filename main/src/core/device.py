"""
Heliot Framework abstractions are Devices, Nodes and Tasks
Devices are part of Testbed and Nodes are part of the scenario which are mapped to Devices

device.py define the device abstrction which refers to testbed physical devices.
"""

from .compute import *
from .memory import *
import sys
import logging

logger = logging.getLogger('In device.py')
# create console handler and set level to debug
ch = logging.StreamHandler()

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)




class device:

# type is one of [mininet_server, airsim_server, server, nvidia_jetson_tx2, google_vision_kit, smartphone , ..]
# attributes is a dictionary which defines the device in more details

# device attributes are: list of compute, memory, list of connection, list of sensors, os and description

#compute is list of compute objects
    _compute=[]

#_memory store the memory objects
    _memory =memory()

    def __init__(self,type=''):
        self._type = type

    def add_compute(self, c):
        #verify c is compute object
        if type(c) is compute:
            self._compute.append(c)
        else:
            logger.error('add_compute called with wrong input')  # will not print anything
            sys.exit()

    def add_memory(self, m):
        #verify m is memory object
        if type(m) is memory:
            self._memory = m
        else:
            logger.error('add_memory called with wrong input')  # will not print anything
            sys.exit()

    def get_info(self):

        attributes = {
        'compute':self._compute,
        'memory' : self._memory
        }


        return self._type, attributes


    # def __repr__(self):
    #     return self.get_info()
    #
    # def __str__(self):
    #     return self.get_info()
