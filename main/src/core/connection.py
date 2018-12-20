"""
Heliot Framework abstractions are Devices, Nodes and Tasks
Devices are part of Testbed and Nodes are part of the scenario which are mapped to Devices

connection.py define the connection definition (ssh, REST) which are part of devices.
"""

class connection:

# type is one of [ram, ...]
# attributes is a dictionary which defines the connection in more details
    def __init__(self,type='',attributes={}):
        self.type = type
        self.attributes = attributes

    def get_info(self):
        info ='\n type:'+str(self.type)+','
        info = info + '\n attributes:'+str(self.attributes)
        return info


    # def __repr__(self):
    #     return self.get_info()
    #
    # def __str__(self):
    #     return self.get_info()
