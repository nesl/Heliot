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
#Network imports for mininet
from network.netHeliot import *
#Task import
from core.taskHeliot import *

#other imports
import os
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

        # This is initialized and connectivity is assigned by start_network() function
        self._net=None

        # list of tasks in the scenario to run
        self._tasks=[]
        #stores the ids of all the tasks in the Scenario
        #used to verify one task is added only once
        self._taskid=[]



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

    def add_task(self, task):
        if type(task) is taskHeliot:
            if id in self._taskid:
                print('Task:',self._taskid,'  is already part of scenario')
            else:
                self._tasks.append(task)
                print('Adding task:',task._taskid)
                self._taskid.append(task._taskid)
        else:
            logger.error('add_task called with wrong input')
            sys.exit()



    def stop_network(self):
        print('Stopping the network');11
        self._net._network.stop()

    def start_network(self):

        # a digit has to be added as part of the id, else
        # mininet is not able to initialize the switches and hosts

        mininet_id="0"

        if os.getuid()!=0:
            logger.error('Heliot cannot start network without sudo privileges')
            logger.error('if using jupyter, use: "sudo jupyter notebook --allow-root"')
            sys.exit()
        else:

            # Note this has to be started on the mininet machine
            # At present, I am assuming my work machine is mininet machine

            self._net = netHeliot()

            #adding the virtual infrastructure nodes
            # virtual switches
            print('Adding infranodes to the network')
            for inode in self._infranode:
                #print('Adding:',inode._id+mininet_id)
                self._net.add_switch(inode._id+mininet_id)

            print('Adding nodes to the network')
            #Adding other nodes as hosts
            for node in self._node:
                self._net.add_host(node._id+mininet_id)

            print('Adding airSim sensors to the network')
            for sensor in self._airsimSensor:
                self._net.add_host(sensor._id+mininet_id)

            #Add the links
            for link in self._mininetLink:
                self._net.add_link(link._id_1+mininet_id, link._id_2+mininet_id)

            print('Starting the network using Mininet')
            self._net._network.start()
            self._net._network.pingAll()
            #self.net._network.stop()
