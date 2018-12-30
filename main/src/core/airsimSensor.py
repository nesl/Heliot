"""
Heliot Framework abstractions are Devices, Nodes and Tasks
Devices are part of Testbed and Nodes are part of the scenario which are mapped to Devices

Scenario is defined by three types of nodes in the Heliot:
1) node: which refer to the compute node (real/virtual containers) which may have sensors.
2) virtual infrastructure node: which refer to the virtual mininet nodes such as switches used to connect the nodes
3) virtual sensor nodes: This refers to the virtual sensors nodes defined in Airsim. At present we only consider airsim virtual sensors

airsimSensor.py define the  virtual sensors of Airsim abstrction for the scenario.

To Do: Extend this abstrction to other types of virtual sensors.
"""


class airsimSensor:

# type is one of [drone, car, cv , ..]
# attributes is a dictionary which defines the airsimSensors in more details

    def __init__(self,type=''):

        #type should be a string
        if isinstance(type, str):
            self._type = type
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
