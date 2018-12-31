"""
The definition of workload in Heliot consists of Testbed and Scenario

Testbed defines the physical devices. The devices are defined in core folder.
Testbed consists of list of devices

"""


#Heliot imports
from core.device import *

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



class testbed:

# testbed has list of devices
# device attributes  defines the device in more details
# device attributes are: list of compute, memory, list of connection, list of sensors, os and description



    def __init__(self,name=''):
        self._name = name

        # _device store the list of physical devices
        self._device = []

    def add_device(self, d):
        #verify c is compute object
        if type(d) is device:
            self._device.append(d)
        else:
            logger.error('add_device called with wrong input')
            sys.exit()

    def get_info(self):
        return self._name, self._device



#t1 = testbed('mytestbed')

#print(t1.get_info())
