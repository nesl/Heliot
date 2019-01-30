"""
Heliot Framework abstractions are Devices, Nodes and Tasks
Devices are part of Testbed and Nodes are part of the scenario which are mapped to Devices

Devices are connected to the physical network. Nodes are connected via virtual network controlled by mininet

The nodes are connected to each other using virtual infranodes.
The connection can have different properties as desired.

"""

"""
id_1, id_2  (connectivity is between 2 types of nodes (node and virtual infranode ),
identified by id_1 and id_2)

_latency, is added as attribute

TODO: Add more keywords to control other network characteristics like packet drops etc.
"""

class mininetLink:

# attributes is a dictionary which defines the mininet Connectivity in more details

    def __init__(self,name='', id_1='',id_2=''):

        #type should be a string
        if isinstance(id_1, str) and isinstance(id_2, str) and isinstance(name, str) and id_1 != id_2:
            self._id_1=id_1
            self._id_2=id_2
            self._name = name
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
