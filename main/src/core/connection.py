"""
Heliot Framework abstractions are Devices, Nodes and Tasks
Devices are part of Testbed and Nodes are part of the scenario which are mapped to Devices

connection.py define the connection definition (ssh, REST) which are part of devices.
"""

"""
Predefined connection keywords:
type: _ssh, _rest

1) for _ssh:
_ip, _username, _password: to connect to the linux, windows machines

2) for _rest:
TODO: need to add
"""


class connection:

# type is one of [_ssh, _rest]
# attributes is a dictionary which defines the connection in more details
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
        return self._type, self._attributes


    # def __repr__(self):
    #     return self.get_info()
    #
    # def __str__(self):
    #     return self.get_info()
