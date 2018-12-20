"""
Heliot Framework abstractions are Devices, Nodes and Tasks
Devices are part of Testbed and Nodes are part of the scenario which are mapped to Devices

os.py define the operating system types and definitions (ubuntu, windows , ..) which are part of devices and nodes
"""

class os:

# type is one of [camera, audio, imu , ..]
# attributes is a dictionary which defines the sensors in more details
    def __init__(self,type='',attributes={}):
        self.type = type
        self.attributes = attributes

    def get_info(self):
        info ='\n type:'+str(self.type)+','
        info = info + '\n attributes:'+str(self.attributes)
        return info


    def __repr__(self):
        return self.get_info()

    def __str__(self):
        return self.get_info()
