"""
Heliot Framework abstractions are Devices, Nodes and Tasks
Devices are part of Testbed and Nodes are part of the scenario which are mapped to Devices

Scenario is defined by three types of nodes in the Heliot:
1) node: which refer to the compute node (real/virtual containers) which may have sensors.
2) virtual infrastructure node: which refer to the virtual mininet nodes such as
switches used to connect the nodes
3) virtual sensors: This refers to the virtual sensors defined in Airsim.



infranode.py define the virtual infrastructure nodes which can be part of the scenario.
"""

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



class infranode:

# type is one of [switch, ..]
# attributes is a dictionary which defines the infranode in more details


    def __init__(self,id='', type=''):

        #type should be a string
        if isinstance(type, str) and isinstance(id, str):
            self._type = type
            self._id = id
            self._attributes={}

        else:
            logger.error('__init__ called with wrong input')
            sys.exit()

# Adding info to the  attributes
    def add_attribute(self, key, value):
        #key has to be string
        if isinstance(key,str):
            self._attributes[key]=value
        else:
            logger.error('add_attribute called with wrong input')
            sys.exit()


    def clear_attributes(self):
        self._attributes = {}

    def get_info(self):
        info ='\n type:'+str(self._type)+','
        info = info + '\n attributes:'+str(self._attributes)
        return info

    # def __repr__(self):
    #     return self.get_info()
    #
    # def __str__(self):
    #     return self.get_info()
