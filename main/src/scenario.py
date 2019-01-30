"""
The definition of workload in Heliot consists of Testbed and Scenario

Scenario defines the (nodes, airsimSensor) (tasks or computations) and mapping etc.
The definition of objects are defined in core folder.
Scenario represents a current usecase which is run by Heliot

"""

"""
Logic and predefined heliot keywords used in the Scenario file:

1) nodes should have unique id. A list of id is maintained and it is ensured each node has
unique id
2) mininet node is special type of node and neednot to be defines in the scenario.
By default a mininet node is assumed part of scenario.
3) airsimSensor should have a unique id. A list of id is maintained and it is ensured each
airsimSensor has unique id

"""

#Heliot imports
from core.node import *
from core.airsimSensor import *
from core.infranode import *
from core.mininetLink import *
from core.taskHeliot import *

#other imports
import logging
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
ch.setLevel(logging.DEBUG)

logger.addHandler(ch)

logger.setLevel(logging.DEBUG)


class scenario:

# scenario has list of Nodes, list of virtual airsim sensors,

    def __init__(self,name=''):
        self._name = name

        # nodes
        self._node = []

        #virtual sensors
        self._airsimSensor = []


        # infrastructure Nodes
        self._infranode = []


        # mininet links between nodes/virtual sensor and virtual infranode
        self._mininetLink=[]


        # Stores the ids of all the nodes in the scenario
        # all node should have unique ids
        self._nodeid = []

        # Stores the ids of all the airsimSensors in the scenario
        # all airsimSensors should have unique ids
        self._airsimSensorid=[]

        # Stores the ids of all the infranodes in the scenario
        # all infranodes should have unique ids
        self._infranodeid=[]




    # Add node to the list of nodes in the scenario
    def add_node(self, n):
        #verify n is node object
        if type(n) is node:
            id = n._id

            # check if device of this id is already present in scenario
            if str(id) in self._nodeid:
                logger.error(str(id)+' is already present in scenario')
                logger.error('id of each node should be unique')
                sys.exit()

            print('Adding node ',id, ' to scenario')
            self._node.append(n)
            self._nodeid.append(str(id))

        else:
            logger.error('add_node called with wrong input')
            sys.exit()

    def add_airsimSensor(self, v):
        #verify v is airsimSensor object
        if type(v) is airsimSensor:
            id = v._id

            # check if airsimSensor of this id is already present in scenario
            if str(id) in self._airsimSensorid:
                logger.error(str(id)+' is already present in scenario')
                logger.error('id of each airsimSensor should be unique')
                sys.exit()

            print('Adding airsimSensor ',id, ' to scenario')
            self._airsimSensor.append(v)
            self._airsimSensorid.append(str(id))

        else:
            logger.error('add_airsimSensor called with wrong input')
            sys.exit()


    # Add infranode to the list of infranodes in the scenario
    def add_infranode(self, inode):
        #verify in is infranode object
        if type(inode) is infranode:
            id = inode._id

            # check if infranode of this id is already present in scenario
            if str(id) in self._infranodeid:
                logger.error(str(id)+' is already present in scenario')
                logger.error('id of each infranode should be unique')
                sys.exit()

            print('Adding infranode ',id, ' to scenario')
            self._infranode.append(inode)
            self._infranodeid.append(str(id))

        else:
            logger.error('add_infranode called with wrong input')
            sys.exit()


    def add_mininetLink(self, l):
        #verify l is mininetLink object
        if type(l) is mininetLink:
            id_1 = l._id_1
            id_2 = l._id_2

            #Checks:
            #  id_1 can be node or  virtual airsim sensor or infranode
            #  id_2 has to be virtual infranode

            if id_1 in self._nodeid or id_1 in self._infranodeid or id_1 in self._airsimSensorid:
                if id_2 in self._infranodeid:

                    print('Adding mininetLink ',l._name, ' to scenario')
                    self._mininetLink.append(l)
                else:
                    logger.error('id_2 in add_mininetLink is not an infranode id')
                    sys.exit()

            else:
                logger.error('id_1 in add_mininetLink has to be a node id or infranode id or airsimSensor id')
                sys.exit()

        else:
            logger.error('add_mininetLink called with wrong input')
            sys.exit()
