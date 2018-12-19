"""
Heliot Framework abstractions are Devices, Nodes and Tasks
Devices are part of Testbed and Nodes are part of the scenario which are mapped to Devices

compute.py define the compute which can be part of devices and nodes.
"""

class compute:

# type is one of [cpu, gpu, vpu, ...]
# attributes is a dictionary which defines the compute in more details
    def __init__(self,type='',attributes={}):
        self.type = type
        self.attributes = attributes

    def get_info(self):
        info = 'compute def'
        info = info + '\n'+'*'*50
        info = info + '\n'+str(self.type)
        info = info + '\n'+str(self.attributes)
        return info

    def __repr__(self):
        return self.get_info()

    def __str__(self):
        return self.get_info()
