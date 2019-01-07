"""
Heliot Framework abstractions are Devices, Nodes and Tasks
Devices are part of Testbed and Nodes are part of the scenario which are mapped to Devices

os.py define the operating system types and definitions (ubuntu, windows , ..) which are part of devices and nodes
"""

class osHeliot:

# type is one of [camera, audio, imu , ..]
# attributes is a dictionary which defines the sensors in more details
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
