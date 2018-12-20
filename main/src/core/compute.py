"""
Heliot Framework abstractions are Devices, Nodes and Tasks
Devices are part of Testbed and Nodes are part of the scenario which are mapped to Devices

compute.py define the compute which can be part of devices and nodes.
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



class compute:

# type is one of [cpu, gpu, vpu, ...]
# attributes is a dictionary which defines the compute in more details
    def __init__(self,type=''):

        
        #type should be a string
        if isinstance(type, str):
            self.type = type

        else:
            logger.error('__init__ called with wrong input')
            sys.exit()


    def get_info(self):
        info ='\n type:'+str(self.type)+','
        info = info + '\n attributes:'+str(self.attributes)
        return info

    # def __repr__(self):
    #     return self.get_info()
    #
    # def __str__(self):
    #     return self.get_info()
